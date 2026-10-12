# Cross-Jurisdiction Regulatory Comparison Example

This document demonstrates how to execute a multi-agency regulatory comparison under the `pharma-regulatory-helper` skill, benchmarking **BPOM (Indonesia)** against the **US FDA**, **EMA (European Union)**, and **ICH Guidelines**.

---

## 1. Comparative Analysis: Finished Product Stability Requirements

| Parameter | BPOM (Indonesia) | US FDA (United States) | EMA (European Union) | ICH Harmonized Baseline |
| :--- | :--- | :--- | :--- | :--- |
| **Climatic Zone** | **Zone IVb** (Hot & very humid) | **Zone I / II** (Temperate / Mediterranean) | **Zone I / II** (Temperate) | **ICH Q1A(R2)** (Zones I to IVb) |
| **Long-Term Testing Condition** | **$30^\circ\text{C} \pm 2^\circ\text{C} \ / \ 75\% \pm 5\% \text{RH}$** | $25^\circ\text{C} \pm 2^\circ\text{C} \ / \ 60\% \pm 5\% \text{RH}$ (atau $30^\circ\text{C}/65\%\text{ RH}$) | $25^\circ\text{C} \pm 2^\circ\text{C} \ / \ 60\% \pm 5\% \text{RH}$ | $25^\circ\text{C}/60\%\text{ RH}$ (Z-I/II) atau $30^\circ\text{C}/75\%\text{ RH}$ (Z-IVb) |
| **Accelerated Testing Condition** | **$40^\circ\text{C} \pm 2^\circ\text{C} \ / \ 75\% \pm 5\% \text{RH}$** | $40^\circ\text{C} \pm 2^\circ\text{C} \ / \ 75\% \pm 5\% \text{RH}$ | $40^\circ\text{C} \pm 2^\circ\text{C} \ / \ 75\% \pm 5\% \text{RH}$ | $40^\circ\text{C} \pm 2^\circ\text{C} \ / \ 75\% \pm 5\% \text{RH}$ |
| **Minimum Real-Time Data at Filing** | **12 Bulan** (Wajib Zone IVb) | **12 Bulan** (Zone I/II) | **6 - 12 Bulan** (Zone I/II tergantung status) | **12 Bulan** (Standar umum) |
| **Dossier Section** | ACTD Part II.C.11 | ICH CTD Module 3 (3.2.P.8) | ICH CTD Module 3 (3.2.P.8) | CTD Module 3.2.P.8 |
| **Regulatory Impact for Global Transfer** | Stabilitas global Zone II **tidak diakui**; wajib menyertakan data Zone IVb spesifik kemasan primer pasar Indonesia. | Menerima data Zone II untuk peredaran domestik AS. | Menerima data Zone II untuk peredaran di wilayah EEA. | Memberikan prinsip umum tanpa memaksakan zonasi tunggal. |

---

## 2. Comparative Analysis: Nitrosamine Impurity Risk Management

| Parameter | BPOM (Indonesia) | US FDA (United States) | EMA (European Union) | ICH Standard |
| :--- | :--- | :--- | :--- | :--- |
| **Governing Document** | Surat Edaran BPOM No. PW.01.07.3.34.05.21.32 tentang Pengawalan Mutu Obat Terkait Cemaran Nitrosamin | FDA Guidance for Industry: *Control of Nitrosamine Impurities in Human Drugs* (Rev 1) | EMA/409815/2020: *Questions and answers for marketing authorisation holders* | **ICH M7(R2)** (Assessment and Control of DNA Reactive Mutagenic Impurities) |
| **Default Acceptable Intake (AI)** | $26.5\text{ ng/hari}$ (jika tidak ada data toksikologis spesifik zat) | $26.5\text{ ng/hari}$ (Threshold of Toxicological Concern - TTC) | $26.5\text{ ng/hari}$ (TTC default class-specific) | Mengacu pada konsep TTC ($1.5\ \mu\text{g/hari}$ untuk mutagenik umum; $26.5\text{ ng}$ untuk kelompok berpotensi tinggi) |
| **Risk Assessment Requirement** | Wajib dilakukan pada registrasi baru dan evaluasi CPOB berkala untuk semua API sintetis. | Wajib melampirkan *Confirmatory Testing* jika teridentifikasi risiko pada Step 1. | Wajib melakukan Call for Review Step 1, 2, dan 3 untuk seluruh sediaan obat. | Terintegrasi dalam kontrol strategi impuritas API & FPP. |

---

## 3. Practical Harmonization Takeaways

1. **Dual Stability Strategy**: Industri farmasi multinasional atau lokal yang menargetkan ekspor ke negara ASEAN (Indonesia, Malaysia, Vietnam, Filipina) harus mendesain protokol stabilitas sejak awal menggunakan **kondisi ganda (Zone II dan Zone IVb)** guna menghindari penundaan registrasi akibat kekurangan durasi pengujian 12 bulan di Zone IVb.
2. **Dossier Conversion (ICH CTD to ACTD)**:
   - Module 2 (Overviews) harus dilebur ke dalam ringkasan pembuka masing-masing Bagian ACTD (misal: QOS masuk ke Bagian II.A).
   - Module 1 FDA/EMA harus diadaptasi total ke dalam format Bagian I ACTD dengan bahasa Indonesia pada Informasi Produk (PIL) dan etiket.
