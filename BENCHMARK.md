# Data Ingestion & Vector Retrieval

### A. Strategi Pemotongan Teks (Chunking)
Ini akan sangat memengaruhi apa yang direpresentasikan oleh vektor.

Ukuran (Size): 128, 256, 512, 1024 token.

Tumpang Tindih (Overlap): 0%, 10%, 25%.

Metode: Pemotongan statis (jumlah karakter fix) vs Pemotongan sintaksis (berhenti di titik/akhir paragraf) vs Semantic Chunking (berhenti saat topik berubah).

### B. Representasi Vektor (Embedding Model)
Pada benchmark awal ini, model embedding dibuat **tetap** agar hasil uji chunk lebih adil.

Model yang digunakan:

```text
sentence-transformers/all-MiniLM-L6-v2
```

Alasannya: tujuan benchmark saat ini adalah melihat pengaruh **jumlah chunk yang diambil (Top-K)**, bukan membandingkan model embedding. Jika model embedding ikut diganti, hasil akan sulit dibaca karena kita tidak tahu peningkatan berasal dari chunking atau dari model embedding.

Perbandingan model seperti `BAAI/bge-m3`, `nomic-ai/nomic-embed-text-v1.5`, atau embedding API lain sebaiknya dilakukan pada tahap lanjutan setelah konfigurasi chunk terbaik ditemukan.

### C. Variasi Tipe Query (Query Diversity)
Untuk mengevaluasi ketangguhan sistem pencarian secara komprehensif, pengujian (metrik *Hit Rate*) harus menggunakan variasi kueri berikut:

1. **Factoid/Simple Query:** Pertanyaan langsung (Misal: "Berapa dimensi dari model embedding BGE-M3?").
2. **Reasoning/Complex Query:** Pertanyaan yang membutuhkan sintesis konsep (Misal: "Mengapa IVF-PQ lebih hemat memori dibandingkan HNSW?").
3. **Paraphrased/Semantic Query:** Pertanyaan yang sengaja TIDAK menggunakan istilah yang ada di dalam teks, tetapi maknanya sama. Ini adalah ujian sesungguhnya bagi sebuah *Vector Database*.
4. **Conversational/Noisy Query:** Pertanyaan dengan gaya bahasa kasual, tidak baku, atau mengandung sedikit *typo*, menyerupai ketikan pengguna asli di dunia nyata.

## Hasil Benchmarking Saat Ini

Benchmark ini menguji retrieval dengan **embedding Transformer saja**, tanpa Gemini. Variabel yang diuji adalah `Top-K`, yaitu jumlah chunk yang diambil dari Qdrant.

Konfigurasi uji:

| Komponen | Nilai |
| --- | --- |
| Collection | `scientific_articles` |
| Total chunk di DB | `109` |
| Model embedding | `sentence-transformers/all-MiniLM-L6-v2` |
| Metode chunking | Hybrid Markdown header + recursive splitter |
| Filter metadata | Ya, filter DOI |
| DOI target | `10.1016/j.undsp.2024.04.008` |
| Jumlah query uji | `3` |
| File hasil | `benchmark_results/retrieval_benchmark.md` |

Ringkasan hasil:

| Top-K | Jumlah Query | Hit Rate | MRR | Rata-rata Latensi | Kesimpulan |
| ---: | ---: | ---: | ---: | ---: | --- |
| `1` | `3` | `0.0%` | `0.000` | `91.5 ms` | Terlalu sedikit; belum menemukan chunk jawaban |
| `3` | `3` | `0.0%` | `0.000` | `133.1 ms` | Masih belum cukup; jawaban belum muncul di 3 chunk teratas |
| `5` | `3` | `33.3%` | `0.083` | `47.7 ms` | Mulai menemukan jawaban, tetapi belum stabil |

Detail penting dari hasil:

| Query | Top-K Berhasil | Ranking Chunk Jawaban | Catatan |
| --- | ---: | ---: | --- |
| `q1` - main contribution | - | - | Belum menemukan expected terms |
| `q2` - proposed method | - | - | Belum menemukan expected terms |
| `q3` - experimental results | `5` | `4` | Jawaban baru muncul pada ranking ke-4 |

Kesimpulan sementara:

```text
Top-K=5 adalah hasil terbaik dari pengujian Top-K 1, 3, dan 5.
Namun Top-K=5 belum bisa disebut optimal karena hit rate masih 33.3%.
```

Rekomendasi berikutnya:

1. Uji `Top-K=10` dan `Top-K=15`.
2. Perbaiki `expected_terms` agar memakai istilah spesifik dari paper, bukan kata umum.
3. Setelah Top-K terbaik ditemukan, baru lanjutkan benchmark ukuran chunk seperti `500`, `1000`, dan `1500`.

## Benchmark Jumlah Chunk yang Diambil (Top-K)

Untuk mencari jumlah chunk yang optimal saat RAG, uji nilai `Top-K` berbeda pada data dan query yang sama. `Top-K` adalah jumlah chunk yang dikirim dari Qdrant ke LLM/Gemini.

Panduan lengkap tersedia di:

```text
docs/BENCHMARK_GUIDE.md
```

Skrip yang digunakan:

```powershell
python scripts\benchmark_retrieval.py --top-k 1,3,5,10
```

Output dibuat otomatis dalam bentuk tabel:

```text
benchmark_results/retrieval_benchmark.md
benchmark_results/retrieval_benchmark.csv
```

File query uji default ada di:

```text
benchmark_queries.example.json
```

Sebelum dipakai serius, salin atau edit file tersebut lalu isi `expected_terms` dengan kata/frasa jawaban yang benar dari paper Anda. Contoh:

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

Makna kolom hasil:

| Kolom | Makna |
| --- | --- |
| `collection` | Nama collection Qdrant yang diuji |
| `total_chunks_db` | Total chunk yang tersimpan di collection |
| `top_k` | Jumlah chunk yang diambil dari Qdrant |
| `hit_rate` | Persentase query yang menemukan `expected_terms` di hasil retrieval |
| `mrr` | Mean Reciprocal Rank; makin dekat ke 1 makin baik karena jawaban muncul di ranking atas |
| `avg_latency_ms` | Rata-rata waktu pencarian |

## Benchmark Ukuran Chunk Ingest

Jika ingin membandingkan ukuran chunk `500`, `1000`, dan `1500`, buat collection berbeda agar hasilnya tidak bercampur:

```powershell
python ingest.py .\papers\ --collection chunks_500 --chunk-size 500 --chunk-overlap 100
python ingest.py .\papers\ --collection chunks_1000 --chunk-size 1000 --chunk-overlap 200
python ingest.py .\papers\ --collection chunks_1500 --chunk-size 1500 --chunk-overlap 300
```

Lalu bandingkan collection tersebut dengan query uji yang sama:

```powershell
python scripts\benchmark_retrieval.py --collections chunks_500,chunks_1000,chunks_1500 --top-k 1,3,5,10
```

Interpretasi cepat:

| Pola Hasil | Kesimpulan |
| --- | --- |
| `hit_rate` naik saat `top_k` naik, tapi latensi masih aman | Gunakan `top_k` lebih besar |
| `hit_rate` sama antara `top_k=5` dan `top_k=10` | Pilih `top_k=5` karena lebih hemat konteks |
| `chunks_500` hit rate tinggi tapi latensi/konteks besar | Chunk kecil bagus untuk recall, tetapi boros konteks |
| `chunks_1500` hit rate rendah | Chunk terlalu besar; embedding menjadi kurang spesifik |
| MRR tinggi pada `chunks_1000` | Biasanya konfigurasi ini paling seimbang |

## Panduan Pengisian Benchmarking

Evaluasi Sistem *Retrieval* (Pengambilan Data) adalah nyawa dari arsitektur RAG. Berikut adalah penjelasan ringkas mengapa kolom-kolom metrik di atas sangat penting untuk dipantau dalam fase eksperimen Anda:

### 1. `Top-K (Limit)`
- **Definisi:** Jumlah *chunk* maksimal yang dikembalikan oleh Qdrant ke Gemini.
- **Insight:** Terkadang, menyetel *Top-K* ke angka 10 dengan ukuran *chunk* yang lebih kecil (misal 500 karakter) justru memberikan konteks yang jauh lebih beragam (berasal dari berbagai halaman) dibandingkan mengambil *Top-K* 3 dengan *chunk* raksasa.

### 2. `Hit Rate (Recall@K)`
- **Definisi:** Persentase keberhasilan sistem menemukan "*Chunk* yang mengandung jawaban yang benar" pada pencarian Top-K.
- **Insight:** Ini adalah metrik paling krusial. Anda bisa membuat 10 pasang pertanyaan-jawaban tes. Jika dari 10 pertanyaan tersebut Qdrant berhasil menemukan paragraf yang tepat sebanyak 8 kali di peringkat atas, maka *Hit Rate (Recall)* Anda adalah 80%. Semakin tinggi nilainya, semakin kecil risiko LLM berhalusinasi.

### 3. `Filter Metadata`
- **Definisi:** Apakah pencarian menggunakan *pre-filtering* (seperti membatasi pencarian hanya pada DOI atau *Section Header* tertentu)?
- **Insight:** Filter DOI bisa meningkatkan *Hit Rate* menjadi nyaris 100% secara instan karena sistem secara eksplisit "membuang" gangguan teks (*noise*) dari jurnal lain yang tidak relevan.

### 4. `Rata-rata Latensi (ms)`
- **Definisi:** Waktu komputasi komprehensif dari saat kueri dikirim hingga Qdrant mengembalikan hasilnya.
- **Insight:** Sangat krusial untuk lingkungan *Production*. Jika Anda beralih menggunakan model *embedding* raksasa, latensi pencarian bisa melambung tinggi. Harus diperhitungkan jika aplikasi akan diakses ratusan pengguna serentak.

### 5. `Ukuran Index DB (MB)`
- **Definisi:** Ukuran total folder *database* lokal (contoh: `qdrant_db/`) untuk jumlah kumpulan jurnal uji tertentu.
- **Insight:** Berhubungan langsung dengan konsumsi *Storage* dan *RAM/VRAM* di *Cloud*. Apakah mengorbankan akurasi sebesar 2% sepadan dengan penghematan penyimpanan sebesar 50%? Jawabannya dapat dievaluasi di sini.

### 6. `Dukungan Bahasa (Language Support)`
- **Definisi:** Kemampuan model untuk memetakan bahasa yang berbeda ke dalam ruang semantik yang berdekatan (*Cross-Lingual Information Retrieval*).
- **Insight:** Sangat krusial jika *database* Anda berisi jurnal Bahasa Inggris, tetapi *user* memasukkan pencarian (*query*) dalam Bahasa Indonesia. Model *Multi-bahasa* seperti BGE-M3 dapat mempertemukan *query* Bahasa Indonesia dengan teks jurnal Bahasa Inggris secara cerdas, sedangkan model *Hanya Inggris* (seperti MiniLM) akan gagal total dalam skenario lintas-bahasa ini.
