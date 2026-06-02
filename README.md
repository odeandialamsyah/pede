# PEDE - PDF to Model Embedding

PEDE adalah project RAG sederhana untuk mengubah artikel ilmiah PDF menjadi vector embedding yang bisa dicari secara semantik. Project ini cocok untuk eksperimen pencarian dokumen ilmiah, chatbot berbasis jurnal, atau backend retrieval untuk aplikasi AI.

Alur utama:

```text
PDF -> Markdown -> Metadata -> Chunking -> Embedding Transformer -> Qdrant -> Search/API/RAG
```

## Fungsi Project

Project ini melakukan beberapa tahap:

1. Mengubah PDF menjadi Markdown menggunakan `pymupdf4llm`.
2. Mengambil metadata artikel seperti judul, author, DOI, abstract, jumlah halaman, dan jurnal.
3. Memecah isi artikel menjadi chunk berdasarkan heading Markdown dan ukuran teks.
4. Membuat embedding menggunakan model Transformer `sentence-transformers/all-MiniLM-L6-v2`.
5. Menyimpan embedding dan metadata ke Qdrant.
6. Menyediakan pencarian semantik melalui CLI atau REST API FastAPI.
7. Menyediakan contoh RAG dengan Gemini melalui `testrag.py`.

## Struktur File Penting

| File | Fungsi |
| --- | --- |
| `ingest.py` | Pipeline utama untuk ingest PDF ke Qdrant |
| `api.py` | Server FastAPI untuk pencarian semantik |
| `testrag.py` | Contoh RAG: ambil konteks dari Qdrant lalu kirim ke Gemini |
| `dump_chunks.py` | Ekspor chunk dari Qdrant ke JSON |
| `core/pdf_converter.py` | Konversi PDF ke Markdown |
| `core/metadata_extractor.py` | Ekstraksi metadata artikel |
| `core/chunker.py` | Pemecahan Markdown menjadi chunk |
| `core/vector_store.py` | Embedding dan operasi Qdrant |

## Model Embedding

Project ini menggunakan:

```text
sentence-transformers/all-MiniLM-L6-v2
```

Model ini berbasis Transformer, ringan, cepat, dan menghasilkan vektor berdimensi 384. Jika sebelumnya database dibuat dengan `BAAI/bge-m3`, hapus atau gunakan folder Qdrant baru karena dimensi vektor lama berbeda.

Contoh:

```powershell
Remove-Item -Recurse -Force .\qdrant_db
```

Jalankan perintah hapus database hanya jika Anda memang ingin mengulang ingest dari awal.

## Instalasi

Masuk ke folder project:

```powershell
cd d:\Kuliah\AI\pede
```

Buat virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependency:

```powershell
pip install -r requirements.txt
```

Salin konfigurasi environment:

```powershell
Copy-Item .env.example .env
```

Default project memakai Qdrant lokal:

```ini
QDRANT_PATH="./qdrant_db"
```

Jika ingin memakai Qdrant Cloud, isi:

```ini
QDRANT_URL="https://xxx.cloud.qdrant.io"
QDRANT_API_KEY="api_key_anda"
```

## Cara Mencoba

### 1. Ingest PDF

Single file:

```powershell
python ingest.py .\paper.pdf
```

Folder berisi banyak PDF:

```powershell
python ingest.py .\papers\
```

Multiple file:

```powershell
python ingest.py .\paper1.pdf .\paper2.pdf
```

Output proses ingest akan membuat:

| Folder | Isi |
| --- | --- |
| `data/markdown` | Hasil konversi PDF ke Markdown |
| `data/images` | Gambar dari PDF jika ada |
| `data/metadata` | Metadata artikel dalam JSON |
| `qdrant_db` | Database vektor lokal |

### 2. Cek Database

Lihat artikel yang sudah masuk:

```powershell
python ingest.py --list
```

Lihat statistik collection:

```powershell
python ingest.py --info
```

### 3. Tes Search dari CLI

Cari di semua artikel:

```powershell
python ingest.py --search "apa metode utama penelitian ini?"
```

Cari berdasarkan DOI:

```powershell
python ingest.py --search "apa hasil eksperimennya?" --doi "10.xxxx/xxxx"
```

### 4. Jalankan API

```powershell
python api.py
```

Buka dokumentasi interaktif:

```text
http://localhost:8000/docs
```

Endpoint utama:

| Method | URL | Fungsi |
| --- | --- | --- |
| `GET` | `/` | Health check |
| `POST` | `/search` | Pencarian semantik |

Contoh request `/search`:

```json
{
  "query": "apa kontribusi utama paper ini?",
  "limit": 5,
  "doi": "10.xxxx/xxxx"
}
```

### 5. Jalankan Contoh RAG Gemini

Set API key Gemini:

```powershell
$env:GEMINI_API_KEY="API_KEY_ANDA"
```

Edit nilai `QUERY` dan `DOI_TARGET` di `testrag.py`, lalu jalankan:

```powershell
python testrag.py
```

Script ini akan:

1. Mencari chunk relevan di Qdrant.
2. Menyusun konteks dari hasil pencarian.
3. Mengirim konteks dan pertanyaan ke Gemini.
4. Menampilkan jawaban berdasarkan isi dokumen.

## Tahapan Memahami Project

Urutan belajar yang disarankan:

1. Baca `README.md` ini untuk memahami gambaran besar.
2. Buka `ingest.py` untuk melihat pipeline utama dari PDF sampai masuk Qdrant.
3. Buka `core/pdf_converter.py` untuk memahami konversi PDF ke Markdown.
4. Buka `core/metadata_extractor.py` untuk memahami ekstraksi DOI, judul, author, dan metadata lain.
5. Buka `core/chunker.py` untuk memahami strategi pemecahan teks.
6. Buka `core/vector_store.py` untuk memahami embedding dan pencarian Qdrant.
7. Buka `api.py` untuk memahami cara project ini dipakai oleh aplikasi lain.
8. Buka `testrag.py` untuk memahami bentuk RAG sederhana.

## Catatan Penting

- Model embedding pertama kali akan diunduh dari Hugging Face jika belum ada di cache lokal.
- Jika model embedding diganti, database Qdrant lama biasanya perlu dibuat ulang karena ukuran vektor bisa berubah.
- Ekstraksi metadata akan lebih baik jika PDF memiliki DOI dan koneksi internet tersedia untuk CrossRef.
- Untuk dokumen Indonesia-Inggris campuran, model MiniLM lebih cepat tetapi tidak sekuat model multilingual besar seperti BGE-M3.

## Lisensi

GNU GPL v3
