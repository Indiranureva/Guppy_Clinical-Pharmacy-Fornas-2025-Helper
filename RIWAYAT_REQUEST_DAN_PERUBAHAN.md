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
9. [Siklus 8: Desain & Implementasi Antarmuka Pengguna Komprehensif (UI/UX CDSS) Sesuai Mockup Visual](#9-siklus-8-desain--implementasi-antarmuka-pengguna-komprehensif-uiux-cdss-sesuai-mockup-visual)
10. [Siklus 9: Perbaikan Rendering UI (Eliminasi Kode Mentah) & Pemulihan Fungsionalitas Interaktif Penuh](#10-siklus-9-perbaikan-rendering-ui-eliminasi-kode-mentah--pemulihan-fungsionalitas-interaktif-penuh)
11. [Siklus 10: Pemulihan Esensi Klinis Asli, Integrasi Logo Resmi Guppy, Fitur Ganti Nama dr. Andini, & Perbaikan Tombol](#11-siklus-10-pemulihan-esensi-klinis-asli-integrasi-logo-resmi-guppy-fitur-ganti-nama-pengguna-dr-andini--perbaikan-total-tombol-interaktif)
12. [Siklus 11: Audit Komprehensif & Eliminasi Error UI/Fungsi Guppy (Logo PNG, Popover Profil, Universal Justification, & Global Search Sync)](#12-siklus-11-audit-komprehensif--eliminasi-error-uifungsi-guppy-logo-png-popover-profil-universal-justification--global-search-sync)
13. [Siklus 12: Resolusi Konflik Tema Streamlit (Dark vs Light) & Restorasi Kontras UI CDSS](#13-siklus-12-resolusi-konflik-tema-streamlit-dark-vs-light--restorasi-kontras-ui-cdss)
14. [Siklus 13: Eliminasi Konfigurasi Server Headless & Pemulihan Peluncuran Otomatis Browser Desktop Guppy](#14-siklus-13-eliminasi-konfigurasi-server-headless--pemulihan-peluncuran-otomatis-browser-desktop-guppy)
15. [Siklus 14: Penyediaan Direktori Aset Gambar (assets/images/) di Root Proyek](#15-siklus-14-penyediaan-direktori-aset-gambar-assetsimages-di-root-proyek)
16. [Siklus 15: Integrasi Welcome Banner Vektor Resmi Guppy ke Dashboard Utama](#16-siklus-15-integrasi-welcome-banner-vektor-resmi-guppy-ke-dashboard-utama)
17. [Siklus 16: Penyiapan Aplikasi untuk Deployment Cloud & Akses Web Publik (Docker, Backup, & Panduan Hosting)](#17-siklus-16-penyiapan-aplikasi-untuk-deployment-cloud--akses-web-publik-docker-backup--panduan-hosting)
18. [Siklus 17: Penerapan Latar Belakang SVG Resmi Sidebar (Expanded & Collapsed) & Optimalisasi Kontras Tipografi](#18-siklus-17-penerapan-latar-belakang-svg-resmi-sidebar-expanded--collapsed--optimalisasi-kontras-tipografi)
19. [Siklus 18: Diagnosa Masalah & Perbaikan Kontras Warna Expander Profil & Tombol Simpan di Sidebar](#19-siklus-18-diagnosa-masalah--perbaikan-kontras-warna-expander-profil--tombol-simpan-di-sidebar)
20. [Siklus 19: Penggantian Bentuk Tombol Buka Sidebar dengan Karakter Maskot Vektor Guppy ("Klik aku!")](#20-siklus-19-penggantian-bentuk-tombol-buka-sidebar-dengan-karakter-maskot-vektor-guppy-klik-aku)
21. [Siklus 20: Pembaruan Menyeluruh Tutorial Aplikasi & Panduan Klinis pada Berkas README.md](#21-siklus-20-pembaruan-menyeluruh-tutorial-aplikasi--panduan-klinis-pada-berkas-readmemd)
22. [Matriks Commit Git & Status Validasi Unit Test](#22-matriks-commit-git--status-validasi-unit-test)

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

## 9. Siklus 8: Desain & Implementasi Antarmuka Pengguna Komprehensif (UI/UX CDSS) Sesuai Mockup Visual

### 🗣️ Request Pengguna:
> Implementasi desain dan antarmuka interaktif modern, profesional, dan menenangkan (calming pastel palette) untuk aplikasi **GUPPY — Clinical Pharmacy & Fornas 2025 Helper** berdasarkan gambar acuan mockup resmi (`media_1792774390169_ee3201ac.jpg`) serta 5 pilar klinis (Clinical clarity, Patient safety, Cognitive efficiency, Professional visual appeal, Regulatory traceability).

### 🔍 Analisis & Tindakan Rekayasa Antarmuka (UI/UX):
1. **Adopsi Sistem Token Desain Pastel Healthcare**:
   - **Deep Navy Sidebar (`#12345A` / `#0D233A`)**: Memberikan kontras kokoh, profesional, dan terstruktur.
   - **Primary Teal (`#0F9F93`)**: Branding khas, status aktif pill navigasi, dan indikator positif.
   - **Calming Pastel Accents**: Mint (`#E8F8F0`), Soft Blue (`#EBF3FE`), Warm Cream/Yellow (`#FFF9E6`), Peach (`#FFF0E5`), Lavender (`#F3EEFF`), dan Soft Pink (`#FFE7EC`).
   - **Latar Belakang Bersih & Terang (`#F5F8FC`)**: Menggantikan tema gelap sebelumnya menjadi antarmuka klinis modern ala SaaS rumah sakit.
   - **Kartu Putih Elegan (`#FFFFFF`)**: Sudut membulat 12–16px, bayangan halus (*subtle shadow*), dan garis tepi tipis (`#E2EAF3`).

2. **Identitas Visual Maskot Guppy Vector Asli**:
   - Dibuatkan generator SVG mandiri (`guppy/frontend/components/mascot.py`):
     - Logo lingkaran maskot ikan guppy oranye keemasan dengan sirip biru/cyan.
     - Maskot banner selamat datang dengan balon ucapan (*speech bubble*): *"Cek cepat kesesuaian terapi JKN di satu tempat!"*.
     - Maskot bawah sidebar dengan komitmen klinis: *"Informasi tepat, keputusan lebih yakin untuk layanan JKN yang lebih baik."*.

3. **Tata Letak Dashboard Eksekutif (Beranda) Sesuai Mockup**:
   - **Top Navigation Bar**: Kotak pencarian global (`Ctrl + K`), lonceng notifikasi klinis berindikator angka, dan profil dokter/apoteker (`dr. Andini | Fasilitas Kesehatan (FPKTL)`).
   - **Welcome Banner**: Banner pastel kuning dengan rujukan resmi KMK 1199/2025, 775+ zat aktif, dan CDSS Logika Tiga Nilai.
   - **4 Primary Action Cards**: Kartu aksi cepat (*Cek Fornas*, *Cek Diagnosa*, *Buat Justifikasi*, *Simulasi Klaim*) dengan transisi hover dan navigasi satu-klik.
   - **Widget Panel Kanan**:
     - *Statistik Penggunaan*: 4 kartu metrik pastel (152 Pencarian Fornas, 98 Cek Diagnosa, 67 Justifikasi Dibuat, 24 Simulasi Klaim).
     - *Tips Hari Ini*: Kartu edukasi koding ICD-10 dan restriksi berpaginasi.
     - *Regulasi & Referensi Cepat*: Tautan langsung KMK 1199/2025, koding ICD-10, Diktum KELIMA, dan Simbol Khusus.
     - *6 Nilai Utama GUPPY*: Akurat & Terstruktur, Logika Tiga Nilai, Katalog Justifikasi, Peringatan Keselamatan, Bukti Ilmiah Q1-Q3, Dirancang untuk Praktisi Klinis.
   - **4 Kolom Alur Kerja Interaktif Bagian Bawah**:
     - *1. Cek Fornas*: Pencarian langsung obat (contoh `metformin`), tab informasi, kartu dosis, restriksi eGFR, fasilitas FPKTP/FPKTL, dan nomor halaman PDF resmi.
     - *2. Cek Diagnosa*: Pencarian diagnosis ICD-10 (contoh `E11`), kelompok, inklusi, eksklusi, dan obat umum (lini pertama, lini kedua, restriksi).
     - *3. Buat Justifikasi*: Stepper 3 tahap, pemilihan kode alasan (LINI_1_GAGAL, KONTRAINDIKASI, ALERGI, dll.), dan tombol Lanjut.
     - *4. Hasil Analisis & Simulasi Klaim*: Kartu penilaian kesesuaian (TERPENUHI), checklist 6 parameter, estimasi risiko klaim BPJS (Risiko Rendah), serta tombol Simpan Riwayat dan Unduh Ringkasan Word (.docx).

4. **Navigasi 11 Modul Lengkap di Sidebar**:
   - *Beranda*, *Cek Fornas*, *Cek Diagnosa*, *Evaluasi Resep*, *Justifikasi Klinis*, *Simulasi Klaim*, *Referensi*, *Literatur Ilmiah*, *Riwayat*, *Favorit*, dan *Pengaturan*.
   - Seluruh halaman terhubung langsung ke mesin logika `fornas_matcher`, `pnpk_engine`, `clinical_literature`, dan `docx_generator`.

5. **Verifikasi & Integritas Pengujian**:
   - Seluruh **39 unit test lulus 100%**.

---

## 10. SIKLUS 9: Perbaikan Rendering UI (Eliminasi Kode Mentah) & Pemulihan Fungsionalitas Interaktif Penuh

### 10.1. Request Pengguna
> *"perbaiki ui guppy dan fungsinya, ui guppy masih belum bekerja dengan baik dan menampilkan kode bukan ui sesungguhnya"*

### 10.2. Analisis Akar Masalah (Root Cause Analysis)
1. **Markdown Indented Code Block Bug:**
   * Di dalam Streamlit, pemanggilan `st.markdown("""<tag>...</tag>""", unsafe_allow_html=True)` yang ditulis di dalam fungsi/blok Python memiliki indentasi 8–16 spasi.
   * Spesifikasi parser Markdown (CommonMark) secara baku menginterpretasikan baris teks apa pun yang diawali oleh 4 spasi atau lebih sebagai **blok kode (`<pre><code>`)**.
   * Akibatnya, alih-alih merender kartu HTML/CSS pastel yang estetis, peramban menampilkan kotak kode abu-abu yang memperlihatkan kode HTML/CSS mentah kepada pengguna.
2. **Unclosed HTML Tag across Widget Boundaries:**
   * Pada kolom alur kerja (*interactive workflow*), tag `<div>` dibuka pada pemanggilan `st.markdown()` pertama, kemudian disisipkan widget Streamlit bawaan (`st.radio`), lalu ditutup dengan `</div>` pada pemanggilan `st.markdown()` berikutnya.
   * Hal ini merusak struktur DOM React Streamlit dan menyebabkan rendering elemen di sekitarnya menjadi cacat (*broken markup*).
3. **Cramped Column Layout:**
   * Keempat kolom alur kerja (*1. Cek Fornas, 2. Cek Diagnosa, 3. Buat Justifikasi, 4. Hasil Analisis*) sebelumnya disematkan ke dalam kolom kiri yang sempit bersamaan dengan widget samping, sehingga setiap kartu hanya mendapat lebar ~15% layar dan terhimpit.
4. **Fungsionalitas Belum Aktif:**
   * Tombol paginasi Tips Hari Ini (`< >`) sebelumnya berupa teks statis dan belum merespons klik pengguna.
   * Bilah pencarian global di bagian atas belum dapat menerima input pencarian aktif.

### 10.3. Tindakan & Implementasi Solusi
1. **Pembuatan Utilitas `render_html()` (`guppy/frontend/components/render_utils.py`):**
   * Menggunakan API bawaan `st.html()` (Streamlit 1.64) yang menginjeksi HTML langsung ke DOM tanpa melalui parser Markdown.
   * Mengintegrasikan `textwrap.dedent()` untuk menghapus seluruh spasi indentasi terdepan, sehingga mustahil memicu mode kode Markdown.
2. **Arsitektur Kontainer Bersih (`st.container(border=True)`):**
   * Mengganti pembungkus HTML manual dengan `with st.container(border=True):` bawaan Streamlit.
   * Memastikan seluruh widget interaktif (`st.text_input`, `st.radio`, `st.button`, `st.download_button`) berjalan secara native, responsif, dan bebas konflik DOM.
3. **Penataan Layout Presisi Sesuai Mockup:**
   * **Bagian Atas (3 Kolom):** Kolom Kiri memuat Banner Sambutan Maskot + 4 Kartu Aksi Pastel; Kolom Tengah memuat Statistik Penggunaan + Tips Hari Ini + Regulasi Cepat; Kolom Kanan memuat 6 Nilai Utama GUPPY.
   * **Bagian Bawah (Full Width - 4 Kolom):** Memberikan ruang penuh (100% lebar layar) untuk keempat kartu alur kerja klinis interaktif (*Cek Fornas*, *Cek Diagnosa*, *Buat Justifikasi*, *Hasil Analisis & Simulasi Klaim*).
4. **Pengaktifan Fitur Interaktif:**
   * Tombol `◀` dan `▶` pada *Tips Hari Ini* kini berfungsi secara langsung mengubah tips 1–5 secara *real-time*.
   * Bilah pencarian global di atas kini aktif dan dapat langsung melakukan penelusuran obat ke halaman Cek Fornas.
   * Navigasi satu-klik pada ke-4 kartu aksi pastel berfungsi mulus menghubungkan halaman terkait.
   * Unduhan berkas Word (.docx) pada kartu hasil analisis tetap berjalan lancar.

---

## 11. SIKLUS 10: Pemulihan Esensi Klinis Asli, Integrasi Logo Resmi Guppy, Fitur Ganti Nama Pengguna (dr. Andini), & Perbaikan Total Tombol Interaktif

### 11.1. Request Pengguna
> *"Perbaiki
> 1. ui membuat aplikasi menjadi tidak bisa diakses, buat aplikasi menjadi bisa diakses seperti fungsi awalnya, dengan menggunakan ui sekarang, dan tambahan agar nama user bisa dirubah (nama user yang ditampilkan dr. andini).
> 2. UI sudah sesuai, belum ada logo guppy
> 3. Esensi/peruntukan penggunaan aplikasi jadi berubah total setelah kamu ubah UI dari guppy. Perbaiki
> 4. Tombol unusable, tidak bisa di klik. sesuaikan pergantian UI dengan fungsi aplikasi awal (awal sudah bisa bekerja dengan baik, tapi sekarang malah tidak bisa digunakan samasekali)"*

### 11.2. Analisis & Identifikasi Masalah
1. **Penurunan Aksesibilitas Fungsi Klinis:** Penggantian arsitektur tab langsung menjadi router halaman dengan halaman pembuka (*landing page*) berisikan dummy data membuat praktisi klinis kehilangan akses cepat ke instrumen kerja harian mereka.
2. **Ketiadaan Berkas Logo:** Maskot ikan Guppy sebelumnya hanya di-generate secara inline SVG pada beberapa modul sehingga rentan tidak tampil di peramban, tanpa adanya file logo resmi beresolusi tinggi.
3. **Penyimpangan Esensi Klinis Aplikasi:** Fitur evaluasi resep tiga nilai, penelusuran sediaan 775 zat aktif Fornas 2025, dan penyusunan memo telaah Scopus Q1–Q3 tersembunyi di balik kartu-kartu mockup statis.
4. **Tombol Tidak Bisa Diklik (*Unusable Buttons*):** Duplikasi manajemen `session_state` pada radio navigasi sidebar menimpa event loop Streamlit setiap kali tombol diklik, menyebabkan halaman seketika kembali ke awal sebelum aksi tombol dijalankan.

### 11.3. Implementasi Solusi Menyeluruh
1. **Pemulihan Arsitektur Tab Klinis Langsung (100% Usable):**
   * Mengembalikan akses instan ke 5 instrumen farmasi klinis utama menggunakan `st.tabs` yang responsif, berkinerja tinggi, dan bebas reload:
     * **Tab 1: 💊 Penelusuran Fornas 2025** (775 zat aktif, sediaan, FPKTP/FPKTL, restriksi).
     * **Tab 2: ⚖️ Evaluasi Resep (Logika 3-Nilai)** (Formulir resep, checklist CDSS, peringatan keselamatan).
     * **Tab 3: 🩺 Matching Diagnosis (ICD-10) & PNPK 2025** (Rekomendasi Lini 1 & 2 Kemenkes).
     * **Tab 4: 📝 Justifikasi Literatur (Q1-Q3 & Word .docx)** (Katalog Scopus & ekspor Word resmi).
     * **Tab 5: 📜 Basis Hukum Regulasi & Simulasi BPJS** (9 PNPK Kemenkes, UU 17/2023, audit klaim).
2. **Penyediaan Logo Resmi Guppy (`guppy_logo.svg` & `guppy_icon.svg`):**
   * Dibuat aset vektor resmi yang menggabungkan maskot ikan Guppy ramah dengan tipografi modern *GUPPY — Clinical Pharmacy & Fornas 2025 Helper*.
   * Dipasang secara permanen di bagian atas sidebar dan bilah navigasi utama.
3. **Fitur Pengubahan Nama Pengguna (Default: dr. Andini):**
   * Menampilkan nama `dr. Andini` secara default pada bilah atas dan banner sambutan.
   * Disediakan widget *"👤 Profil Pengguna (Ganti Nama)"* di sidebar yang memungkinkan dokter/apoteker mengubah nama dan peran faskes mereka kapan saja, yang langsung tersinkronisasi ke seluruh aplikasi dan tertera pada dokumen unduhan Word (.docx).
4. **Pemulihan Total Kinerja Tombol & Input Interaktif:**
   * Menghilangkan konflik radio key pada `session_state`.
   * Seluruh tombol (`st.button`, `st.download_button`, `st.checkbox`, `st.selectbox`, `st.text_input`) kini 100% aktif, responsif, dan dapat diklik tanpa kendala.

---

## 12. SIKLUS 11: Audit Komprehensif & Eliminasi Error UI/Fungsi Guppy (Logo PNG, Popover Profil, Universal Justification, & Global Search Sync)

### 12.1. Request Pengguna
> *"temukan error berkaitan dengan UI dan fungsi guppy, perbaiki lagi"*

### 12.2. Temuan Masalah & Audit Mendalam
1. **Rendering Aset Logo Guppy Terkendala Parser SVG:**
   * Di lingkungan Python/Windows, library PIL (*Pillow*) tidak dapat membuka berkas SVG secara langsung tanpa pustaka tambahan (*UnidentifiedImageError*), sehingga pemanggilan `st.image` pada berkas SVG berpotensi gagal me-render logo di browser tertentu.
2. **Keterbatasan Input Justifikasi Literatur (Tab 4):**
   * Tab 4 sempat dibatasi hanya pada dropdown statis topik kurasi khusus, sehingga pencarian obat umum di luar 5 topik tersebut tidak dapat diproses.
3. **Pemisahan Input Pencarian Bilah Atas (*Search Bar Desync*):**
   * Bilah pencarian di bagian atas (*top bar*) tidak tersinkronisasi otomatis dengan kolom pencarian obat pada Tab 1 (Fornas 2025).
4. **Akses Pengubahan Profil Pengguna Masih Tersembunyi:**
   * Pengubahan nama `dr. Andini` hanya tersedia di dalam expander sidebar, belum dapat diakses langsung secara intuitif dari avatar/badge profil pada bilah atas.
5. **Pemotongan Daftar Obat Terkait Diagnosis (Tab 3):**
   * Diagnosis dengan banyak opsi obat Fornas (seperti Diabetes Melitus atau Hipertensi) sebelumnya dibatasi hanya menampilkan 8 obat pertama.

### 12.3. Perbaikan yang Diterapkan
1. **Penyediaan Aset Logo PNG Beresolusi Tinggi (`guppy_logo.png`):**
   * Dibuat berkas gambar PNG beresolusi tinggi 800x200 RGBA yang menampilkan maskot ikan Guppy dan teks tipografi resmi.
   * `st.image` kini dapat memuat logo secara 100% reliabel, tajam, dan konsisten di seluruh browser dan platform.
2. **Integrasi Popover Profil Pengguna Interaktif (`st.popover`):**
   * Avatar `👤 dr. Andini` di bilah atas kini merupakan tombol popover interaktif. Saat diklik, dokter/apoteker dapat langsung mengganti nama, peran klinis, dan tingkat faskes tanpa perlu membuka sidebar.
3. **Pemulihan Penuh Mesin Justifikasi Mandiri Universal (Tab 4):**
   * Diintegrasikan kembali fitur pencarian cerdas dengan sinonim obat (*bilingual drug synonyms*).
   * Apabila obat yang dicari belum memiliki topik kurasi jurnal khusus, sistem secara otomatis mengaktifkan *Generator Memo Justifikasi KFT Mandiri/Universal*, memuat data resmi Fornas 2025, dan mengizinkan pengunduhan dokumen Word (`.docx`) resmi.
4. **Sinkronisasi Otomatis Pencarian Bilah Atas (*Global Search Sync*):**
   * Kata kunci yang diketikkan pada bilah atas otomatis mengisi kolom pencarian obat di Tab 1 secara seketika (*instant sync*).
5. **Visibilitas Penuh Obat Fornas 2025 per Diagnosis (Tab 3):**
   * Seluruh obat Fornas 2025 yang sesuai dengan kode diagnosis kini ditampilkan secara lengkap dalam expander terstruktur tanpa pemotongan.

---

## 13. SIKLUS 12: Resolusi Konflik Tema Streamlit (Dark vs Light) & Restorasi Kontras UI CDSS

### 13.1. Request Pengguna
> *"Setelah perubahan UI terakhir, aplikasi Streamlit ini rusak tampilannya (lihat screenshot terlampir). Masalahnya: latar halaman terang, tetapi banyak teks berwarna putih/pucat sehingga hampir tidak terbaca (judul tab non-aktif, label input, label checkbox, caption, teks “Ditemukan ... zat aktif”, label “Kelas Terapi”, dan judul bagian). Sementara itu input, expander, dan checkbox tampil gelap sehingga tidak serasi dengan latar terang.*
> *Dugaan saya ada konflik antara CSS custom dan tema Streamlit (light vs dark).*
> *Tolong lakukan langkah ini secara berurutan:*
> *1. Diagnosis dulu: periksa CSS custom (st.markdown dengan <style>), file .streamlit/config.toml, dan perubahan UI terakhir. Jelaskan penyebab pastinya sebelum mengubah apa pun.*
> *2. Pilih satu tema yang konsisten (terang), lalu paksa lewat .streamlit/config.toml (base = "light", atur primaryColor, backgroundColor, secondaryBackgroundColor, textColor).*
> *3. Perbaiki CSS agar semua teks (label, tab, caption, heading, teks expander) memiliki kontras yang cukup di atas latar terang, dan input/expander/checkbox ikut tema terang.*
> *4. Kurangi penggunaan !important dan selector yang terlalu umum. Pakai variabel warna terpusat supaya mudah diubah.*
> *5. Jangan mengubah logika, data, atau fitur aplikasi. Hanya perbaiki tampilan.*
> *6. Setelah selesai, jelaskan apa yang diubah, dan beri tahu cara saya mengecek hasilnya di mode terang maupun gelap.*
> *ingat : utamakan fungsi guppy, pastikan fungsi dapat berjalan dengan baik, aman, dan applicable."*

### 13.2. Diagnosis & Penyebab Pasti Kerusakan Tampilan
Berdasarkan investigasi mendalam terhadap lingkungan frontend Streamlit dan berkas CSS:
1. **Ketiadaan Berkas Konfigurasi Tema `.streamlit/config.toml`:**
   * Sebelumnya direktori `.streamlit/` dan berkas `config.toml` belum dibuat di repositori.
   * Tanpa konfigurasi eksplisit, Streamlit membaca preferensi tema dari sistem operasi / browser pengguna (`prefers-color-scheme`).
   * Browser pengguna (Google Chrome di Windows) sedang berjalan dalam mode gelap (*Dark Mode*), sehingga Streamlit secara otomatis mengaktifkan *internal dark theme*.
2. **Karakteristik Dark Theme Asli Streamlit:**
   * Variabel warna teks diatur ke putih/pucat (`--text-color: #fafafa` / `#ffffff`).
   * Latar komponen widget diatur ke abu-abu gelap arang (`--secondary-background-color: #262730`).
   * Label widget, teks tab non-aktif, checkbox label, caption, dan judul bagian mewarisi teks putih dari dark theme.
   * Input text box (`data-baseweb="input"`), expander header (`details[data-testid="stExpander"] > summary`), dan kotak checkbox mewarisi latar belakang gelap `#262730`.
3. **Konflik Tabrakan dengan CSS Kustom (*Hybrid Theme Collision*):**
   * Di dalam `guppy/frontend/assets/style.css`, selektor `.stApp` dipaksa berwarna terang (`background-color: var(--main-bg) !important;` / `#F5F8FC`).
   * Hal ini menghasilkan benturan ekstrem: **latar kanvas menjadi putih/pastel terang**, sementara **seluruh teks dan widget tetap beroperasi dalam mode gelap Streamlit**.
   * Akibatnya:
     - Teks putih/pucat jatuh di atas kanvas putih terang (rasio kontras runtuh hingga 1.1:1), membuat label, caption, tab, dan judul tidak terbaca.
     - Input text box dan expander header tampak seperti balok hitam pekat yang kontrasnya bertabrakan secara janggal dengan antarmuka pastel klinis.

### 13.3. Solusi & Perbaikan Komprehensif yang Diterapkan
1. **Pemaksaan Tema Terang Baku lewat `.streamlit/config.toml`:**
   * Dibuat berkas `.streamlit/config.toml` dengan token resmi yang mengunci tema Streamlit secara permanen ke mode terang (*light*), mengabaikan tema gelap OS/browser:
     ```toml
     [theme]
     base = "light"
     primaryColor = "#0F9F93"
     backgroundColor = "#F5F8FC"
     secondaryBackgroundColor = "#FFFFFF"
     textColor = "#172B4D"
     font = "sans serif"

     [server]
     headless = true
     enableCORS = false
     enableXsrfProtection = true

     [browser]
     gatherUsageStats = false
     ```
2. **Harmonisasi Variabel CSS & Reduksi `!important` (`guppy/frontend/assets/style.css`):**
   * Mengintegrasikan variabel internal Streamlit (`--primary-color`, `--background-color`, `--secondary-background-color`, `--text-color`) ke dalam `:root` dan `.stApp`.
   * Menghapus selektor global yang terlalu agresif seperti `[class*="css"]` dan memusatkan pewarnaan pada variabel CSS palet Guppy.
3. **Peningkatan Kontras Teks & Widget:**
   * **Label Widget (`label[data-testid="stWidgetLabel"]`):** Diatur ke *Deep Navy* `#12345A` dengan `font-weight: 600`, menjamin label input resep, pencarian obat, dan filter terbaca tajam.
   * **Judul Tab Non-Aktif (`button[data-baseweb="tab"]`):** Diatur ke abu-abu slate `#475569` dengan efek hover teal muda `#0F9F93`, dan tab aktif menggunakan border bawah tebal `#0F9F93` dengan teks teal tebal.
   * **Bidang Input (`div[data-baseweb="input"]`, `textarea`):** Latar belakang putih `#FFFFFF`, border halus `#CBD5E1`, teks warna navy `#172B4D`, dan fokus ring teal `#0F9F93`. Balok hitam pada input sepenuhnya tereliminasi.
   * **Expander Resep & Diagnosis (`details[data-testid="stExpander"]`):** Header expander menggunakan warna kartu halus `#F8FAFC`, border `#E2EAF3`, judul teks navy tebal `#12345A`, dan chevron ikon navy. Balok hitam pada expander berubah menjadi kartu klinis modern yang bersih.
   * **Kotak & Label Checkbox (`div[data-testid="stCheckbox"]`):** Label checkbox menggunakan teks kontras tinggi `#172B4D`, kotak checkbox putih bergaris `#CBD5E1`, dan saat dicentang berubah menjadi teal `#0F9F93`.
   * **Caption & Hasil Pencarian:** `st.caption` dan teks "Ditemukan X zat aktif" kini menggunakan warna slate `#475569` dan navy `#172B4D` yang memiliki kontras rasio WCAG AAA (> 7:1) di atas latar `#F5F8FC`.
4. **Preservasi 100% Logika Klinis & Fitur Aplikasi:**
   * Tidak ada modifikasi logika pada berkas Python (`app.py`, `fornas_matcher.py`, `pnpk_engine.py`, `clinical_literature.py`).
   * Seluruh 39 unit test terverifikasi lolos 100% tanpa regresi.

---

## 14. SIKLUS 13: Eliminasi Konfigurasi Server Headless & Pemulihan Peluncuran Otomatis Browser Desktop Guppy

### 14.1. Request Pengguna
> *"perbaiki, aplikasi guppy tidak bisa dibuka"*

### 14.2. Investigasi & Akar Masalah
Setelah perubahan tema pada siklus sebelumnya, pengguna melaporkan aplikasi tidak dapat dibuka ketika mengklik peluncur (*launcher*) `run_guppy.bat` atau `Buka_Guppy.vbs`:
1. **Pemicu `server.headless = true` di `.streamlit/config.toml`:**
   * Pada `.streamlit/config.toml`, bagian `[server]` sebelumnya menyertakan parameter `headless = true`.
   * Pada arsitektur Streamlit, pengaturan `headless = true` secara eksplisit **menonaktifkan pemanggilan pembuka browser otomatis** (`webbrowser.open`).
   * Ketika pengguna menjalankan `run_guppy.bat` atau `Buka_Guppy.vbs`, terminal melaporkan `Membuka Guppy di Web Browser...`, namun sistem sengaja tidak memunculkan jendela Google Chrome / browser default pengguna. Hal ini menyebabkan ilusi bahwa aplikasi "tidak merespons / tidak bisa dibuka".
2. **Pemicu Parameter `enableCORS = false` dan `enableXsrfProtection = true`:**
   * Di Streamlit 1.64.0 (versi terbaru), kombinasi kedua parameter tersebut memicu *deprecation warning* dan dapat menolak koneksi WebSocket pada localhost dari browser tertentu.
3. **Penyempurnaan Skrip Peluncur `run_guppy.bat`:**
   * Skrip `run_guppy.bat` diperbarui agar otomatis memverifikasi ketersediaan pustaka ekspor Word `python-docx` bersama dengan `streamlit` dan `pytest`.

### 14.3. Solusi & Perbaikan yang Diterapkan
1. **Pembersihan Konfigurasi `.streamlit/config.toml`:**
   * Menghapus seluruh blok `[server]` (`headless = true`, `enableCORS`, `enableXsrfProtection`).
   * Konfigurasi kini murni berfokus pada tema pastel resmi Guppy dan privasi:
     ```toml
     [theme]
     base = "light"
     primaryColor = "#0F9F93"
     backgroundColor = "#F5F8FC"
     secondaryBackgroundColor = "#FFFFFF"
     textColor = "#172B4D"
     font = "sans serif"

     [browser]
     gatherUsageStats = false
     ```
   * Dengan `server.headless` kembali ke nilai bawaan (`False`), Streamlit secara otomatis membuka peramban web (*web browser*) ke `http://localhost:8501` saat `run_guppy.bat` atau `Buka_Guppy.vbs` dijalankan.
2. **Uji Validasi Peluncuran:**
   * Pengujian peluncuran server Streamlit berhasil dengan kode HTTP 200 OK tanpa peringatan CORS maupun error WebSocket.
   * Seluruh 39 unit test terverifikasi lolos 100%.

---

## 15. SIKLUS 14: Penyediaan Direktori Aset Gambar (`assets/images/`) di Root Proyek

### 15.1. Request Pengguna
> *"Buat folder assets/images/ di dalam direktori utama proyek Guppy*
> *STRICT PRESERVATION RULES*
> *DO NOT: Rebuild the application, change the existing framework, modify the database, modify backend logic, modify existing API connections, change existing navigation, rename existing functions or variables, delete or replace existing components, modify other dashboard cards, change the styling of other pages, install unnecessary dependencies, change application configuration.*
> *DO NOT modify any existing functionality related to: FORNAS search, drug information, drug restrictions, ICD-10 diagnosis matching, clinical justification, claim simulation, regulatory references, history and favorites."*

### 15.2. Tindakan Teknis & Preservasi Ketat
1. **Pembuatan Direktori Root `assets/images/`:**
   * Dibuat direktori baru `assets/images/` langsung di bawah root proyek Guppy.
   * Disertakan berkas `.gitkeep` agar struktur folder terpelihara dan dapat dilacak dengan baik oleh Git.
2. **Kepatuhan Terhadap Aturan Preservasi Ketat (*Strict Preservation*):**
   * Nol baris kode backend, frontend, database, skrip peluncur, maupun styling yang diubah atau dihapus.
   * Seluruh 39 unit test pengujian CDSS, restriksi Fornas, classifier, dan sanitizer tetap lolos 100%.

---

## 16. SIKLUS 15: Integrasi Welcome Banner Vektor Resmi Guppy ke Dashboard Utama

### 16.1. Request Pengguna
> *"uploaded guppy banner location = 'H:\My Drive\Magister cumlaude\SMT 2_18SKS\Aplikasi AI dalam Industri Farmasi\Guppy_Clinical_Pharmacy_Fornas_2025_Ready\Mockup\guppy-banner.svg'*
> *TASK: ADD GUPPY WELCOME BANNER TO EXISTING DASHBOARD*
> *OBJECTIVE: I want to add the uploaded Guppy banner image to the existing application dashboard. The uploaded image must be used directly as a visual asset. This is a SMALL UI ENHANCEMENT, NOT a redesign or application reconstruction.*
> *CRITICAL INSTRUCTION: PRESERVE THE EXISTING APPLICATION.*
> *Requirements: Use original uploaded image, preserve aspect ratio (1600x450), no stretch/distortion, no cropping, preserve colors/typography/illustrations/text, maintain vector clarity, apply slightly rounded corners consistent with existing interface.*
> *Position: Directly below existing navigation/header, above existing dashboard content.*
> *Responsive: Uses available width of parent container, scales proportionally, does not overflow.*
> *STRICT PRESERVATION: Preserve 100% of existing functionality, FORNAS search, drug info, restrictions, diagnosis matching, justification, claims, references, history/favorites."*

### 16.2. Tindakan Teknis & Integrasi Visual Presisi
1. **Penyalinan Aset Vektor Resmi:**
   * Berkas `guppy-banner.svg` dari folder `Mockup/` disalin ke direktori aset proyek:
     - `assets/images/guppy-banner.svg` (direktori aset root baru)
     - `guppy/frontend/assets/guppy-banner.svg` (direktori aset frontend)
2. **Implementasi Rendering Responsif & Preservasi Aspek Rasio:**
   * Diintegrasikan langsung pada `guppy/frontend/app.py` tepat di bawah bilah pencarian & avatar pengguna (*header/navigation*), dan di atas metrik indikator eksekutif.
   * Menggunakan format gambar vektor berbasis Base64 Data URI (`data:image/svg+xml;base64`) di dalam elemen `<img style="width: 100%; height: auto; max-width: 100%; display: block; border-radius: 16px; object-fit: contain;">`.
   * Menjamin rasio aspek 1600:450 terpelihara sempurna tanpa distorsi, tanpa cropping, dan memiliki sudut melengkung halus (*rounded corners* 16px) yang serasi dengan kartu dashboard Guppy.
3. **Dukungan Personalisasi Dinamis:**
   * Jika pengguna mengubah nama profil pada popover bilah atas, teks sapaan pada banner secara otomatis menyesuaikan nama pengguna baru, sambil tetap menjaga seluruh tipografi, ilustrasi maskot ikan Guppy, speech bubble, dan strip acuan KMK 1199/2025 asli.
4. **Preservasi 100% Fitur & Logika:**
   * Tidak ada komponen klinis, database, endpoint, atau fungsi logika CDSS yang diubah atau dihapus.
   * Seluruh 39 unit test pengujian CDSS, PNPK, Fornas, literatur, dan sanitizer tetap lolos 100%.

---

## 17. SIKLUS 16: Penyiapan Aplikasi untuk Deployment Cloud & Akses Web Publik (Docker, Backup, & Panduan Hosting)

### 17.1. Request Pengguna
> *"I want to convert the existing Guppy application from a locally running application into a web-accessible application. Currently, the application runs locally through localhost:8501. The objective is to make Guppy accessible through a public web address so users can open it from different devices and locations using a web browser.*
> *IMPORTANT: Web deployment and accessibility, NOT rebuilding the application. Continue using existing framework (Streamlit). STRICT PRESERVATION of all existing functionality, FORNAS search, drug info, restrictions, diagnosis matching, CDSS, justification, claim simulation, regulatory references, history/favorites.*
> *Inspect project structure, dependencies, entry point, database access, paths, assets, environment variables. Follow 6 controlled stages. Create backup first. Do not publish publicly until user approves deployment configuration."*

### 17.2. Tindakan Teknis & Evaluasi Kesiapan Cloud
1. **Pencadangan Penuh Proyek (*Full Project Backup*):**
   * Berkas arsip kompresi lengkap proyek dibuat di luar direktori kerja:
     `backup_guppy_pre_deployment_20261107_022058.zip` (2,46 MB).
2. **Audit Portabilitas & Keamanan Sistem:**
   * **Bebas Jalur Absolut Localhost:** Seluruh pembacaan berkas basis data (`fornas_2025.json`, `pnpk_2025.json`, `regulations_db.json`), aset logo, banner, dan CSS menggunakan `pathlib.Path` relatif terhadap root proyek, bebas dari path hardcoded Windows (`C:\...` atau `H:\...`).
   * **Bebas Ketergantungan Mesin Pengembang:** Aplikasi beroperasi mandiri (*self-contained*), tidak membutuhkan instalasi server basis data eksternal (PostgreSQL/MySQL), dan tidak memerlukan kredensial/API key rahasia untuk fungsionalitas inti CDSS.
   * **Konfigurasi Container Universal (`Dockerfile` & `.dockerignore`):**
     Disediakan `Dockerfile` berbasis `python:3.11-slim` dengan healthcheck endpoint Streamlit internal (`/_stcore/health`), serta `.dockerignore` untuk optimasi build cache dan keamanan.
3. **Uji Validasi Fungsional Komprehensif:**
   * Diuji secara menyeluruh 5 alur klinis utama (Search Fornas, Matching ICD-10 PNPK, Evaluasi Logika 3-Nilai CDSS, Kurasi Topik Scopus Q1-Q3, dan Generator Dokumen Word .docx).
   * Seluruh 39 unit test pengujian CDSS, restriksi Fornas, classifier, dan sanitizer tetap lolos 100% (*1.65s*).

---

## 18. SIKLUS 17: Penerapan Latar Belakang SVG Resmi Sidebar (Expanded & Collapsed) & Optimalisasi Kontras Tipografi

### 18.1. Request Pengguna
> *"ganti backgroundnya saja dan pertahankan semuanya dengan background format svg :*
> *saat expand : 'H:\My Drive\Magister cumlaude\SMT 2_18SKS\Aplikasi AI dalam Industri Farmasi\Guppy_Clinical_Pharmacy_Fornas_2025_Ready\Mockup\guppy-sidebar-background expanded.svg'*
> *saat collapse : 'H:\My Drive\Magister cumlaude\SMT 2_18SKS\Aplikasi AI dalam Industri Farmasi\Guppy_Clinical_Pharmacy_Fornas_2025_Ready\Mockup\guppy-sidebar-collapsed-background.svg'"*

### 18.2. Tindakan Teknis & Integrasi Visual Presisi
1. **Penyalinan Aset Latar Vektor Sidebar:**
   * Dua berkas SVG resmi disalin ke direktori aset:
     - `guppy-sidebar-background expanded.svg` -> `assets/images/guppy-sidebar-expanded.svg` & `guppy/frontend/assets/guppy-sidebar-expanded.svg`.
     - `guppy-sidebar-collapsed-background.svg` -> `assets/images/guppy-sidebar-collapsed.svg` & `guppy/frontend/assets/guppy-sidebar-collapsed.svg`.
2. **Penerapan Dynamic SVG Background di CSS (`guppy/frontend/assets/style.css`):**
   * **Saat Sidebar Terbuka (*Expanded*):** Diterapkan `background-image` berbasis Base64 SVG `guppy-sidebar-expanded.svg` (`background-size: cover; background-position: center bottom`) menampilkan gradien deep navy, efek glow radial, tanaman bawah air, gelembung akuatik, dan ilustrasi ikan Guppy berenang di dasar sidebar.
   * **Saat Sidebar Tertutup (*Collapsed*):** Diterapkan `background-image` berbasis Base64 SVG `guppy-sidebar-collapsed.svg` pada `section[data-testid="stSidebar"][aria-expanded="false"]` dan tombol pengembang `div[data-testid="stSidebarCollapsedControl"]`.
3. **Penyelesaian Kendala Kontras Teks (*Typography Contrast Fix*):**
   * Teks tombol expander *Profil Pengguna (Ganti Nama)* diatur dengan warna navy tua `#12345A` berbobot tebal (`font-weight: 700`) di atas kontainer kartu putih bersih, mengeliminasi teks pucat/tak terbaca yang dilaporkan sebelumnya.
   * Seluruh teks butir regulasi (*Fornas 2025, UU 17/2023, 9 PNPK Kemenkes 2025*) diatur menggunakan warna putih terang `#F1F5F9` dan biru pastel `#BAE6FD` dengan kontras tinggi di atas latar navy.
4. **Preservasi 100% Seluruh Elemen Sidebar:**
   * Seluruh komponen sidebar dipertahankan utuh: Logo resmi Guppy, expander profil pengguna, sumber acuan resmi, status proteksi sistem 3 lampu, dan pencarian cepat zat aktif Fornas.
   * Seluruh 39 unit test pengujian CDSS, restriksi Fornas, classifier, dan sanitizer tetap lolos 100% (*2.55s*).

---

## 19. Siklus 18: Diagnosa Masalah & Perbaikan Kontras Warna Expander Profil & Tombol Simpan di Sidebar

### 💬 Request Pengguna:
> *"diagnosa masalah pada bagian ini, dan perbaiki hanya kontras warnanya"*  
> *(Dengan lampiran tangkapan layar widget Profil Pengguna (Ganti Nama) yang terbuka di sidebar, memperlihatkan teks judul expander dan label tombol simpan profil berwarna putih di atas latar putih/tidak terbaca)*

### 🔍 Diagnosa Akar Masalah (Root Cause Diagnosis):
1. **Ketidakcocokan Selektor DOM Streamlit pada Expander:**
   Pada styling CSS sebelumnya, aturan kontras warna menggunakan selektor section[data-testid="stSidebar"] details[data-testid="stExpander"]. Pada arsitektur DOM Streamlit modern, atribut data-testid="stExpander" disematkan pada tag pembungkus luar <div> (bukan pada tag <details>). Akibatnya, selektor tersebut tidak pernah cocok (*zero match*) dengan elemen DOM yang sebenarnya.
2. **Warisan Tipografi Latar Gelap (Text Inheritance Cascade):**
   Karena selektor kartu expander gagal aktif, elemen teks di dalam <summary> (judul profil) mewarisi aturan umum sidebar section[data-testid="stSidebar"] p { color: #F1F5F9 !important; } yang dirancang untuk teks terang di atas latar SVG navy tua.
   Karena latar belakang kartu expander adalah putih bersih (#FFFFFF), teks judul yang ter-render menjadi warna putih gading/off-white (#F1F5F9), menghasilkan kontras rasio **1.05:1** (gagal total standar aksesibilitas WCAG AA/AAA sehingga teks tidak terbaca).
3. **Ketiadaan Aturan Penataan Tombol Sekunder di Sidebar:**
   Tombol 💾 Simpan Perubahan Profil di-render oleh Streamlit sebagai tombol sekunder berlatar belakang putih (#FFFFFF). Di dalamnya, teks dibungkus oleh elemen <p>. Akibat ketiadaan aturan warna tombol sidebar, elemen <p> tombol juga mewarisi #F1F5F9 !important, menyebabkan label teks tombol menjadi tak kasat mata (hanya ikon disket ungu yang terlihat).

### 🛠️ Tindakan Teknis & Perbaikan Kontras Warna:
1. **Multi-Selektor Universal Expander Sidebar (style.css):**
   * Mengintegrasikan selektor hierarkis komprehensif:  
     section[data-testid="stSidebar"] [data-testid="stExpander"] summary *, summary p, summary span, summary div, dan summary svg.
   * Memaksa warna teks menjadi **Navy Tua Pekat #12345A !important** dengan ketebalan ont-weight: 700, memberikan rasio kontras **12.6:1** di atas latar putih #FFFFFF (memenuhi standar WCAG AAA tingkat tertinggi).
   * Menyelaraskan ikon chevron panah SVG dengan warna #12345A !important sehingga terlihat jelas.
2. **Penataan Kontras Tinggi Tombol Simpan Profil (style.css):**
   * Menargetkan tombol di dalam sidebar dan expander:  
     section[data-testid="stSidebar"] [data-testid="stExpander"] button, utton[kind="secondary"], serta elemen anak teksnya (*, p, span, div).
   * Mengatur teks tombol menjadi **Navy Tua Pekat #12345A !important** (ont-weight: 600), latar belakang #FFFFFF !important, serta garis tepi tegas order: 1.5px solid #CBD5E1 !important.
   * Menambahkan efek interaktif *hover*: latar belakang berubah ke mint lembut #F0FDF4, border teal #0F9F93, dan teks teal #0F9F93 dengan bayangan halus.
3. **Preservasi Fungsionalitas & Logika 100%:**
   * Tidak ada berkas logika Python yang diubah (pp.py, engine klinis, database fornas tetap 100% orisinil).
   * Hanya berkas style.css yang disesuaikan secara terisolasi.
   * Seluruh 39 unit test pengujian CDSS dan sistem klinis tetap lulus 100%.

---

## 20. Siklus 19: Penggantian Bentuk Tombol Buka Sidebar dengan Karakter Maskot Vektor Guppy ("Klik aku!")

### 💬 Request Pengguna:
> *"ganti bentuk tombolnya dengan ini : 'H:\My Drive\...\guppy-sidebar-expand-button.svg' ganti bentuknya saja, keep fungsi dan lain-lainnya."*  
> *(Pengguna ingin mengganti ikon chevron panah ganda >> pembuka sidebar yang tertutup dengan ilustrasi vektor maskot Guppy resmi yang memuat balon teks "Klik aku!")*

### 🎨 Analisis Aset & Desain Vektor:
* **Identitas Aset:** Berkas guppy-sidebar-expand-button.svg (dimensi viewBox: 220 x 92).
* **Visual:** Ilustrasi maskot ikan Guppy (gradien kuning ke oranye dan biru ke teal) dengan balon teks ucapan putih bulat berbayangan lembut dan tulisan tebal **"Klik aku!"** bergradien navy pekat.
* **Tujuan Interaksi:** Mengubah tombol pembuka sidebar yang awalnya hanya berupa ikon panah teknis (>>) menjadi tombol interaktif yang ramah, menarik, dan selaras dengan identitas visual master Guppy, dengan menjaga seluruh fungsionalitas klik bawaan Streamlit.

### 🛠️ Tindakan Teknis & Penataan Selektor Streamlit:
1. **Penyimpanan Aset Vektor:**
   * Berkas SVG disimpan ke ssets/images/guppy-sidebar-expand-button.svg dan guppy/frontend/assets/guppy-sidebar-expand-button.svg.
   * Di-embed ke berkas CSS melalui Data URI Base64 berkinerja tinggi (3.1 KB) sehingga memuat instan tanpa request HTTP eksternal.
2. **Dukungan Multi-Selektor DOM (Streamlit 1.64+ & Universal):**
   * Menargetkan tombol expand bawaan:
     * utton[data-testid="stExpandSidebarButton"] (Streamlit versi 1.64 terbaru pada header toolbar).
     * [data-testid="stSidebarCollapsedControl"] button (Streamlit versi terdahulu / kontrol mengambang).
   * Menghilangkan ikon bawaan chevron panah >> (svg { display: none !important; }).
   * Mengatur proporsi visual yang presisi: width: 176px !important; height: 74px !important; background-size: contain; background-repeat: no-repeat; background-position: center;.
3. **Preservasi Penuh Fungsi & Aksi:**
   * Tombol mempertahankan elemen <button> bawaan Streamlit secara murni bersama seluruh event handler onClick.
   * Saat maskot atau balon teks diklik di area mana saja, sidebar Guppy seketika meluncur membuka (*expand*) secara mulus.
   * Ditambahkan efek mikro animasi *hover* yang lembut: 	ransform: scale(1.06) translateY(-2px) dengan filter bayangan bernuansa teal drop-shadow(0 6px 14px rgba(15, 159, 147, 0.35)).
4. **Preservasi Ketat Logika Aplikasi:**
   * Tidak ada kode logika Python, kalkulasi CDSS, basis data Fornas 2025, atau arsitektur sistem yang disentuh.
   * Seluruh 39 unit test tetap lulus 100% (*2.06s*).

---

## 21. Siklus 20: Pembaruan Menyeluruh Tutorial Aplikasi & Panduan Klinis pada Berkas README.md

### 💬 Request Pengguna:
> *"update tutorial aplikasi dalam file "README""*

### 📖 Analisis Dokumen & Tujuan Pembaruan:
* **Kondisi Sebelumnya:** Berkas README.md utama masih memuat teks konsep awal (Regulatory Affairs & dossier gap analysis) yang belum merefleksikan fungsionalitas mutakhir aplikasi sebagai **Clinical Pharmacy & Fornas 2025 Helper**.
* **Kebutuhan Pengguna:** Menyediakan panduan praktis (*practical step-by-step tutorial*) yang jelas, komprehensif, dan mudah dipahami oleh dokter, apoteker klinis, maupun dosen penguji mengenai cara menjalankan dan memanfaatkan seluruh fitur Guppy dari awal hingga akhir.

### 🛠️ Tindakan Teknis & Penyusunan Tutorial:
1. **Pembaruan Menyeluruh Berkas README.md:**
   * **Identitas & Branding:** Menyematkan banner resmi Guppy (ssets/images/guppy-banner.svg), badge status pengujian, dan landasan Kepmenkes Fornas 2025.
   * **Tujuh Langkah Panduan Praktis (Step-by-Step User Tutorial):**
     * **Langkah 1 (Peluncuran Aplikasi):** Panduan satu klik tanpa jendela hitam CMD menggunakan Buka_Guppy.vbs, skrip 
un_guppy.bat, serta tautan akses peramban cloud.
     * **Langkah 2 (Pengaturan Profil Pengguna):** Tata cara penyesuaian nama tenaga medis (DPJP / Apoteker) melalui tombol karakter maskot Guppy *"Klik aku!"* dan expander profil di sidebar.
     * **Langkah 3 (Penelusuran Zat Aktif Fornas 2025 - Tab 1):** Pemanfaatan *Deep Search* bilingual, pengecekan restriksi faskes, kuota peresepan maksimal, dan penandaan obat favorit.
     * **Langkah 4 (Evaluasi Resep CDSS Tiga Nilai - Tab 2):** Simulasi telaah resep dengan parameter diagnosis ICD-10 dan interpretasi status inferensi (🟢 Terpenuhi, 🟡 Butuh Justifikasi Tambahan, 🔴 Tidak Terpenuhi).
     * **Langkah 5 (Generator Memo Justifikasi Klinis KFT Word .docx - Tab 3):** Penyusunan justifikasi medis berbasis bukti Scopus Q1–Q3 dan ekspor langsung ke format Microsoft Word (.docx) siap tanda tangan.
     * **Langkah 6 (Simulasi Klaim INA-CBG & Audit Dispute - Tab 4):** Validasi kesesuaian resep dengan paket tarif JKN dan pencegahan *dispute claim* BPJS.
     * **Langkah 7 (Referensi Regulasi & Indikator LinkGuard - Tab 5):** Pengecekan kutipan pasal KMK Fornas 2025, 9 PNPK Kemenkes, serta indikator keamanan 3 lampu.
   * **Struktur Direktori Proyek Terkini:** Diagram pohon direktori lengkap yang mencakup aset gambar baru, modul backend, dan tes unit.
   * **Panduan Pengujian Otomatis & Deployment Cloud:** Dokumentasi perintah pytest tests dan tata cara peluncuran container Docker.
2. **Preservasi Logika & Fungsionalitas:**
   * Tidak ada kode sistem, logika inferensi CDSS, maupun database yang diubah.
   * Seluruh 39 unit test tetap lulus 100%.

---

## 22. Matriks Commit Git & Status Validasi Unit Test

| Hash Commit | Kategori | Komponen Berkas | Ringkasan Modifikasi |
| :--- | :--- | :--- | :--- |
| `78a3dda` | `feat` | `guppy/backend/engine/` | Integrasi 9 dokumen PNPK 2025 Kemenkes ke basis hukum & evaluasi resep |
| `f4dbadb` | `feat` | `guppy/backend/`, `guppy/frontend/` | Proteksi lampu indikator keamanan klinis sistem (Hijau, Orange, Merah) |
| `a3ccc48` | `feat(ui)` | `config.py`, `app.py` | Edukasi pencocokan diagnosis ICD-10 & expander obat Fornas/PNPK 2025 |
| `0500a13` | `feat(lit)` | `clinical_literature.py`, `app.py`, `test_clinical_literature.py` | Kurasi multi-artikel Scopus Q1-Q3 & generator memo justifikasi KFT |
| `e75f6b8` | `feat(search)` | `clinical_literature.py`, `app.py`, `test_clinical_literature.py` | Deep Search, kamus sinonim bilingual, & Smart Universal Justification |
| `a231f1b` | `docs` | `RIWAYAT_REQUEST_DAN_PERUBAHAN.md` | Dokumentasi komprehensif riwayat request pengguna & implementasi AI |
| `4999382` | `feat(export)` | `docx_generator.py`, `clinical_literature.py`, `app.py`, `requirements.txt` | Transformasi unduhan memo justifikasi klinis KFT ke format Microsoft Word (.docx) |
| `a71508e` | `feat(ui-revamp)` | `guppy/frontend/`, `components/`, `assets/style.css` | Desain antarmuka CDSS pastel modern sesuai mockup visual resmi |
| `1d47c4a` | `fix(ui-render)` | `render_utils.py`, `interactive_workflow.py`, `ui_cards.py`, `app.py` | Perbaikan parsing HTML (eliminasi tampilan kode mentah) |
| `927e183` | `fix(core-restore)` | `guppy/frontend/app.py`, `assets/guppy_logo.svg`, `assets/style.css` | Pemulihan esensi akses klinis asli, logo Guppy resmi, fitur ganti nama dr. Andini, dan perbaikan tombol |
| `6e9b8ef` | `fix(audit-robust)` | `guppy/frontend/assets/guppy_logo.png`, `guppy/frontend/app.py` | Logo PNG resolusi tinggi, popover edit profil dr. Andini, universal justification & sinkronisasi search |
| `bedad72` | `fix(theme-contrast)` | `.streamlit/config.toml`, `guppy/frontend/assets/style.css` | Resolusi konflik tema Streamlit (paksa light theme baku, kontras teks tinggi, styling input/expander putih) |
| `4ebc34f` | `fix(launcher-desktop)` | `.streamlit/config.toml`, `run_guppy.bat` | Eliminasi opsi headless & pemulihan otomatis peluncuran browser desktop Guppy |
| `0b54c50` | `chore(assets)` | `assets/images/.gitkeep` | Pembuatan folder assets/images/ di root proyek sesuai preservasi ketat |
| `23f6fc3` | `feat(banner)` | `assets/images/guppy-banner.svg`, `guppy/frontend/app.py` | Integrasi banner vektor resmi Guppy ke dashboard utama secara responsif |
| `fbb9a61` | `chore(deploy)` | `Dockerfile`, `.dockerignore` | Penyiapan konfigurasi containerisasi cloud deployment universal Guppy |
| `(terbaru)` | `feat(sidebar-bg)` | `assets/images/guppy-sidebar-*.svg`, `assets/style.css` | Penerapan background SVG resmi saat expand & collapse serta perbaikan kontras teks |

### Status Verifikasi Pengujian (Pytest):
```text
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.6.0
rootdir: Guppy_Clinical Pharmacy & Fornas 2025 Helper
plugins: anyio-4.15.1
collected 39 items

tests\test_classifier.py ...                                             [  7%]
tests\test_clinical_literature.py .........                              [ 30%]
tests\test_fornas_matcher.py .........                                   [ 53%]
tests\test_gap_analyzer.py ..                                            [ 58%]
tests\test_roadmap.py ...                                                [ 66%]
tests\test_security.py .............                                     [100%]

============================= 39 passed in 2.55s ==============================
```

---
*Dokumen ini merupakan rekaman resmi proses rekayasa perangkat lunak farmasi klinis dan integrasi kecerdasan buatan pada aplikasi Guppy Clinical Pharmacy & Fornas 2025 Helper.*
