# Aneks 8 CPOB: Kualifikasi dan Validasi Proses Manufaktur

Panduan ini memuat ketentuan teknis pelaksanaan validasi proses pembuatan sediaan farmasi sesuai **Aneks 8 CPOB 2018** (jo. PIC/S PE 009-14 Annex 15).

---

## 1. Pendekatan Validasi Proses CPOB

CPOB mengakui tiga pendekatan dalam kualifikasi kinerja proses (Process Performance Qualification - PPQ):

### A. Pendekatan Tradisional (Traditional Approach)
- **Persyaratan**: Dilakukan sekurang-kurangnya pada **3 (tiga) bets berturut-turut** yang dibuat pada kondisi komersial rutin.
- **Kondisi Bets**: Menggunakan bahan baku yang telah disetujui, peralatan tervalidasi, personil terkualifikasi, dan ukuran bets skala komersial penuh.
- **Kriteria Keberhasilan**: Seluruh atribut mutu kritis (CQA) memenuhi spesifikasi dengan variabilitas proses yang dapat diterima secara statistik (RSD / standard deviation konsisten).

### B. Verifikasi Proses Kontinu (Continuous Process Verification - CPV)
- Menggunakan teknologi analisis proses (*Process Analytical Technology* - PAT) dan kontrol proses otomatis untuk memantau CQA dan CPP secara *real-time* atau *in-line*.
- Cocok untuk manufaktur berkesinambungan (*continuous manufacturing*) atau proses granulasi/blending dengan sensor NIR (Near-Infrared).

### C. Pendekatan Hibrida (Hybrid Approach)
- Kombinasi pendekatan tradisional untuk tahapan proses tertentu dan CPV untuk tahapan kritis lainnya (misal: validasi pencampuran dengan NIR, dilanjutkan 3 bets komersial untuk pencetakan tablet).

---

## 2. Parameter Kritis Proses (CPP) vs. Atribut Mutu Kritis (CQA)

| Kategori | Definisi | Contoh Parameter dalam Formulasi Padat (Tablet) |
| :--- | :--- | :--- |
| **Critical Quality Attribute (CQA)** | Sifat atau karakteristik fisik, kimia, biologi, atau mikrobiologi yang harus berada dalam batas spesifikasi untuk memastikan mutu produk. | - Kadar Zat Aktif (Assay: 95.0% - 105.0%)<br/>- Keseragaman Sediaan (Uniformity of Dosage Units AV $\le 15.0$)<br/>- Laju Disolusi ($Q \ge 75\%$ dalam 30 menit)<br/>- Kekerasan, Kerapuhan ($< 1.0\%$), dan Waktu Hancur |
| **Critical Process Parameter (CPP)** | Parameter proses yang variasinya berdampak langsung terhadap atribut mutu kritis (CQA). | - Kecepatan Putaran Pengaduk (Impeller Speed)<br/>- Waktu Pencampuran Granulasi Basah<br/>- Suhu Udara Masuk & Laju Semprot pada Fluid Bed Dryer<br/>- Tekanan Kompresi Mesin Cetak Tablet (Pre & Main Compression Force) |

---

## 3. Verifikasi Proses On-Going (Ongoing Process Verification - OPV)

- Validasi proses tidak berakhir setelah 3 bets selesai.
- Industri farmasi wajib memantau mutu produk sepanjang siklus hidup komersial (*product lifecycle*).
- Menghitung kapabilitas proses secara berkala:
  $$C_{pk} = \min\left( \frac{\text{USL} - \mu}{3\sigma}, \frac{\mu - \text{LSL}}{3\sigma} \right)$$
  - Target ideal: $C_{pk} \ge 1.33$ membuktikan proses manufaktur berada dalam status terkendali (*statistically in control*).
