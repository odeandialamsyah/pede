# Panduan Benchmark Retrieval PEDE

Dokumen ini menjelaskan cara menguji jumlah chunk yang optimal untuk RAG di project PEDE. Tujuannya sederhana: menemukan konfigurasi yang paling seimbang antara **jawaban akurat**, **konteks tidak terlalu panjang**, dan **latensi masih cepat**.

## Gambaran Singkat

Dalam RAG, sistem tidak langsung mengirim seluruh PDF ke Gemini. PEDE mengambil beberapa potongan teks paling relevan dari Qdrant, lalu potongan itu dikirim sebagai konteks.

Potongan teks itu disebut **chunk**.

Jumlah chunk yang diambil disebut **Top-K**.

Contoh:

| Top-K | Artinya |
| ---: | --- |
| `1` | Ambil 1 chunk paling relevan |
| `3` | Ambil 3 chunk paling relevan |
| `5` | Ambil 5 chunk paling relevan |
| `10` | Ambil 10 chunk paling relevan |

Semakin besar Top-K, peluang menemukan jawaban biasanya naik. Tapi konteks juga makin panjang, biaya LLM bisa naik, dan jawaban bisa lebih berisik kalau chunk yang diambil terlalu banyak.

## File Penting

| File | Fungsi |
| --- | --- |
| `benchmark_queries.example.json` | Daftar pertanyaan uji dan kata/frasa jawaban yang diharapkan |
| `scripts/benchmark_retrieval.py` | Skrip benchmark retrieval |
| `benchmark_results/retrieval_benchmark.md` | Hasil benchmark dalam bentuk tabel Markdown |
| `benchmark_results/retrieval_benchmark.csv` | Hasil detail dalam format CSV |
| `BENCHMARK.md` | Catatan umum dan template benchmark project |

## Cara Menjalankan Benchmark

Jalankan dari root project:

```powershell
python scripts\benchmark_retrieval.py --top-k 1,3,5,10
```

Setelah selesai, hasil akan dibuat di:

```text
benchmark_results/retrieval_benchmark.md
benchmark_results/retrieval_benchmark.csv
```

Gunakan file Markdown untuk membaca cepat. Gunakan CSV jika ingin membuka hasil di Excel, Google Sheets, atau membuat grafik.

## Cara Mengisi Query Uji

Buka:

```text
benchmark_queries.example.json
```

Contoh isi:

```json
{
  "id": "q1",
  "query_type": "method",
  "query": "What method is proposed in this paper?",
  "doi": "10.1016/j.undsp.2024.04.008",
  "expected_terms": ["nama metode utama"],
  "match": "any"
}
```

Penjelasan field:

| Field | Penjelasan |
| --- | --- |
| `id` | ID pendek untuk pertanyaan |
| `query_type` | Jenis pertanyaan, misalnya `factoid`, `method`, `result`, atau `semantic` |
| `query` | Pertanyaan yang akan dikirim ke Qdrant |
| `doi` | DOI paper target agar pencarian fokus ke satu artikel |
| `expected_terms` | Kata/frasa yang harus muncul di chunk agar dianggap berhasil |
| `match` | `any` berarti cukup salah satu term muncul, `all` berarti semua term harus muncul |

Tips penting: isi `expected_terms` dengan istilah spesifik dari paper. Jangan terlalu umum.

Kurang kuat:

```json
"expected_terms": ["method", "result"]
```

Lebih kuat:

```json
"expected_terms": ["nama model", "nama dataset", "nilai akurasi"]
```

## Cara Membaca Hasil Summary

Contoh hasil:

| collection | total_chunks_db | top_k | queries | hit_rate | mrr | avg_latency_ms |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| scientific_articles | 109 | 1 | 3 | 0.0% | 0.000 | 91.5 |
| scientific_articles | 109 | 3 | 3 | 0.0% | 0.000 | 133.1 |
| scientific_articles | 109 | 5 | 3 | 33.3% | 0.083 | 47.7 |

Maknanya:

| Kolom | Arti |
| --- | --- |
| `collection` | Nama collection Qdrant yang diuji |
| `total_chunks_db` | Total chunk di database |
| `top_k` | Jumlah chunk yang diambil saat search |
| `queries` | Jumlah pertanyaan uji |
| `hit_rate` | Persentase query yang berhasil menemukan chunk berisi jawaban |
| `mrr` | Seberapa tinggi ranking chunk jawaban; makin dekat ke `1.000` makin bagus |
| `avg_latency_ms` | Rata-rata waktu pencarian dalam milidetik |

## Interpretasi Hasil Awal

Dari hasil contoh:

| Top-K | Hit Rate | Kesimpulan |
| ---: | ---: | --- |
| `1` | `0.0%` | Terlalu sedikit, jawaban tidak ditemukan |
| `3` | `0.0%` | Masih belum cukup |
| `5` | `33.3%` | Mulai menemukan jawaban, tapi belum stabil |

Kesimpulan sementara:

```text
Top-K=5 lebih baik daripada Top-K=1 dan Top-K=3,
tetapi belum bisa disebut optimal karena hit rate masih rendah.
```

Langkah berikutnya adalah menguji:

```powershell
python scripts\benchmark_retrieval.py --top-k 1,3,5,10,15
```

Jika `Top-K=10` menaikkan hit rate secara jelas, gunakan `10`. Jika `Top-K=10` sama saja dengan `5`, gunakan `5` karena lebih hemat konteks.

## Cara Membaca Detail CSV

File CSV berisi hasil per query. Kolom penting:

| Kolom | Arti |
| --- | --- |
| `query_id` | Pertanyaan mana yang diuji |
| `hit` | `yes` jika jawaban ditemukan, `no` jika tidak |
| `first_hit_rank` | Posisi pertama chunk jawaban ditemukan |
| `avg_score` | Rata-rata skor similarity hasil retrieval |
| `context_chars` | Panjang konteks yang akan dikirim ke LLM |
| `top_sections` | Section artikel yang paling sering muncul di hasil retrieval |

Contoh:

| query_id | top_k | hit | first_hit_rank |
| --- | ---: | --- | ---: |
| q3 | 5 | yes | 4 |

Artinya, untuk query `q3`, jawaban baru muncul di chunk ranking ke-4. Jadi `Top-K=3` gagal, sedangkan `Top-K=5` berhasil.

## Benchmark Ukuran Chunk

Selain Top-K, ukuran chunk saat ingest juga penting.

Untuk membandingkan chunk kecil, sedang, dan besar, buat collection berbeda:

```powershell
python ingest.py .\papers\ --collection chunks_500 --chunk-size 500 --chunk-overlap 100
python ingest.py .\papers\ --collection chunks_1000 --chunk-size 1000 --chunk-overlap 200
python ingest.py .\papers\ --collection chunks_1500 --chunk-size 1500 --chunk-overlap 300
```

Lalu jalankan benchmark:

```powershell
python scripts\benchmark_retrieval.py --collections chunks_500,chunks_1000,chunks_1500 --top-k 1,3,5,10
```

Panduan membaca:

| Hasil | Kemungkinan Kesimpulan |
| --- | --- |
| `chunks_500` hit rate tinggi | Chunk kecil membantu menemukan jawaban spesifik |
| `chunks_500` context terlalu panjang | Banyak chunk kecil membuat konteks boros |
| `chunks_1000` hit rate tinggi dan latensi aman | Biasanya kandidat konfigurasi seimbang |
| `chunks_1500` hit rate rendah | Chunk terlalu besar, embedding kurang fokus |

## Cara Menentukan Konfigurasi Terbaik

Gunakan aturan praktis ini:

| Kondisi | Pilihan |
| --- | --- |
| Hit rate paling tinggi dan MRR tinggi | Kandidat terbaik |
| Hit rate sama, Top-K lebih kecil | Pilih Top-K lebih kecil |
| Hit rate naik sedikit, konteks jauh lebih panjang | Pertimbangkan tetap pakai konfigurasi lebih kecil |
| Latensi terlalu tinggi | Turunkan Top-K atau pakai chunk size lebih seimbang |

Rekomendasi format keputusan:

```text
Konfigurasi terbaik sementara:
- Chunk size: 1000
- Overlap: 200
- Top-K: 5
- Alasan: hit rate terbaik pada data uji saat ini, konteks masih cukup kecil, dan latensi masih aman.
```

## Checklist Eksperimen

Sebelum menyimpulkan hasil, pastikan:

| Checklist | Status |
| --- | --- |
| Minimal 5-10 query uji dibuat | |
| Query mencakup method, result, contribution, dan conclusion | |
| `expected_terms` sudah spesifik | |
| Benchmark Top-K sudah diuji | |
| Benchmark chunk size sudah diuji | |
| Hasil Markdown/CSV disimpan | |
| Kesimpulan ditulis berdasarkan `hit_rate`, `mrr`, dan `latency` | |

## Catatan

Benchmark ini mengukur kualitas retrieval, bukan kualitas jawaban Gemini secara langsung. Jika retrieval gagal menemukan chunk yang benar, Gemini kemungkinan besar akan menjawab tidak lengkap atau mengatakan informasi tidak ditemukan.

Dengan kata lain:

```text
RAG yang baik dimulai dari retrieval yang baik.
```

