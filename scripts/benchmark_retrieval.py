#!/usr/bin/env python3
"""
Benchmark retrieval quality for different Qdrant collections and Top-K values.

The benchmark is evidence-based but simple: a query is counted as a hit when
the retrieved chunks contain the expected term(s) configured in the query file.
"""

import argparse
import csv
import json
import statistics
import sys
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


def parse_int_list(raw: str) -> list[int]:
    values = []
    for item in raw.split(","):
        item = item.strip()
        if item:
            values.append(int(item))
    return values


def load_queries(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as f:
        queries = json.load(f)
    if not isinstance(queries, list) or not queries:
        raise ValueError("Query file must contain a non-empty JSON array.")
    return queries


def term_hit(text: str, expected_terms: list[str], match_mode: str) -> bool:
    if not expected_terms:
        return False
    text_lower = text.lower()
    checks = [term.lower() in text_lower for term in expected_terms if term.strip()]
    if not checks:
        return False
    if match_mode == "all":
        return all(checks)
    return any(checks)


def first_hit_rank(results: list[dict], expected_terms: list[str], match_mode: str) -> int | None:
    for idx, result in enumerate(results, 1):
        if term_hit(result["content"], expected_terms, match_mode):
            return idx
    return None


def summarize_sections(results: list[dict]) -> str:
    sections = []
    for result in results:
        section = result["metadata"].get("section_header", "Unknown")
        if section not in sections:
            sections.append(section)
    return "; ".join(sections[:3])


def run_benchmark(args: argparse.Namespace) -> tuple[list[dict], list[dict]]:
    from core.vector_store import VectorStore

    queries = load_queries(Path(args.queries))
    top_k_values = parse_int_list(args.top_k)
    collections = [item.strip() for item in args.collections.split(",") if item.strip()]

    rows = []
    summary_rows = []

    for collection in collections:
        store = VectorStore(
            qdrant_path=args.qdrant_path,
            collection_name=collection,
        )
        store.ensure_collection()

        try:
            collection_info = store.get_collection_info()

            for top_k in top_k_values:
                latencies = []
                hits = []
                reciprocal_ranks = []

                for query_item in queries:
                    started = time.perf_counter()
                    results = store.search(
                        query=query_item["query"],
                        n_results=top_k,
                        doi_filter=query_item.get("doi") or None,
                    )
                    elapsed_ms = (time.perf_counter() - started) * 1000

                    expected_terms = query_item.get("expected_terms", [])
                    match_mode = query_item.get("match", "any").lower()
                    combined_context = "\n".join(r["content"] for r in results)
                    hit = term_hit(combined_context, expected_terms, match_mode)
                    rank = first_hit_rank(results, expected_terms, match_mode)
                    avg_score = statistics.mean([r["score"] for r in results]) if results else 0.0
                    context_chars = len(combined_context)

                    latencies.append(elapsed_ms)
                    hits.append(1 if hit else 0)
                    reciprocal_ranks.append((1 / rank) if rank else 0)

                    rows.append(
                        {
                            "collection": collection,
                            "total_chunks_db": collection_info["points_count"],
                            "top_k": top_k,
                            "query_id": query_item.get("id", ""),
                            "query_type": query_item.get("query_type", ""),
                            "doi": query_item.get("doi", ""),
                            "hit": "yes" if hit else "no",
                            "first_hit_rank": rank or "",
                            "avg_score": f"{avg_score:.4f}",
                            "latency_ms": f"{elapsed_ms:.1f}",
                            "context_chars": context_chars,
                            "top_sections": summarize_sections(results),
                            "query": query_item["query"],
                        }
                    )

                summary_rows.append(
                    {
                        "collection": collection,
                        "total_chunks_db": collection_info["points_count"],
                        "top_k": top_k,
                        "queries": len(queries),
                        "hit_rate": f"{(sum(hits) / len(hits)) * 100:.1f}%",
                        "mrr": f"{statistics.mean(reciprocal_ranks):.3f}",
                        "avg_latency_ms": f"{statistics.mean(latencies):.1f}",
                    }
                )
        finally:
            store.client.close()

    return summary_rows, rows


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ").replace("|", "/") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_markdown(path: Path, summary_rows: list[dict], detail_rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = "\n\n".join(
        [
            "# Retrieval Benchmark Results",
            "## Summary",
            markdown_table(summary_rows),
            "## Detail",
            markdown_table(detail_rows),
            "",
        ]
    )
    path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Benchmark PEDE retrieval with comparable Markdown and CSV tables."
    )
    parser.add_argument(
        "--queries",
        default="benchmark_queries.example.json",
        help="Path to JSON query set with expected_terms.",
    )
    parser.add_argument(
        "--collections",
        default="scientific_articles",
        help="Comma-separated Qdrant collections to compare.",
    )
    parser.add_argument(
        "--top-k",
        default="1,3,5,10",
        help="Comma-separated Top-K values to test.",
    )
    parser.add_argument(
        "--qdrant-path",
        default="./qdrant_db",
        help="Qdrant local DB path.",
    )
    parser.add_argument(
        "--out-md",
        default="benchmark_results/retrieval_benchmark.md",
        help="Markdown table output path.",
    )
    parser.add_argument(
        "--out-csv",
        default="benchmark_results/retrieval_benchmark.csv",
        help="CSV detail output path.",
    )
    args = parser.parse_args()

    summary_rows, detail_rows = run_benchmark(args)
    write_markdown(Path(args.out_md), summary_rows, detail_rows)
    write_csv(Path(args.out_csv), detail_rows)

    print("\nSummary")
    print(markdown_table(summary_rows))
    print(f"\nSaved Markdown: {args.out_md}")
    print(f"Saved CSV:      {args.out_csv}")


if __name__ == "__main__":
    main()
