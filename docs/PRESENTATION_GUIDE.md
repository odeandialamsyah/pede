# Panduan Presentasi PEDE dan Benchmark Chunk

Dokumen ini dibuat sebagai bahan bantu presentasi. Isinya menjelaskan project PEDE, alur sistem, eksperimen benchmark chunk, hasil yang diperoleh, serta istilah-istilah penting yang mungkin ditanyakan saat presentasi.

## 1. Ringkasan Project

PEDE adalah project RAG sederhana untuk mengubah artikel ilmiah PDF menjadi data vektor yang bisa dicari secara semantik.

Alur utamanya:

```text
PDF -> Markdown -> Metadata -> Chunking -> Embedding Transformer -> Qdrant -> Search/RAG
```

Penjelasan singkat:

| Tahap | Penjelasan |
| --- | --- |
| PDF | Artikel ilmiah dalam bentuk file PDF |
| Markdown | PDF dikonversi menjadi teks Markdown agar struktur heading dan isi lebih mudah diproses |
| Metadata | Sistem mengambil judul, author, DOI, jumlah halaman, dan informasi artikel lainnya |
| Chunking | Teks panjang dipecah menjadi potongan kecil yang disebut chunk |
| Embedding Transformer | Setiap chunk diubah menjadi vektor angka menggunakan model Transformer |
| Qdrant | Database vektor untuk menyimpan dan mencari chunk yang paling relevan |
| Search/RAG | Query pengguna dicari ke Qdrant, lalu hasilnya bisa dipakai sebagai konteks untuk LLM |

Kalimat presentasi:

```text
Project ini bertujuan membuat dokumen PDF ilmiah bisa dicari berdasarkan makna, bukan hanya berdasarkan kata kunci.
```

## 2. Masalah yang Ingin Diselesaikan

PDF artikel ilmiah biasanya panjang, padat, dan sulit dicari secara manual. Jika langsung diberikan ke LLM, konteks bisa terlalu panjang dan tidak efisien.

Karena itu, dokumen perlu:

1. Diubah menjadi teks.
2. Dipecah menjadi chunk.
3. Diubah menjadi embedding.
4. Disimpan ke vector database.
5. Dicari berdasarkan pertanyaan pengguna.

Tujuan benchmark adalah mencari konfigurasi chunk yang paling baik agar retrieval menemukan bagian dokumen yang benar.

## 3. Fokus Eksperimen

Eksperimen ini tidak menguji Gemini terlebih dahulu. Eksperimen hanya menguji kualitas retrieval menggunakan embedding Transformer.

Alur benchmark:

```text
Query -> Embedding Transformer -> Qdrant Search -> Evaluasi Hit Rate/MRR/Latency
```

Kenapa Gemini tidak dipakai dulu?

Karena jika retrieval belum bagus, jawaban LLM juga akan buruk. Jadi kualitas retrieval harus dibuktikan terlebih dahulu.

Kalimat presentasi:

```text
Saya memisahkan evaluasi retrieval dan evaluasi LLM agar hasil eksperimen lebih jelas. Pada tahap ini yang diuji adalah apakah sistem bisa menemukan chunk yang benar.
```

## 4. Konfigurasi Benchmark

Model embedding yang digunakan:

```text
sentence-transformers/all-MiniLM-L6-v2
```

Alasan memakai satu model saja:

1. Agar eksperimen adil.
2. Variabel yang diuji hanya chunk size dan Top-K.
3. Jika model embedding ikut diganti, hasil sulit dianalisis.

Collection yang diuji:

| Collection | Chunk Size | Overlap | Total Chunk |
| --- | ---: | ---: | ---: |
| `chunks_500` | `500` | `100` | `203` |
| `chunks_1000` | `1000` | `200` | `109` |
| `chunks_1500` | `1500` | `300` | `71` |

Top-K yang diuji:

```text
1, 3, 5, 10, 15, 20
```

Top-K berarti jumlah chunk teratas yang diambil dari Qdrant.

## 5. Metrik Evaluasi

| Metrik | Arti | Semakin Baik Jika |
| --- | --- | --- |
| Hit Rate | Persentase query yang berhasil menemukan chunk berisi jawaban | Nilainya semakin tinggi |
| MRR | Mengukur seberapa tinggi ranking chunk jawaban | Mendekati 1 |
| Avg Latency | Rata-rata waktu pencarian | Semakin rendah |
| Avg Context Chars | Panjang konteks yang akan dikirim ke LLM | Secukupnya, tidak terlalu besar |

Penjelasan sederhana:

```text
Hit Rate menjawab pertanyaan: apakah jawaban ditemukan?
MRR menjawab pertanyaan: seberapa cepat jawaban muncul di ranking atas?
Latency menjawab pertanyaan: seberapa cepat sistem mencari?
Context Chars menjawab pertanyaan: seberapa besar konteks yang harus dikirim ke LLM?
```

## 6. Hasil Utama Benchmark

Tabel ringkas kandidat terbaik:

| Peringkat | Konfigurasi | Hit Rate | MRR | Avg Context Chars | Kesimpulan |
| ---: | --- | ---: | ---: | ---: | --- |
| `1` | `chunks_500`, `Top-K=5` | `66.7%` | `0.233` | `1494` | Terbaik sementara |
| `2` | `chunks_1500`, `Top-K=5` | `66.7%` | `0.150` | `3639` | Hit rate sama, tapi konteks lebih besar |
| `3` | `chunks_1000`, `Top-K=15` | `66.7%` | `0.107` | `8485` | Butuh Top-K besar dan konteks jauh lebih panjang |

Konfigurasi optimal sementara:

```text
Chunk size: 500
Chunk overlap: 100
Top-K: 5
Collection: chunks_500
Embedding model: sentence-transformers/all-MiniLM-L6-v2
```

## 7. Kenapa `chunks_500 + Top-K=5` Dipilih?

Konfigurasi ini dipilih karena:

1. Mencapai Hit Rate tertinggi, yaitu `66.7%`.
2. Memiliki MRR tertinggi, yaitu `0.233`.
3. Menggunakan konteks lebih kecil dibanding konfigurasi lain yang hit rate-nya sama.
4. Menambah Top-K ke `10`, `15`, atau `20` tidak meningkatkan Hit Rate.

Kalimat presentasi:

```text
Konfigurasi chunks_500 dengan Top-K 5 menjadi pilihan terbaik karena sudah mencapai akurasi retrieval tertinggi, tetapi tetap hemat konteks. Menambah jumlah chunk tidak meningkatkan hasil, hanya menambah panjang konteks.
```

## 8. Interpretasi Hasil

Hasil menunjukkan bahwa chunk yang lebih kecil cenderung lebih spesifik.

Pada `chunks_500`, sistem lebih cepat menemukan bagian yang relevan karena setiap chunk memuat informasi yang lebih fokus.

Namun chunk terlalu kecil juga bisa membuat jumlah data di database lebih banyak. Karena itu, perlu dicari titik seimbang.

Pada eksperimen ini, titik seimbangnya adalah:

```text
Chunk size 500 + Top-K 5
```

## 9. Batasan Eksperimen

Eksperimen ini masih memiliki beberapa batasan:

1. Query uji baru berjumlah `3`.
2. Dokumen uji baru satu paper.
3. Query `q1` tentang kontribusi utama belum berhasil ditemukan di semua konfigurasi.
4. Model embedding yang diuji baru satu model.
5. Evaluasi masih berbasis expected terms, belum evaluasi manual penuh.

Kalimat presentasi:

```text
Hasil ini adalah optimal sementara untuk data uji saat ini. Untuk generalisasi yang lebih kuat, perlu ditambah jumlah paper, jumlah query, dan variasi model embedding.
```

## 10. Pertanyaan yang Mungkin Ditanyakan

### Apa itu RAG?

RAG adalah singkatan dari Retrieval-Augmented Generation. Artinya, LLM tidak menjawab hanya dari pengetahuan internalnya, tetapi dibantu dengan dokumen yang diambil dari database.

Jawaban singkat:

```text
RAG adalah metode yang mengambil konteks relevan dari dokumen, lalu konteks itu digunakan LLM untuk menjawab pertanyaan.
```

### Apa itu chunk?

Chunk adalah potongan kecil dari dokumen panjang.

Jawaban singkat:

```text
Chunk adalah bagian teks yang lebih kecil agar dokumen panjang bisa dicari dan diproses lebih efisien.
```

### Kenapa dokumen harus dipecah menjadi chunk?

Karena dokumen PDF terlalu panjang untuk langsung dicari atau dikirim seluruhnya ke LLM. Dengan chunk, sistem bisa mengambil hanya bagian yang relevan.

### Apa itu embedding?

Embedding adalah representasi teks dalam bentuk vektor angka.

Jawaban singkat:

```text
Embedding mengubah teks menjadi angka agar komputer bisa membandingkan kemiripan maknanya.
```

### Apa itu Transformer?

Transformer adalah arsitektur model deep learning yang banyak digunakan untuk pemrosesan bahasa alami.

Dalam project ini, Transformer digunakan untuk membuat embedding dari teks.

### Apa itu Qdrant?

Qdrant adalah vector database. Fungsinya menyimpan embedding dan mencari vektor yang paling mirip dengan query.

### Apa itu Top-K?

Top-K adalah jumlah hasil teratas yang diambil dari vector database.

Contoh:

```text
Top-K=5 berarti sistem mengambil 5 chunk paling relevan.
```

### Apa itu Hit Rate?

Hit Rate adalah persentase keberhasilan sistem menemukan chunk yang mengandung jawaban.

Contoh:

```text
Jika 2 dari 3 query berhasil, Hit Rate = 66.7%.
```

### Apa itu MRR?

MRR atau Mean Reciprocal Rank mengukur posisi ranking jawaban benar.

Jika jawaban muncul di ranking 1, nilainya tinggi. Jika muncul di ranking bawah, nilainya lebih rendah.

Jawaban singkat:

```text
MRR mengukur apakah jawaban ditemukan di ranking atas atau tidak.
```

### Kenapa tidak langsung pakai Gemini?

Karena Gemini membutuhkan konteks yang benar. Jika retrieval salah, jawaban Gemini juga bisa salah atau tidak lengkap.

Jawaban singkat:

```text
Saya menguji retrieval dulu agar bisa memastikan konteks yang dikirim ke Gemini sudah relevan.
```

### Kenapa memakai MiniLM?

MiniLM dipakai karena ringan, cepat, dan cukup baik sebagai baseline embedding Transformer.

Jawaban singkat:

```text
MiniLM digunakan sebagai baseline karena cepat dan cocok untuk eksperimen awal di lokal.
```

### Kenapa tidak membandingkan BGE-M3 atau model embedding lain?

Karena fokus eksperimen saat ini adalah chunking. Jika model embedding ikut diganti, hasil eksperimen sulit dianalisis.

Jawaban singkat:

```text
Model embedding dibuat tetap agar pengaruh chunk size dan Top-K bisa terlihat jelas.
```

### Kenapa chunk size 500 lebih baik?

Karena pada data uji ini, chunk size 500 menghasilkan potongan teks yang lebih fokus. Dengan Top-K 5, sistem dapat menemukan jawaban lebih cepat dan dengan konteks yang lebih kecil.

### Kenapa Top-K 20 tidak dipilih padahal mengambil lebih banyak chunk?

Karena Top-K 20 tidak meningkatkan Hit Rate atau MRR dibanding Top-K 5. Top-K 20 hanya menambah panjang konteks.

Jawaban singkat:

```text
Top-K 20 tidak dipilih karena hasilnya tidak lebih akurat, tetapi konteksnya jauh lebih besar.
```

### Apa maksud optimal sementara?

Optimal sementara berarti konfigurasi terbaik berdasarkan data uji yang tersedia saat ini. Hasil bisa berubah jika jumlah paper, query, atau model embedding ditambah.

## 11. Narasi Presentasi Singkat

Gunakan narasi ini jika ingin menjelaskan dengan alur cepat:

```text
Project ini mengubah PDF artikel ilmiah menjadi embedding yang disimpan di Qdrant. Tujuannya agar artikel bisa dicari berdasarkan makna. Saya melakukan benchmark untuk mencari konfigurasi chunk terbaik sebelum memakai LLM.

Eksperimen dilakukan dengan satu model embedding, yaitu all-MiniLM-L6-v2, agar hasilnya adil. Saya membandingkan chunk size 500, 1000, dan 1500, lalu menguji Top-K 1 sampai 20.

Hasil terbaik sementara adalah chunk size 500 dengan Top-K 5. Konfigurasi ini mencapai Hit Rate 66.7%, MRR 0.233, dan konteks rata-rata 1494 karakter. Top-K yang lebih besar tidak meningkatkan akurasi, sehingga Top-K 5 lebih efisien.

Kesimpulannya, untuk data uji saat ini, chunk yang lebih kecil dan Top-K sedang memberikan hasil retrieval yang paling seimbang.
```

## 12. Slide yang Disarankan

| Slide | Isi |
| ---: | --- |
| 1 | Judul project dan tujuan |
| 2 | Masalah: PDF ilmiah sulit dicari secara semantik |
| 3 | Alur sistem PEDE |
| 4 | Penjelasan chunking dan embedding |
| 5 | Desain benchmark |
| 6 | Metrik evaluasi |
| 7 | Tabel hasil benchmark |
| 8 | Konfigurasi optimal sementara |
| 9 | Batasan eksperimen |
| 10 | Kesimpulan dan pengembangan selanjutnya |

## 13. Pengembangan Selanjutnya

Beberapa pengembangan yang bisa dilakukan:

1. Menambah jumlah query uji menjadi 10-20.
2. Menambah jumlah paper.
3. Membandingkan model embedding lain seperti BGE-M3.
4. Mengevaluasi jawaban akhir dengan Gemini.
5. Membersihkan noise dari hasil konversi PDF.
6. Menambahkan evaluasi manual oleh manusia.

