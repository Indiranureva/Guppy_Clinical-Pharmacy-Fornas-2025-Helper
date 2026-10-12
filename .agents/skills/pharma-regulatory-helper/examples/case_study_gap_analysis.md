# Case Study: Gap Analysis for Drug Registration (Metformin HCl 500 mg Film-Coated Tablet)

This example demonstrates how an AI agent operating under the `pharma-regulatory-helper` skill conducts a thorough regulatory assessment and gap analysis on a generic drug submission dossier targeted for BPOM Indonesia.

---

## 1. Case Profile

- **Product Name**: Metformin Hydrochloride 500 mg Film-Coated Tablet
- **Applicant**: PT Farma Sejahtera Indonesia
- **Category**: Registrasi Baru Obat Copy (Kategori 3)
- **Reference Inovator Product**: Glucophage® 500 mg (Merck)
- **Submitted Dossier**: ACTD Parts I, II, and IV

---

## 2. Regulatory Assessment & Gap Analysis Matrix

| ACTD Section | Dossier Submission State | BPOM Requirement & Legal Citation | Compliance Status | Gap Description & Regulatory Severity |
| :--- | :--- | :--- | :--- | :--- |
| **Part I.G (Packaging & Labeling)** | Mock-up blister & dus hanya mencantumkan barcode linear UPC standar. | **PerBPOM No. 31 Tahun 2018** & **PerBPOM No. 22 Tahun 2022**: Penandaan Obat wajib memuat 2D Barcode (QR Code) otentikasi BPOM dan NIE. | **NON-COMPLIANT** | **Moderate Severity**: Mock-up kemasan ditolak pada tahap Pra-Registrasi atau memicu PTD. Harus mengintegrasikan area pencetakan 2D barcode BPOM. |
| **Part II.C.11 (Stability Study)** | Data stabilitas diserahkan pada kondisi $25^\circ\text{C} \pm 2^\circ\text{C} / 60\% \pm 5\% \text{RH}$ selama 24 bulan (Zone II). | **PerBPOM No. 24 Tahun 2017 Lampiran 3** & **ASEAN Stability Guidelines**: Indonesia berada pada **Climatic Zone IVb ($30^\circ\text{C} \pm 2^\circ\text{C} / 75\% \pm 5\% \text{RH}$)**. Wajib menyertakan data riil Zone IVb minimal 12 bulan pada saat registrasi. | **CRITICAL GAP** | **Critical Severity (Showstopper)**: BPOM tidak menerima ekstrapolasi data Zone II untuk izin edar lokal. Risiko penolakan registrasi baru secara langsung. |
| **Part IV.C (Bioequivalence)** | Pemohon mengajukan permohonan pembebasan uji BE in vivo (Biowaiver) hanya berdasarkan klaim bahwa Metformin adalah obat yang sudah lama beredar. | **Peraturan KaBPOM HK.00.05.3.1818**: Metformin HCl oral lepas cepat merupakan produk yang wajib uji ekivalensi in vivo, kecuali memenuhi kriteria BCS Biowaiver secara ketat (BCS Kelas III). | **MAJOR GAP** | **High Severity**: Pembebasan uji BE ditolak tanpa adanya data kelarutan pada 3 rentang pH (1.2, 4.5, 6.8) dan profil disolusi terbanding ($f_2$) dengan produk inovator. |

---

## 3. Resolving the Biowaiver Gap via Scientific Literature Protocol (Q1–Q3)

Karena pemohon membutuhkan pembenaran ilmiah (*scientific rationale*) untuk mendukung pengajuan biowaiver BCS Kelas III Metformin HCl sesuai pedoman ICH M9 dan WHO Technical Report Series:

> 🔬 **Dasar Pembenaran Ilmiah (Scientific Rationale)**:
> - **Penulis & Tahun**: Cheng, C. L., Chou, C. H., et al., 2008
> - **Judul Artikel**: *"Biowaiver monographs for immediate release solid oral dosage forms: Metformin hydrochloride"*
> - **Jurnal & Peringkat**: *Journal of Pharmaceutical Sciences*, Vol. 97, No. 1, pp. 212–218 (Scopus **Q1**, Scimago H-index: 185)
> - **Identifikasi Unik**: DOI: `10.1002/jps.21077` | PubMed Central
> - **Temuan Kunci / Bukti Empiris**: Metformin HCl terbukti memiliki kelarutan yang sangat tinggi (dosis tertinggi 1000 mg larut dalam $< 250\text{ mL}$ media air pada pH 1.2 hingga 6.8). Meskipun merupakan senyawa BCS Kelas III (permeabilitas terbatas), biowaiver direkomendasikan secara ilmiah jika sediaan menunjukkan disolusi sangat cepat ($>85\%$ dalam 15 menit) dan formulasi menggunakan eksipien konvensional yang tidak mengganggu motilitas saluran cerna.
> - **Rekomendasi Dossier**: Melampirkan uji disolusi terbanding (*in vitro comparative dissolution*) terhadap Glucophage® pada media pH 1.2 (HCl), pH 4.5 (Dapar Asetat), dan pH 6.8 (Dapar Fosfat) yang membuktikan $Q \ge 85\%$ pada 15 menit untuk melengkapi Bagian IV.C ACTD.

---

## 4. Remediation Action Plan & Timelines

1. **Uji Stabilitas Ulang (Zone IVb)**:
   - Segera masukkan 3 bets pilot ke dalam *climatic chamber* Zone IVb ($30^\circ\text{C} \pm 2^\circ\text{C} / 75\% \pm 5\% \text{RH}$ dan kondisi dipercepat $40^\circ\text{C} / 75\% \text{RH}$).
   - **Timeline**: 6 bulan untuk data stabilitas dipercepat dan 12 bulan untuk data jangka panjang sebelum pengajuan registrasi.
2. **Kajian Disolusi Terbanding (UDT)**:
   - Jalankan uji disolusi terbanding 12 unit dosis vs. Glucophage® bets komparator resmi.
   - Evaluasi nilai $f_2$ (Similarity Factor) $\ge 50$ atau disolusi sangat cepat dalam 15 menit.
3. **Revisi Penandaan (Packaging Design)**:
   - Tambahkan placeholder QR code BPOM 2D dan logo lingkaran Obat Keras (K).
