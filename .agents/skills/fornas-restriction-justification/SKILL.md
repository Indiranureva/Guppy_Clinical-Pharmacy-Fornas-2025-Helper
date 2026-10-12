---
name: fornas-restriction-justification
description: Membantu agent menilai kesesuaian antara restriksi penggunaan obat Fornas (Formularium Nasional) dengan diagnosis/kondisi klinis pasien, dan menyusun justifikasi yang terstruktur, dapat diaudit, serta aman ketika kondisi lapangan tidak sesuai aturan baku (data tidak lengkap, gawat darurat, lini 1 gagal, komorbid, populasi khusus, peresepan maksimal terlampaui, stok kosong, obat di luar Fornas). Gunakan skill ini setiap kali pengguna menyebut Fornas, restriksi obat, peresepan maksimal, kesesuaian obat-diagnosis, verifikasi resep JKN/BPJS, validasi klaim obat, rule engine formularium, override/justifikasi resep, notifikasi/alert/pengingat terkait resep atau justifikasi Fornas, atau meminta desain/logika justifikasi pada aplikasi farmasi/CDSS, walaupun tidak menyebut kata "justifikasi" secara eksplisit.
---

# Justifikasi Restriksi Fornas

Skill ini membuat agent mampu (1) mencocokkan restriksi Fornas dengan data pasien secara teliti, dan (2) ketika hasilnya tidak cocok, menentukan **apakah ada alasan sah untuk menyimpang**, alasan apa, bukti apa yang dibutuhkan, dan siapa yang berwenang menyetujui.

## Prinsip dasar (baca dulu, ini yang membedakan hasil bagus dan buruk)

1. **Restriksi adalah alat kendali mutu dan biaya, bukan larangan klinis.** Dokter tetap pengambil keputusan terapi. Tugas agent: memastikan penyimpangan *terdokumentasi, beralasan, dan dapat ditinjau*, bukan menghalangi terapi yang dibutuhkan pasien.
2. **Data kosong bukan berarti tidak sesuai.** Pakai logika tiga nilai per kriteria: `TERPENUHI`, `TIDAK_TERPENUHI`, `TIDAK_DIKETAHUI`. Memperlakukan "tidak diketahui" sebagai "gagal" menghasilkan banyak penolakan palsu dan membuat pengguna mengisi asal-asalan.
3. **Agent tidak boleh mengarang fakta klinis.** Setiap butir justifikasi harus menunjuk ke field data pasien (diagnosis, hasil lab, riwayat obat, dsb.). Jika bukti tidak ada, minta datanya; jangan menyimpulkan.
4. **Justifikasi tidak boleh menjadi jalan memutar.** Jangan pernah menyarankan mengubah/menambah diagnosis agar lolos restriksi. Diagnosis hanya boleh berubah karena temuan klinis baru atau koreksi kesalahan input yang terbukti. Lihat bagian "Pola yang harus ditandai".
5. **Agent merekomendasikan, manusia memutuskan.** Keputusan akhir ada pada dokter penulis resep, apoteker, atau Komite/Tim Farmasi dan Terapi (KFT) sesuai tingkat risiko. Agent tidak melakukan persetujuan final untuk kasus berisiko.
6. **Jangan menghafal isi restriksi.** Isi Fornas diperbarui berkala. Selalu ambil teks restriksi dari sumber data aplikasi (versi Fornas aktif) dan catat versinya pada output. Jika teks restriksi tidak tersedia, katakan begitu dan berhenti pada status `DATA_KURANG`. Jalur regulasi (mis. mekanisme obat di luar Fornas, batas waktu justifikasi gawat darurat) harus diverifikasi ke Kepmenkes Fornas yang berlaku dan aturan BPJS Kesehatan terbaru, karena berbeda antar versi.

## Alur kerja

### Langkah 1. Pecah restriksi menjadi kriteria atomik

Teks restriksi biasanya berisi beberapa syarat sekaligus. Pecah menjadi kriteria terpisah, masing-masing dengan operator `DAN`/`ATAU`:

| Jenis kriteria | Contoh bentuk |
|---|---|
| Diagnosis / indikasi | kode ICD-10 atau frasa klinis |
| Derajat / stadium | NYHA, GOLD, HbA1c, eGFR, skor tertentu |
| Lini terapi | "setelah gagal dengan..." / "bila kontraindikasi..." |
| Populasi | usia, berat badan, kehamilan |
| Penulis resep | spesialis tertentu / dokter terlatih |
| Fasilitas | FKTP vs FKRTL / kelas fasilitas |
| Kuantitas | peresepan maksimal (jumlah, hari, per kunjungan) |
| Syarat penunjang | hasil lab/pemeriksaan wajib, persetujuan tertentu |

**Struktur restriksi Fornas** (diverifikasi pada KMK HK.01.07/MENKES/1199/2025; cek ulang bila ada edisi atau adendum baru):
- Restriksi dapat tertulis pada tiga tingkat: **kelas/subkelas terapi** (berlaku untuk semua item di kelas itu), **nama zat aktif** (semua kekuatan dan sediaan), atau **kekuatan/sediaan tertentu** (hanya sediaan itu). Selalu gabungkan ketiga tingkat saat menilai satu sediaan.
- Satu zat aktif dapat tercantum di beberapa kelas terapi sesuai indikasi. Tanpa indikasi/kelas, entri yang berlaku belum bisa dipilih; itu `DATA_KURANG`, bukan salah satu entri dipilih sembarang.
- Peresepan maksimal ditulis per kekuatan/sediaan dan kadang berbeda per tingkat fasilitas (FPKTP vs FPKTL). Selnya bisa menyatu untuk beberapa sediaan.
- Kolom fasilitas: centang FPKTP/FPKTL; "PP" = Puskesmas Perawatan; tanda `*` = dapat diberikan FPKTP/apotek PRB untuk program rujuk balik (centang bintang: initial treatment di FPKTL); `[P]` = pengadaan program Kemenkes/BKKBN; `[Ca]` = terapi kanker; centang OEN = obat esensial nasional.
- Obat di luar Fornas (Diktum KELIMA edisi itu): obat lain dapat dipakai secara terbatas atas persetujuan kepala/direktur fasilitas pelayanan kesehatan setempat sesuai peraturan perundang-undangan.
- Teks restriksi klinis jangan ditafsirkan mesin sebagai kode ICD-10 tanpa tinjauan apoteker/KFT. Pemetaan otomatis hanya berstatus usulan.

Beri setiap kriteria **sifat restriksi** karena ini menentukan seberapa ketat justifikasi dan siapa yang harus dilibatkan:

| Sifat | Contoh | Konsekuensi |
|---|---|---|
| `keselamatan` | batas usia, kehamilan, fungsi ginjal/hati, kontraindikasi | Penyimpangan minimal perlu apoteker dan umumnya KFT; tidak pernah lolos otomatis; peringatan keselamatan selalu ditampilkan |
| `kendali_biaya` | syarat gagal lini 1, spesialis tertentu, peresepan maksimal | Apoteker cukup bila bukti objektif ada |
| `administratif` | fasilitas, kelengkapan dokumen | Dapat otomatis atau retrospektif |

Bila sifatnya tidak jelas dari teks, anggap `keselamatan` (pilihan yang lebih hati-hati) dan tandai `ambigu: true`.

Simpan sebagai struktur (lihat `references/skema-data.md`). Untuk teks yang ambigu, tandai `ambigu: true` dan jangan memaksakan tafsir; eskalasikan ke apoteker/KFT.

### Langkah 2. Normalisasi data pasien

- Cocokkan diagnosis pada **tingkat kode dan hierarki ICD-10** (induk ke turunan), bukan hanya string. Sertakan diagnosis sekunder dan komorbid, bukan hanya diagnosis utama.
- Pisahkan **diagnosis kerja** (sementara) dari **diagnosis definitif**; catat tanggal dan sumbernya.
- Satukan satuan (mg/dL vs mmol/L, kg, tahun/bulan), dan beri **usia data** pada hasil lab (hasil 14 bulan lalu mungkin tidak lagi valid untuk kriteria tertentu).
- Ambil riwayat obat dan lama pemakaian untuk menilai kriteria "lini 1 gagal".

### Langkah 3. Evaluasi tiap kriteria

Beri status tiga nilai plus **bukti** (field + nilai + tanggal) dan **alasan singkat**. Gabungkan sesuai operator.

### Langkah 4. Tentukan status keseluruhan

| Status | Kondisi | Tindakan aplikasi |
|---|---|---|
| `SESUAI` | Semua kriteria terpenuhi | Lanjut, tanpa gesekan |
| `DATA_KURANG` | Tidak ada yang gagal, tetapi ada yang tidak diketahui | Minta data spesifik yang kurang (sebutkan persis apa); jangan blok bila terapi mendesak |
| `PERLU_JUSTIFIKASI` | Ada kriteria gagal, dan ada kategori justifikasi sah yang mungkin berlaku | Tampilkan kode alasan yang relevan + bukti wajib (Langkah 5) |
| `TIDAK_SESUAI` | Ada kriteria gagal dan tidak ada kategori justifikasi yang masuk akal dari data yang ada | Sarankan alternatif Fornas yang sesuai, atau rute persetujuan khusus |
| `ESKALASI` | Restriksi ambigu, data bertentangan, atau pola mencurigakan | Serahkan ke apoteker/KFT dengan ringkasan |

### Langkah 5. Pilih kategori justifikasi

Gunakan **kode alasan terstruktur**, bukan teks bebas, sebagai jalur utama. Teks bebas hanya pelengkap. Alasan: kode bisa divalidasi, diaudit, dan dianalisis tren; teks bebas cenderung berisi "sesuai kebutuhan pasien" yang tidak bernilai.

Ringkasan kategori (rincian bukti wajib, pemberi persetujuan, dan masa berlaku ada di `references/katalog-justifikasi.md`, **baca file itu sebelum menyusun justifikasi**):

| Kode | Kapan dipakai |
|---|---|
| `DATA_TIDAK_LENGKAP` | Kriteria kemungkinan terpenuhi, tetapi belum terdokumentasi |
| `LINI_1_GAGAL` | Terapi lini sebelumnya tidak efektif (dosis dan durasi memadai) |
| `INTOLERANSI_ALERGI` | Efek samping bermakna / alergi pada alternatif Fornas |
| `KONTRAINDIKASI` | Alternatif Fornas dikontraindikasikan pada pasien ini |
| `INTERAKSI_OBAT` | Alternatif menimbulkan interaksi bermakna dengan terapi berjalan |
| `POPULASI_KHUSUS` | Anak, geriatri, hamil/menyusui, gangguan hati/ginjal |
| `KOMORBID` | Komorbid mengubah pilihan terapi yang layak |
| `PERBURUKAN_KLINIS` | Kondisi memburuk melewati ambang kriteria saat ini |
| `DIAGNOSIS_BERUBAH` | Diagnosis kerja menjadi definitif, atau ditemukan temuan baru |
| `GAWAT_DARURAT` | Terapi segera menyelamatkan nyawa / mencegah kecacatan |
| `PERESEPAN_MAKS_LEBIH` | Melebihi batas jumlah/hari (titrasi, berat badan, rujuk balik, perjalanan) |
| `RUJUK_BALIK` | Kelanjutan terapi yang diinisiasi spesialis di fasilitas lain |
| `STOK_KOSONG` | Alternatif Fornas tidak tersedia saat dibutuhkan |
| `OFF_LABEL_BERBASIS_BUKTI` | Indikasi di luar restriksi, didukung pedoman/bukti |
| `OBAT_LUAR_FORNAS` | Tidak ada alternatif Fornas yang memadai |
| `KOREKSI_ADMINISTRATIF` | Salah input kode/data yang terbukti dari rekam medis |
| `LAINNYA` | Tidak masuk kategori; wajib narasi dan otomatis eskalasi |

Aturan memilih:
- Pilih hanya kode yang **didukung data**. Satu kasus boleh punya beberapa kode (mis. `INTOLERANSI_ALERGI` + `KOMORBID`).
- Urutkan dari yang paling kuat buktinya. Jangan menyodorkan semua kode ke dokter.
- Bila bukti wajib suatu kode belum ada, status tetap `PERLU_JUSTIFIKASI` dan agent mencantumkan **bukti apa yang masih kurang**.

### Langkah 6. Tingkatkan akurasi lewat verifikasi silang

Sebelum mengeluarkan hasil, jalankan pemeriksaan ini:

1. **Konsistensi**: apakah diagnosis, obat, dosis, usia, dan hasil lab saling masuk akal? (mis. obat untuk dewasa pada pasien 4 tahun, dosis di atas rentang wajar.)
2. **Kronologi**: apakah tanggal diagnosis, hasil lab, dan mulai obat berurutan wajar? Diagnosis yang muncul tepat setelah resep ditolak adalah sinyal.
3. **Alternatif Fornas**: apakah ada obat Fornas lain untuk indikasi ini yang memenuhi restriksi dan layak secara klinis? Sebutkan, agar dokter dapat memilih tanpa justifikasi. **Nama alternatif hanya boleh berasal dari daftar Fornas/formularium di data aplikasi**, bukan dari ingatan agent. Jika daftar tidak tersedia, tulis "daftar alternatif tidak tersedia dari sumber data" dan minta apoteker memeriksa.
4. **Kualitas bukti**: bedakan bukti objektif (hasil lab, rekam riwayat obat) dari pernyataan bebas. Bobot bukti objektif lebih tinggi.
5. **Keamanan dahulu**: jika ada potensi bahaya pasien (alergi, kontraindikasi, interaksi berat), angkat sebagai peringatan terpisah, di luar urusan restriksi.

## Pola yang harus ditandai (jangan dilolosan diam-diam)

Tandai sebagai `ESKALASI` dan jelaskan polanya, tanpa menuduh. Sebuah pola baru boleh disebut **temuan** bila ada data pembanding (unit/dokter sejenis, periode sebelumnya). Tanpa pembanding, catat hanya sebagai **pengamatan** ("terlihat 9 kali dalam 30 hari; belum ada pembanding") dan minta apoteker/KFT menilai konteksnya, karena angka yang sama bisa wajar di unit tertentu:
- Diagnosis berubah atau ditambah mendekati waktu penolakan resep, tanpa temuan klinis baru.
- Penggunaan kode `GAWAT_DARURAT` berulang oleh penulis/unit yang sama untuk kasus rawat jalan stabil.
- `DATA_TIDAK_LENGKAP` dipakai berulang pada pasien yang sama tanpa data pernah dilengkapi.
- Peresepan mendekati/menyentuh batas maksimal secara konsisten lalu "diperpanjang" lewat `PERESEPAN_MAKS_LEBIH`.
- Teks justifikasi identik (salin-tempel) pada banyak pasien berbeda.
- Hasil lab pendukung yang tidak konsisten dengan diagnosis atau tanggalnya tidak masuk akal.

Jika pengguna meminta agent menyusun alasan agar suatu resep "lolos" padahal data tidak mendukung, tolak dengan sopan dan tawarkan jalur sah: lengkapi data, pilih alternatif Fornas, atau ajukan persetujuan khusus.

## Komunikasi saat ada tekanan

Pengguna sering menulis "pasien sangat butuh" atau "ini darurat". Tekanan itu valid secara emosional, tetapi bukan bukti klinis. Tanggapi dengan: (1) akui urgensinya dalam satu kalimat, (2) langsung tunjukkan jalur tercepat yang sah (mis. `GAWAT_DARURAT` retrospektif bila memenuhi), (3) sebutkan bukti apa yang cukup. Jangan melunakkan standar bukti, dan jangan ceramah.

**Urgensi tidak diketahui pada restriksi `keselamatan`.** Jangan berasumsi kondisi pasien tidak akut. Ajukan satu pertanyaan singkat: "Apakah kondisi ini mengancam nyawa atau kecacatan saat ini?" Sambil menunggu jawaban, kirim notifikasi `KRITIS` ke apoteker jaga dengan permintaan respons cepat, dan jangan menahan terapi yang mungkin darurat. Jika pertanyaan tidak bisa dijawab (tidak ada pengguna), tandai `dapat_menunda_terapi: false` dan eskalasikan ke apoteker/KFT, bukan menyimpulkan sendiri.

## Notifikasi

Setiap hasil evaluasi menghasilkan nol, satu, atau beberapa notifikasi. Notifikasi yang buruk membuat orang mengabaikan semuanya (alert fatigue), jadi tujuannya sedikit tetapi bisa ditindaklanjuti. **Baca `references/notifikasi.md` sebelum menyusun notifikasi**; berikut aturan intinya:

1. **Penerima sesuai peran.** Penulis resep menerima hal yang bisa ia lengkapi sekarang; apoteker menerima antrean persetujuan dan tenggat; KFT menerima restriksi keselamatan, kasus ambigu, pola yang ditandai, dan tren berkala.
2. **Tingkat keparahan menentukan saluran.** `KRITIS` (keselamatan pasien) in-app langsung dan tidak bisa ditutup tanpa diakui; `PENTING` (perlu tindakan hari ini) in-app; `INFO` dikumpulkan dalam ringkasan.
3. **Satu notifikasi, satu tindakan.** Isi: apa yang terjadi, data persis yang kurang, tindakan berikutnya, tenggat. Jangan mengulang teks restriksi panjang.
4. **Tidak ada notifikasi kalau tidak ada yang perlu dilakukan.** Status `SESUAI` dan justifikasi yang masih berlaku tidak memicu apa-apa (cukup tercatat di jejak audit).
5. **Peringatan keselamatan selalu terpisah dan tidak bisa ditekan oleh justifikasi.** Justifikasi restriksi tidak menghapus alert alergi, kontraindikasi, atau interaksi berat.
6. **Pola yang ditandai dikirim ke apoteker/KFT, bukan ke penulis resep, dengan bahasa netral dan faktual.** Penulis resep cukup menerima permintaan melengkapi data. Jangan menyiratkan tuduhan.
7. **Jalur gawat darurat tidak pernah menahan terapi.** Notifikasinya berupa pengingat retrospektif bertahap (awal, mendekati tenggat, lewat tenggat), bukan penghalang.
8. **Privasi.** Notifikasi di luar aplikasi (email, pesan singkat) hanya berisi ID rujukan dan jenis tindakan, tanpa nama pasien atau diagnosis.
9. **Catat hasil notifikasi** (dibuka, ditindaklanjuti, diabaikan, ditolak). Pola diabaikan yang tinggi berarti notifikasi terlalu berisik; ringkas dan beri tahu KFT.
10. **Saat diminta menyetel notifikasi yang terlalu berisik, minta log dulu.** Mintalah distribusi notifikasi per jenis, tingkat, penerima, dan hasil tindak lanjut sebelum mengusulkan perubahan. Tanpa data itu, beri usulan sementara berbasis prinsip dan tandai sebagai belum terukur; jangan mengarang target angka.
11. **Jangan membuat notifikasi dari data yang tidak ada.** Jika agent tidak tahu penerima, tenggat, atau kebijakan fasilitas, isi dengan default dari `references/notifikasi.md` dan tandai sebagai asumsi.

## Format keluaran

Keluarkan JSON sesuai `references/skema-data.md`, diikuti ringkasan 2 sampai 4 kalimat bahasa Indonesia untuk penulis resep/apoteker. Ringkasan harus menjawab: *status apa, kenapa, apa yang perlu dilakukan berikutnya.* Hindari jargon sistem. Contoh nada:

> Obat X memiliki restriksi indikasi Y. Diagnosis utama pasien belum memenuhi, namun hasil lab tanggal 12/09 menunjukkan ... yang memenuhi kriteria alternatif. Kode alasan yang sesuai: `LINI_1_GAGAL`. Mohon lampirkan lama dan dosis terapi sebelumnya; setelah itu resep dapat dilanjutkan dengan persetujuan apoteker.

## Rekomendasi desain untuk aplikasi (saat pengguna meminta desain, bukan evaluasi kasus)

Jika pengguna sedang merancang fiturnya, bukan mengevaluasi satu kasus, gunakan panduan ini:

- **Tingkatkan gesekan secara proporsional dengan risiko.** Tiga tingkat: (a) lolos otomatis, (b) peringatan lunak dengan kode alasan satu klik, (c) persetujuan apoteker/KFT. Jangan membuat semua kasus menjadi tingkat (c).
- **Jalur gawat darurat tidak boleh memblok terapi.** Izinkan lanjut dengan kode `GAWAT_DARURAT`, lalu wajibkan kelengkapan dokumentasi dalam jendela waktu yang dikonfigurasi (retrospektif) dan tinjauan berkala.
- **Justifikasi punya masa berlaku.** Untuk terapi kronis, justifikasi yang disetujui berlaku per periode (atau sampai kondisi berubah), bukan seumur hidup, dan tidak perlu diulang tiap kunjungan selama masih berlaku.
- **Pakai templat justifikasi per obat/restriksi** yang meminta persis bukti yang relevan (mis. riwayat lini 1, lab tertentu).
- **Catat jejak audit lengkap**: versi Fornas, teks restriksi, data yang dipakai, kode alasan, siapa menyetujui, kapan.
- **Umpan balik ke aturan.** Jika satu restriksi sering memicu justifikasi sah yang sama, itu sinyal bahwa aturan di aplikasi terlalu sempit atau data wajib kurang. Ringkas tren ini untuk KFT, termasuk bahan usulan peninjauan kepada pihak yang berwenang.
- **Uji dengan kasus tepi**, bukan hanya kasus umum (lihat `evals/evals.json`).

### Format keluaran untuk permintaan desain

Agar jawaban konsisten, susun dalam urutan: (1) kode alasan yang perlu disediakan, (2) alur persetujuan per tingkat risiko, (3) aturan notifikasi, (4) jejak audit dan umpan balik, (5) hal yang harus diverifikasi ke regulasi/kebijakan fasilitas. Sertakan satu contoh kasus tepi.

## Batasan

- Agent tidak memberi keputusan terapi atau dosis, dan tidak menggantikan dokter, apoteker, maupun KFT.
- Agent tidak menyatakan sebuah penyimpangan "pasti diterima" oleh penjamin/BPJS; ia hanya menilai kelengkapan dan kewajaran justifikasi menurut data yang ada.
- Bila regulasi yang berlaku tidak dapat diverifikasi, katakan terus terang dan tandai langkah yang perlu dicek manual.
