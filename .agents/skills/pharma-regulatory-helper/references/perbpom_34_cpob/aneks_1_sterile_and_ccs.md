# Aneks 1 CPOB: Pembuatan Produk Steril & Contamination Control Strategy (CCS)

Dokumen ini memuat panduan komprehensif terkait revisi **Aneks 1 CPOB (Pembuatan Produk Steril)** yang diharmonisasikan secara penuh dengan **PIC/S GMP Annex 1**.

---

## 1. Prinsip Utama: Contamination Control Strategy (CCS)

Revisi CPOB untuk produk steril mewajibkan setiap industri farmasi menyusun dokumen **Contamination Control Strategy (CCS)** yang holistik dan terdokumentasi aktif (*living document*).

CCS harus mengintegrasikan 16 elemen pengendalian kontaminasi mikroba, endotoksin/pirogen, dan partikulat:

1. **Desain Pabrik dan Proses Manufaktur**: Tata letak ruang, pola aliran udara, dan pemisahan personil/material.
2. **Kualifikasi Bangunan dan Fasilitas**: Sistem tata udara (HVAC/AHU), airlock, pass-box.
3. **Peralatan dan Proses**: Desain sanitasi peralatan, Clean-in-Place (CIP), Sterilization-in-Place (SIP).
4. **Personil**: Pelatihan teknik aseptis, kualifikasi gowning/pakaian kerja steril, dan pemantauan mikrobiologi personil.
5. **Sistem Utilitas Kritis**: Air untuk Injeksi (WFI), steam murni, udara bertekanan, dan gas nitrogen.
6. **Kontrol Bahan Baku & Bahan Pengemas**: Bioburden dan endotoksin bahan aktif serta wadah primer (vial/ampul/stopper).
7. **Persetujuan Pemasok (Vendor Qualification)**: Pengawasan mutu rantai pasok material steril.
8. **Pengendalian Bahan Baku yang Disterilkan**: Siklus sterilisasi uap panas, panas kering, atau radiasi tervalidasi.
9. **Validasi Pembersihan dan Desinfeksi**: Rotasi desinfektan sprosidal dan pemantauan residu pembersih.
10. **Sistem Pemantauan Lingkungan (EMS)**: Partikulat non-viabel kontinu dan pemantauan mikroba viabel.
11. **Batas Tindakan dan Peringatan (Alert & Action Limits)**: Investigasi akar masalah (RCA) jika terjadi tren kenaikan kontaminasi.
12. **Simulasi Proses Aseptis (Media Fill / APS)**: Uji media pengisi minimal tiap 6 bulan per shift/lini.
13. **Manajemen Risiko Mutu (QRM)**: Formalisasi FMEA / HACCP untuk titik-titik kritis aseptis.
14. **Tindakan Perbaikan dan Pencegahan (CAPA)**: Efektivitas tindak lanjut temuan kontaminasi.
15. **Continuous Improvement**: Pengkajian tren mutu berkala.
16. **Pengendalian Pasca-Sterilisasi**: Integritas wadah penutup (Container Closure Integrity - CCI).

---

## 2. Klasifikasi Ruang Bersih (Cleanroom Classification)

| Kelas / Grade | Kondisi Non-Operasional (At Rest) | Kondisi Operasional (In Operation) | Batas Mikrobiologis Udara (CFU/m³) | Batas Cawan Papar (CFU/4 jam) |
| :--- | :--- | :--- | :--- | :--- |
| **Grade A** (Zona Kritis Aseptis) | $\le 3.520$ partikel/m³ ($\ge 0.5\ \mu\text{m}$)<br/>$0$ partikel/m³ ($\ge 5.0\ \mu\text{m}$) | $\le 3.520$ partikel/m³ ($\ge 0.5\ \mu\text{m}$)<br/>$0$ partikel/m³ ($\ge 5.0\ \mu\text{m}$) | **$< 1$ CFU** (Target Nol) | **$< 1$ CFU** (Target Nol) |
| **Grade B** (Latar Belakang Grade A) | $\le 3.520$ partikel/m³ ($\ge 0.5\ \mu\text{m}$)<br/>$0$ partikel/m³ ($\ge 5.0\ \mu\text{m}$) | $\le 352.000$ partikel/m³ ($\ge 0.5\ \mu\text{m}$)<br/>$\le 2.900$ partikel/m³ ($\ge 5.0\ \mu\text{m}$) | **$10$ CFU** | **$5$ CFU** |
| **Grade C** (Preparasi Larutan & Filtrasi) | $\le 352.000$ partikel/m³ ($\ge 0.5\ \mu\text{m}$)<br/>$\le 2.900$ partikel/m³ ($\ge 5.0\ \mu\text{m}$) | $\le 3.520.000$ partikel/m³ ($\ge 0.5\ \mu\text{m}$)<br/>$\le 29.000$ partikel/m³ ($\ge 5.0\ \mu\text{m}$) | **$100$ CFU** | **$50$ CFU** |
| **Grade D** (Pembersihan Komponen Wadah) | $\le 3.520.000$ partikel/m³ ($\ge 0.5\ \mu\text{m}$)<br/>$\le 29.000$ partikel/m³ ($\ge 5.0\ \mu\text{m}$) | Tidak Ditetapkan Batasnya | **$200$ CFU** | **$100$ CFU** |

---

## 3. Ketentuan PUPSIT (Pre-Use Post-Sterilization Integrity Testing)

1. **Definisi**: Pengujian integritas filter penahan mikroba ($0.22\ \mu\text{m}$) yang dilakukan **setelah disterilkan** (misal via autoklaf/SIP) dan **sebelum digunakan** untuk penyaringan larutan steril, serta diulang kembali setelah proses pengisian selesai.
2. **Tujuan**: Mendeteksi kerusakan mikroskopis pada membran filter (misal akibat thermal stress saat siklus sterilisasi panas) yang mungkin tidak terdeteksi jika hanya diuji setelah filtrasi akibat penyumbatan pori oleh partikel produk.
3. **Pengecualian Berbasis Risiko**:
   - Jika PUPSIT tidak memungkinkan secara teknis (misal volume sediaan sangat kecil atau cairan berbusa tinggi), industri harus melampirkan **Kajian Risiko Mutu Komprehensif (QRM)** yang membuktikan validasi sterilisasi filter dan pemantauan bioburden pra-filtrasi yang sangat ketat.

---

## 4. Teknologi Penghalang: Isolator vs. RABS

Revisi CPOB sangat mendorong transisi dari LAF konvensional terbuka ke teknologi penghalang canggih:
- **Isolator**: Sistem tertutup total dengan dekontaminasi gas otomatis ($H_2O_2$ uap / VHP), tekanan positif terhadap ruang sekitar, dan sarung tangan terintegrasi dengan leak test otomatis.
- **RABS (Restricted Access Barrier Systems)**: Sistem pembatas fisik semi-tertutup dengan aliran udara satu arah (unidirectional flow) yang memisahkan operator dari zona kritis Grade A.
