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

Benchmark ini menguji retrieval dengan **embedding Transformer saja**, tanpa Gemini. Variabel yang diuji adalah:

1. Ukuran chunk saat ingest: `500`, `1000`, dan `1500` karakter.
2. Jumlah chunk yang diambil saat retrieval: `Top-K = 1, 3, 5, 10, 15, 20`.

Konfigurasi uji:

| Komponen | Nilai |
| --- | --- |
| Dokumen uji | `papers/1-s2.0-S2467967424000813-main.pdf` |
| Judul paper | `Hybrid deep learning approach for rock tunnel deformation prediction based on spatio-temporal patterns` |
| DOI target | `10.1016/j.undsp.2024.04.008` |
| Model embedding | `sentence-transformers/all-MiniLM-L6-v2` |
| Dimensi embedding | `384` |
| Metode chunking | Hybrid Markdown header + recursive splitter |
| Filter metadata | Ya, filter DOI |
| Jumlah query uji | `3` |
| File query | `benchmark_queries.example.json` |
| File hasil Top-K default | `benchmark_results/retrieval_benchmark_topk.md` |
| File hasil chunk comparison | `benchmark_results/retrieval_benchmark_chunks.md` |

### Ringkasan Collection

| Collection | Chunk Size | Overlap | Total Chunk | Rata-rata Panjang Chunk | Catatan |
| --- | ---: | ---: | ---: | ---: | --- |
| `chunks_500` | `500` | `100` | `203` | sekitar `360` karakter | Chunk lebih kecil, retrieval lebih spesifik |
| `chunks_1000` | `1000` | `200` | `109` | sekitar `703` karakter | Konfigurasi sedang/default |
| `chunks_1500` | `1500` | `300` | `71` | sekitar `1104` karakter | Chunk lebih besar, jumlah point lebih sedikit |

### Tabel Perbandingan Lengkap

| Collection | Total Chunk | Top-K | Hit Rate | MRR | Avg Latency | Avg Context Chars |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `chunks_500` | 203 | 1 | 0.0% | 0.000 | 75.7 ms | 209 |
| `chunks_500` | 203 | 3 | 33.3% | 0.167 | 58.0 ms | 779 |
| `chunks_500` | 203 | 5 | 66.7% | 0.233 | 53.0 ms | 1494 |
| `chunks_500` | 203 | 10 | 66.7% | 0.233 | 48.6 ms | 3114 |
| `chunks_500` | 203 | 15 | 66.7% | 0.233 | 45.9 ms | 4787 |
| `chunks_500` | 203 | 20 | 66.7% | 0.233 | 45.7 ms | 6351 |
| `chunks_1000` | 109 | 1 | 0.0% | 0.000 | 44.0 ms | 262 |
| `chunks_1000` | 109 | 3 | 0.0% | 0.000 | 44.4 ms | 1087 |
| `chunks_1000` | 109 | 5 | 33.3% | 0.083 | 45.0 ms | 2174 |
| `chunks_1000` | 109 | 10 | 33.3% | 0.083 | 45.0 ms | 4685 |
| `chunks_1000` | 109 | 15 | 66.7% | 0.107 | 49.8 ms | 8485 |
| `chunks_1000` | 109 | 20 | 66.7% | 0.107 | 42.4 ms | 11513 |
| `chunks_1500` | 71 | 1 | 0.0% | 0.000 | 49.0 ms | 275 |
| `chunks_1500` | 71 | 3 | 0.0% | 0.000 | 43.8 ms | 1388 |
| `chunks_1500` | 71 | 5 | 66.7% | 0.150 | 44.9 ms | 3639 |
| `chunks_1500` | 71 | 10 | 66.7% | 0.150 | 45.8 ms | 8032 |
| `chunks_1500` | 71 | 15 | 66.7% | 0.150 | 41.8 ms | 14214 |
| `chunks_1500` | 71 | 20 | 66.7% | 0.150 | 46.4 ms | 20321 |

### Kandidat Terbaik

| Peringkat | Konfigurasi | Hit Rate | MRR | Avg Context Chars | Alasan |
| ---: | --- | ---: | ---: | ---: | --- |
| `1` | `chunks_500`, `Top-K=5` | `66.7%` | `0.233` | `1494` | Hit rate maksimum, MRR tertinggi, konteks masih paling hemat di antara konfigurasi maksimum |
| `2` | `chunks_1500`, `Top-K=5` | `66.7%` | `0.150` | `3639` | Hit rate sama, tetapi konteks lebih panjang dan MRR lebih rendah |
| `3` | `chunks_1000`, `Top-K=15` | `66.7%` | `0.107` | `8485` | Hit rate sama, tetapi jawaban muncul lebih rendah dan konteks jauh lebih besar |

### Kesimpulan Optimal Sementara

```text
Konfigurasi optimal sementara:
- Embedding model: sentence-transformers/all-MiniLM-L6-v2
- Chunk size: 500
- Chunk overlap: 100
- Collection: chunks_500
- Top-K: 5
```

Alasan:

1. `chunks_500 + Top-K=5` mencapai hit rate tertinggi, yaitu `66.7%`.
2. MRR paling tinggi, yaitu `0.233`, artinya chunk jawaban muncul lebih dekat ke ranking atas.
3. Menambah Top-K ke `10`, `15`, atau `20` tidak menaikkan hit rate maupun MRR.
4. Konteks `Top-K=5` jauh lebih hemat dibanding Top-K lebih besar.

Catatan batasan:

1. Query `q1` tentang kontribusi utama belum berhasil pada semua konfigurasi.
2. Jumlah query uji masih sedikit, yaitu `3`.
3. `expected_terms` masih perlu dibuat lebih spesifik agar penilaian lebih kuat.

Kesimpulan ini valid untuk data uji saat ini. Untuk klaim yang lebih kuat, tambahkan minimal `5-10` query uji dengan `expected_terms` yang benar-benar spesifik dari isi paper.

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
