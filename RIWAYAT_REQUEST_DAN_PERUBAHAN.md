# 📜 DOKUMENTASI RIWAYAT REQUEST & IMPLEMENTASI PERUBAHAN
## Proyek: Guppy — Clinical Pharmacy & Fornas 2025 Helper
**Mata Kuliah:** Aplikasi AI dalam Industri Farmasi (Program Magister Farmasi)  
**Pengembang:** Apt. Indira Nureva, S.Farm.  
**Platform AI:** Google Antigravity (Gemini 3.8 Flash High)  
**Repositori GitHub:** [`https://github.com/Indiranureva/Guppy_Clinical-Pharmacy-Fornas-2025-Helper.git`](https://github.com/Indiranureva/Guppy_Clinical-Pharmacy-Fornas-2025-Helper.git)  
**Tanggal Pencatatan:** 23 Oktober 2026  

---

## 📌 Daftar Isi
1. [Ringkasan Eksekutif](#1-ringkasan-eksekutif)
2. [Siklus 1: Penghubungan Repositori & Sinkronisasi Git CLI](#2-siklus-1-penghubungan-repositori--sinkronisasi-git-cli)
3. [Siklus 2: Verifikasi & Pengunggahan Rantai Progress Sebelumnya](#3-siklus-2-verifikasi--pengunggahan-rantai-progress-sebelumnya)
4. [Siklus 3: Analisis Komparatif Desain Fitur Justifikasi Literatur Klinis (Q1–Q3)](#4-siklus-3-analisis-komparatif-desain-fitur-justifikasi-literatur-klinis-q1q3)
5. [Siklus 4: Implementasi Kurasi Rutin Multi-Artikel & Generator Memo KFT](#5-siklus-4-implementasi-kurasi-rutin-multi-artikel--generator-memo-kft)
6. [Siklus 5: Investigasi Kendala Pencarian Obat pada Kasus Klinis](#6-siklus-5-investigasi-kendala-pencarian-obat-pada-kasus-klinis)
7. [Siklus 6: Implementasi Deep Search, Kamus Sinonim Bilingual & Smart Fallback](#7-siklus-6-implementasi-deep-search-kamus-sinonim-bilingual--smart-fallback)
8. [Siklus 7: Transformasi Format Unduhan Memo Justifikasi KFT ke Dokumen Microsoft Word (.docx)](#8-siklus-7-transformasi-format-unduhan-memo-justifikasi-kft-ke-dokumen-microsoft-word-docx)
9. [Matriks Commit Git & Status Validasi Unit Test](#9-matriks-commit-git--status-validasi-unit-test)

---

## 1. Ringkasan Eksekutif
Dokumen ini mencatat secara kronologis seluruh instruksi (*prompt/request*) yang diberikan oleh Pengguna (*User*) dan respons tindakan teknis, analisis farmasi klinis, serta perubahan kode yang dieksekusi oleh Agen AI (*Antigravity*) selama pengembangan lanjutan aplikasi **Guppy Clinical Pharmacy & Fornas 2025 Helper**.

Aplikasi Guppy dirancang untuk membantu apoteker klinis dan dokter di faskes (FKTP dan FKRTL) dalam:
- Menguji kesesuaian resep obat terhadap Kepmenkes RI No. HK.01.07/MENKES/1199/2025 (Fornas 2025).
- Menilai rasionalitas terapi menggunakan 9 Pedoman Nasional Pelayanan Kedokteran (PNPK 2025) resmi Kementerian Kesehatan RI.
- Menyusun **Memo Justifikasi Klinis** berbasis bukti ilmiah terindeks Scopus Q1–Q3 yang audit-ready untuk Komite Farmasi & Terapi (KFT) dan BPJS Kesehatan.

---

## 2. Siklus 1: Penghubungan Repositori & Sinkronisasi Git CLI

### 🗣️ Request Pengguna:
> *"hubungkan progress yang akan dilakukan dengan github"*

### 🔍 Analisis & Tindakan Teknis:
1. **Deteksi Lingkungan Git**:
   - Perintah `git` awalnya tidak dikenali langsung di shell PowerShell sistem karena binary Git berada di direktori aplikasi GitHub Desktop (`%LOCALAPPDATA%\GitHubDesktop\app-3.6.7\resources\app\git\cmd\git.exe`).
   - Dibuatkan wrapper `git.bat` di dalam path `%LOCALAPPDATA%\GitHubDesktop\bin\git.bat` sehingga perintah `git` aktif secara native di semua terminal.
2. **Pemeriksaan Status Remote Git**:
   - Remote URL terverifikasi ke: `https://github.com/Indiranureva/Guppy_Clinical-Pharmacy-Fornas-2025-Helper.git` pada branch `main`.
3. **Penyimpanan Perubahan Kerja**:
   - Perubahan pada `guppy/backend/config.py` (kamus diagnosis ICD-10 PNPK 2025) dan `guppy/frontend/app.py` (fitur edukasi matching diagnosis) di-stage dan di-commit.
   - **Commit Hash**: `a3ccc48`
   - **Pesan Commit**: `feat(ui): Integrasi edukasi klinis matching diagnosis ICD-10 dan detail obat Fornas/PNPK 2025`
4. **Otentikasi & Peluncuran GitHub Desktop**:
   - Membuka aplikasi GitHub Desktop secara otomatis agar pengguna dapat mengunggah progress melalui akun `Indiranureva` tanpa perlu input token manual di terminal.

---

## 3. Siklus 2: Verifikasi & Pengunggahan Rantai Progress Sebelumnya

### 🗣️ Request Pengguna:
> *"apakah progress sebelumnya bisa di upload juga?"*

### 🔍 Analisis & Tindakan Teknis:
1. **Penjelasan Mekanisme Git**:
   - Menjelaskan kepada pengguna bahwa Git bekerja secara **kumulatif / berantai**. Begitu tombol *Push* diklik, seluruh rantai commit lokal yang belum ada di remote GitHub akan otomatis terunggah bersamaan.
2. **Daftar Commit yang Terunggah Sekaligus**:
   - `78a3dda`: *Integrasi PNPK 2025 Kemenkes RI ke dalam Basis Hukum, Penelusuran Obat, dan Evaluasi Resep*.
   - `f4dbadb`: *Implementasi parameter proteksi lampu keamanan (Hijau, Orange, Merah) pada informasi sistem Guppy*.
   - `a3ccc48`: *Integrasi edukasi klinis matching diagnosis ICD-10 dan detail obat Fornas/PNPK 2025*.
   - Seluruh berkas presentasi PPTX, pedoman PDF, dan skrip unit testing ikut tersinkronkan ke repositori.
3. **Hasil**: Pengguna berhasil melakukan push 3 commit tersebut ke GitHub.

---

## 4. Siklus 3: Analisis Komparatif Desain Fitur Justifikasi Literatur Klinis (Q1–Q3)

### 🗣️ Request Pengguna:
> *"Pada fitur Justifikasi Literatur Klinis Berbasis Bukti (Q1-Q3) kamu menyediakan literatur yang sudah di download dan siap pakai. Pilihlah perubahan yang paling possible untuk kamu lakukan dari pilihan : mengubah bentuk artikel tersebut menjadi bentuk pencarian secara realtime atau memilihkan beberapa artikel (pilihan rutin di update oleh Guppy) untuk kemudian dipilih lagi oleh pengguna. Jangan proses dulu, pilih dulu dan berikan alasana atas pemilihan kamu"*

### 🔍 Analisis & Komparasi Klinis/Teknis:
Agen membandingkan dua pendekatan:
- **Opsi 1: Pencarian Realtime Bebas (Live Search via PubMed/Crossref API)**
  - *Kelemahan*: Ketergantungan mutlak internet faskes (sering firewall ketat), latensi tinggi (15-30 detik), API rate limits, dan tidak adanya metadata kuartil Scopus (Q1–Q3) pada raw search PubMed, serta risiko halusinasi interpretasi klinis.
- **Opsi 2: Kurasi Rutin Guppy dengan Seleksi Fleksibel Pengguna (*Curated Pre-selection with Interactive User Multi-Picker*)**
  - *Keunggulan*: 100% stabil offline/intranet, latensi nol, artikel terverifikasi Scopus Q1–Q3, dilengkapi implikasi spesifik Fornas 2025, dan apoteker tetap memegang kendali penuh (*human-in-the-loop*) dalam memilih artikel yang paling representatif untuk pasiennya.
- **Keputusan**: Agen memilih **Opsi 2** dan menyampaikan argumentasi lengkap tanpa memodifikasi kode terlebih dahulu, sesuai instruksi pengguna.

---

## 5. Siklus 4: Implementasi Kurasi Rutin Multi-Artikel & Generator Memo KFT

### 🗣️ Request Pengguna:
> *"aku setuju, lanjutkan"*

### 🔍 Analisis & Tindakan Teknis:
1. **Pengembangan Mesin `ClinicalLiteratureScout` (`guppy/backend/engine/clinical_literature.py`)**:
   - Mengembangkan 10 topik kasus klinis prioritas rumah sakit (Endokrin, Ginjal, Kardiovaskular, Geriatri, Gastroenterologi, Nyeri, Infeksi & PPAB).
   - Menghadirkan **25 artikel Scopus Q1–Q3 terverifikasi** (The Lancet, NEJM, JAMA, Diabetes Care, Kidney International, European Heart Journal, Thorax, dll.).
   - Setiap topik memuat klasifikasi:
     - ⭐ **Rekomendasi Utama Guppy** (*Primary Recommendation*): Studi/meta-analisis dengan tingkat bukti tertinggi.
     - 📑 **Studi Pendukung / Konsensus**: Bukti pembanding/guideline (KDIGO, ADA, ESC, AGA).
   - Membuat metode `generate_justification_memo(...)` untuk menyusun naskah Markdown resmi memo justifikasi KFT & BPJS.
2. **Pengembangan Antarmuka Tab 4 Streamlit (`guppy/frontend/app.py`)**:
   - Dropdown seleksi kasus klinis berbasis kategori.
   - Kotak centang (*checkbox*) interaktif per artikel sehingga klinisi dapat memilih artikel yang relevan.
   - Expander rincian makalah (DOI, PMID, metodologi, temuan kunci, dan implikasi Fornas).
   - Formulir personalisasi data pasien (Nama Pasien, No. RM, DPJP, Ruang Rawat, Nama Apoteker, No. SIPA, Catatan PTO).
   - Pratinjau langsung naskah memo dan tombol unduh satu-klik: `⬇️ Unduh Dokumen Memo Justifikasi KFT`.
3. **Pengujian & Git Commit**:
   - Membuat berkas tes `tests/test_clinical_literature.py` (35 unit test lulus 100%).
   - **Commit Hash**: `0500a13`
   - **Pesan Commit**: `feat(literature): Implementasi kurasi rutin multi-artikel Q1-Q3, seleksi interaktif klinisi, dan generator memo justifikasi KFT`

---

## 6. Siklus 5: Investigasi Kendala Pencarian Obat pada Kasus Klinis

### 🗣️ Request Pengguna:
> *"ada beberapa obat ketika di input, dianggap tidak memiliki topik klinis yang cocok, kenapa?"*

### 🔍 Analisis Diagnostik Masalah:
Agen mengidentifikasi 4 faktor penyebab:
1. **Perbedaan Ruang Lingkup (Scope Kurasi vs Database 1.100+ Fornas)**:
   - Tab 1 & Tab 2 memuat seluruh 1.100+ sediaan obat Fornas 2025.
   - Tab 4 adalah fitur kurasi kasus kontroversial/berisiko tinggi (evidence-based justification). Obat rutin tanpa restriksi rumit (misal: Parasetamol, Oralit) memang belum memiliki kartu telaah jurnal Q1–Q3.
2. **Variasi Ejaan Bahasa Indonesia vs Standar Internasional (INN)**:
   - Pengguna mengetik ejaan Indonesia (*Seftriakson*, *Amoksisilin*, *Kandesartan*, *Lansoprazol*), sedangkan entri memakai INN (*Ceftriaxone*, *Amoxicillin*, *Candesartan*, *Lansoprazole*).
3. **Pencarian Dangkal (*Shallow Search*)**:
   - Mesin pencari awal hanya mencocokkan judul topik dan kata kunci utama, belum membaca teks artikel (nama obat pembanding seperti *Gliclazide* di GUIDE study atau *Spironolactone* di RALES trial tidak terindeks).
4. **Obat Belum Masuk Rilis Kurasi Saat Ini**:
   - Obat spesifik seperti agen antiplatelet DAPT atau kortikosteroid belum memiliki topik tersendiri.

---

## 7. Siklus 6: Implementasi Deep Search, Kamus Sinonim Bilingual & Smart Fallback

### 🗣️ Request Pengguna:
> *"terapkan"*

### 🔍 Analisis & Tindakan Teknis:
1. **Kamus Sinonim Bilingual Terintegrasi (`DRUG_SYNONYMS`)**:
   - Menambahkan pemetaan otomatis ejaan bahasa Indonesia, ejaan internasional (INN), dan merek dagang populer ke dalam `ClinicalLiteratureScout`:
     - `seftriakson` $\leftrightarrow$ `ceftriaxone` (Rocephin)
     - `kandesartan` $\leftrightarrow$ `candesartan` (Blopress)
     - `klopidogrel` $\leftrightarrow$ `clopidogrel` (Plavix)
     - `metilprednisolon` $\leftrightarrow$ `methylprednisolone` (Medixon)
     - `deksametason` $\leftrightarrow$ `dexamethasone` (Kalmethasone)
     - `setirizin` $\leftrightarrow$ `cetirizine` (Incidal)
     - `spironolakton` $\leftrightarrow$ `spironolactone` (Aldactone)
     - `gliklazid / glimepirid` $\leftrightarrow$ `gliclazide / glimepiride` (Diamicron / Amaryl)
     - `lansoprazol / omeprazol` $\leftrightarrow$ `lansoprazole / omeprazole` (Prosogan / Losec)
     - dan puluhan obat esensial lainnya.
2. **Mesin Deep Search (Pencarian Mendalam)**:
   - Memperluas algoritma `search_curated_topics` agar mencari ke seluruh metadata, sinonim, judul artikel, nama penulis, jurnal, teks temuan klinis, dan implikasi Fornas.
3. **Penambahan Topik Kasus Klinis Baru**:
   - **Dual Antiplatelet (DAPT) / Clopidogrel + Aspirin** pasca-PCI & ACS *(CURE Trial & ESC Guidelines)*.
   - **Protokol Tapering Off Kortikosteroid Sistemik (Metilprednisolon / Deksametason)** *(RECOVERY Trial & Endocrine Guidelines)*.
   - **Substitusi ARB (Kandesartan / Valsartan)** pada Pasien Intoleran Batuk Kering ACE-Inhibitor *(CHARM Alternative & PNPK Hipertensi Kemenkes)*.
4. **Smart Universal Justification Generator**:
   - Jika obat yang dicari belum ada artikel kurasi spesifiknya:
     - Sistem otomatis mencari obat ke **database 1.100+ obat Fornas 2025** via `FornasMatcher`.
     - Menampilkan kelas terapi resmi, tingkat faskes (FPKTP/FPKTL), dan batas peresepan maksimal.
     - Menyediakan pilihan kategori justifikasi standar (Gawat Darurat, Lini 1 Gagal, Komorbiditas Khusus, Efek Samping Berat, Stok Kosong, Dosis Ginjal/Hati, atau Obat Non-Formularium).
     - Menghasilkan dokumen **Memo Justifikasi KFT Mandiri** resmi yang dapat diunduh seketika.
5. **Pengujian & Git Commit**:
   - Menambahkan pengujian sinonim bilingual dan universal memo di `tests/test_clinical_literature.py` (seluruh 37 unit test lulus 100%).
   - **Commit Hash**: `e75f6b8`
   - **Pesan Commit**: `feat(search): Implementasi Deep Search literatur, kamus sinonim bilingual, dan Smart Universal Justification KFT`

---

## 8. Siklus 7: Transformasi Format Unduhan Memo Justifikasi KFT ke Dokumen Microsoft Word (.docx)

### 🗣️ Request Pengguna:
> *"ubah bentuk dokumen memo justifikasi yang diperoleh dari proses menjadi bentuk word ketika di download"*

### 🔍 Analisis & Tindakan Teknis:
1. **Analisis Kebutuhan Tata Kelola Dokumen Rumah Sakit**:
   - Di instalasi farmasi rumah sakit dan Komite Farmasi & Terapi (KFT), dokumen pertanggungjawaban resmi memerlukan format **Microsoft Word (.docx)** agar dapat:
     - Disesuaikan dengan kop surat resmi rumah sakit masing-masing.
     - Diedit nomor surat/agenda farmasi secara mudah oleh apoteker.
     - Diberi paraf, tanda tangan basah, maupun stempel basah instalasi farmasi/KFT sebelum diserahkan ke verifikator BPJS Kesehatan.
2. **Pengembangan Modul Generator Word (`guppy/backend/engine/docx_generator.py`)**:
   - Mengintegrasikan pustaka `python-docx` (v1.2.0) untuk merakit berkas `.docx` secara in-memory (`io.BytesIO`).
   - Menyusun tata letak (*layout*) berstandar akreditasi rumah sakit:
     - **Header & Tipografi**: Font Calibri 10.5pt, judul utama *Deep Navy* (`#1A365D`), spasi margin standar 1 inci (2.54 cm).
     - **Tabel Data Pasien & Terapi**: Tabel dengan garis pembatas abu-abu rapi dan cell padding terstandar.
     - **Kotak Bukti Ilmiah Berwarna**:
       - Kotak mint hijau (`#F0FDF4`) untuk temuan klinis ilmiah.
       - Kotak amber hangat (`#FFFBEB`) untuk implikasi klinis terhadap restriksi Fornas 2025.
     - **Lembar Pengesahan Tiga Pihak**: Tabel tanda tangan untuk Apoteker Pengkaji (dengan No. SIPA), DPJP (Dokter Penulis Resep), dan Ketua KFT / Direktur RS.
3. **Integrasi Antarmuka Pengunduhan Streamlit (`guppy/frontend/app.py`)**:
   - Mengganti seluruh tombol unduhan di Tab 4:
     - `⬇️ Unduh Dokumen Memo Justifikasi KFT (.docx / Microsoft Word) — [Nama Obat]`
     - MIME type: `application/vnd.openxmlformats-officedocument.wordprocessingml.document`.
     - Nama berkas berekstensi `.docx`.
4. **Pembaruan Pengujian & Dependensi**:
   - Menambahkan pengujian `test_generate_justification_memo_docx` dan `test_generate_universal_justification_memo_docx` di `tests/test_clinical_literature.py` (memvalidasi magic bytes ZIP/DOCX `PK\x03\x04`).
   - Mendaftarkan `python-docx>=1.1.0` ke dalam `requirements.txt`.
   - Seluruh **39 unit test lulus 100%**.

---

## 9. Matriks Commit Git & Status Validasi Unit Test

| Hash Commit | Kategori | Komponen Berkas | Ringkasan Modifikasi |
| :--- | :--- | :--- | :--- |
| `78a3dda` | `feat` | `guppy/backend/engine/` | Integrasi 9 dokumen PNPK 2025 Kemenkes ke basis hukum & evaluasi resep |
| `f4dbadb` | `feat` | `guppy/backend/`, `guppy/frontend/` | Proteksi lampu indikator keamanan klinis sistem (Hijau, Orange, Merah) |
| `a3ccc48` | `feat(ui)` | `config.py`, `app.py` | Edukasi pencocokan diagnosis ICD-10 & expander obat Fornas/PNPK 2025 |
| `0500a13` | `feat(lit)` | `clinical_literature.py`, `app.py`, `test_clinical_literature.py` | Kurasi multi-artikel Scopus Q1-Q3 & generator memo justifikasi KFT |
| `e75f6b8` | `feat(search)` | `clinical_literature.py`, `app.py`, `test_clinical_literature.py` | Deep Search, kamus sinonim bilingual, & Smart Universal Justification |
| `a231f1b` | `docs` | `RIWAYAT_REQUEST_DAN_PERUBAHAN.md` | Dokumentasi komprehensif riwayat request pengguna & implementasi AI |
| `(terbaru)` | `feat(export)` | `docx_generator.py`, `clinical_literature.py`, `app.py`, `requirements.txt` | Transformasi unduhan memo justifikasi KFT ke format Microsoft Word (.docx) |

### Status Verifikasi Pengujian (Pytest):
```text
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0
rootdir: Guppy_Clinical Pharmacy & Fornas 2025 Helper
collected 39 items

tests\test_classifier.py ...                                             [  7%]
tests\test_clinical_literature.py .........                              [ 30%]
tests\test_fornas_matcher.py .........                                   [ 53%]
tests\test_gap_analyzer.py ..                                            [ 58%]
tests\test_roadmap.py ...                                                [ 66%]
tests\test_security.py .............                                     [100%]

============================= 39 passed in 2.54s ==============================
```

---
*Dokumen ini merupakan rekaman resmi proses rekayasa perangkat lunak farmasi klinis dan integrasi kecerdasan buatan pada aplikasi Guppy Clinical Pharmacy & Fornas 2025 Helper.*
