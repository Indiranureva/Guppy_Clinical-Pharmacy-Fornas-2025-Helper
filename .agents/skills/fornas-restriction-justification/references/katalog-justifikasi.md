# Katalog Kategori Justifikasi

Dibaca agent saat menyusun justifikasi. Kolom "Persetujuan" dan "Masa berlaku" adalah **default yang disarankan** untuk aplikasi; sesuaikan dengan kebijakan fasilitas dan aturan Fornas/BPJS yang berlaku dan verifikasi sebelum dipakai sebagai fakta regulasi.

## Daftar isi
1. Cara membaca tabel
2. Kategori A: Dokumentasi dan administrasi
3. Kategori B: Klinis (terapi)
4. Kategori C: Kuantitas dan kontinuitas
5. Kategori D: Ketersediaan dan di luar formularium
6. Contoh penyusunan justifikasi
7. Tanda bukti lemah

## 1. Cara membaca tabel

- **Bukti wajib**: minimal yang harus ada di data/lampiran. Jika belum ada, status tetap `PERLU_JUSTIFIKASI` dan agent menyebut bukti yang kurang.
- **Persetujuan**: tingkat default (`Otomatis`, `Apoteker`, `KFT/Komite`, `Retrospektif`).
- **Risiko salah pakai**: apa yang perlu diwaspadai agent.

## 2. Kategori A: Dokumentasi dan administrasi

| Kode | Bukti wajib | Persetujuan | Masa berlaku | Risiko salah pakai |
|---|---|---|---|---|
| `DATA_TIDAK_LENGKAP` | Daftar kriteria berstatus `TIDAK_DIKETAHUI`; permintaan data spesifik | Otomatis (menunggu data) | Jendela pendek (mis. hingga kunjungan berikutnya) | Dipakai berulang tanpa data pernah dilengkapi |
| `KOREKSI_ADMINISTRATIF` | Dokumen rekam medis yang menunjukkan kode/entri benar, tanggal koreksi, siapa yang mengoreksi | Apoteker; audit | Sekali (koreksi data) | Mengubah diagnosis agar lolos restriksi; tandai bila koreksi muncul setelah penolakan |
| `DIAGNOSIS_BERUBAH` | Temuan baru (lab/pencitraan/konsultasi) dengan tanggal; diagnosis lama dan baru | Apoteker bila temuan objektif; KFT bila tidak ada | Selama diagnosis baru berlaku | Diagnosis ditambah tepat setelah penolakan tanpa temuan baru |

## 3. Kategori B: Klinis (terapi)

| Kode | Bukti wajib | Persetujuan | Masa berlaku | Risiko salah pakai |
|---|---|---|---|---|
| `LINI_1_GAGAL` | Nama obat lini sebelumnya, dosis, durasi, tanggal, alasan gagal (target tidak tercapai/perburukan) | Apoteker | Selama terapi lanjutan; tinjau berkala | Durasi/dosis tidak memadai (gagal semu) |
| `INTOLERANSI_ALERGI` | Reaksi yang tercatat (jenis, tanggal, obat pencetus), derajat | Apoteker | Panjang (alergi tercatat), pendek (intoleransi ringan) | Keluhan ringan dipakai menghindari alternatif murah |
| `KONTRAINDIKASI` | Kondisi/obat penyebab kontraindikasi dan hubungannya dengan alternatif Fornas | Apoteker; KFT bila kontraindikasi relatif | Selama kondisi ada | Kontraindikasi relatif diperlakukan mutlak |
| `INTERAKSI_OBAT` | Pasangan obat berinteraksi, tingkat keparahan, alasan tidak bisa diganti | Apoteker | Selama terapi bersamaan | Interaksi minor dibesar-besarkan |
| `POPULASI_KHUSUS` | Usia/berat/status hamil/menyusui/fungsi hati-ginjal dengan tanggal | Apoteker | Selama kondisi berlaku | Data populasi usang |
| `KOMORBID` | Komorbid terdokumentasi dan alasan klinis mengapa mengubah pilihan | Apoteker; KFT bila tidak jelas | Selama komorbid ada | Komorbid tidak terkait pilihan obat |
| `PERBURUKAN_KLINIS` | Data bukti perburukan (skor/lab/gejala) lebih dari ambang kriteria | Apoteker | Pendek, tinjau ulang | Fluktuasi normal dibaca sebagai perburukan |
| `GAWAT_DARURAT` | Triase/IGD, kondisi mengancam nyawa/kecacatan, waktu, penulis resep | **Retrospektif** (lanjut dulu, tinjau kemudian) | Episode darurat saja | Dipakai untuk kasus stabil; lihat pola di SKILL.md |
| `OFF_LABEL_BERBASIS_BUKTI` | Rujukan pedoman/PNPK/literatur, populasi sesuai, alasan alternatif Fornas tidak memadai | KFT/Komite | Per kasus, tinjau berkala | Rujukan lemah atau tidak sesuai populasi |

## 4. Kategori C: Kuantitas dan kontinuitas

| Kode | Bukti wajib | Persetujuan | Masa berlaku | Risiko salah pakai |
|---|---|---|---|---|
| `PERESEPAN_MAKS_LEBIH` | Alasan konkret: titrasi, berat badan, rencana bepergian, rujuk balik, kontrol jauh; jumlah yang diminta vs batas | Apoteker; KFT bila berulang | Per resep | Menjadi "kebiasaan" pada pasien yang sama |
| `RUJUK_BALIK` | Dokumen rujukan/inisiasi spesialis, obat dan dosis awal, tanggal, fasilitas asal | Apoteker | Selama program rujuk balik | Dokumen tidak tersedia; resep lama kedaluwarsa |

## 5. Kategori D: Ketersediaan dan di luar formularium

| Kode | Bukti wajib | Persetujuan | Masa berlaku | Risiko salah pakai |
|---|---|---|---|---|
| `STOK_KOSONG` | Catatan stok/kekosongan pemasok, tanggal, alternatif Fornas yang dicoba | Apoteker | Sampai stok tersedia | Alasan stok untuk menghindari obat murah |
| `OBAT_LUAR_FORNAS` | Alasan tidak ada alternatif Fornas yang memadai (kegagalan/kontraindikasi), bukti klinis | Kepala/direktur fasilitas setempat (Diktum KELIMA KMK 1199/2025: penggunaan terbatas sesuai peraturan perundang-undangan); tinjauan KFT/Komite bila diatur kebijakan fasilitas (verifikasi di edisi aktif) | Per kasus, tinjau berkala | Lompat ke luar Fornas padahal alternatif ada |
| `LAINNYA` | Narasi bebas (wajib) | KFT/Komite | Per kasus | Dipakai sebagai jalan pintas |

## 6. Contoh penyusunan justifikasi

Contoh ilustrasi; nama obat dan angka bukan kutipan Fornas.

**Kasus.** Obat X dibatasi untuk pasien yang gagal dengan obat A. Diagnosis tercatat sesuai, riwayat obat A tersedia 3 bulan dengan dosis penuh, hasil lab tidak mencapai target.

Keluaran:
- Kriteria diagnosis: `TERPENUHI` (kode ICD-10 sesuai, tanggal tercatat).
- Kriteria "gagal obat A": `TERPENUHI` (A 3 bulan, dosis maksimal, lab 02/09 tidak mencapai target).
- Status: `SESUAI`. Tidak perlu justifikasi tambahan; tampilkan bukti agar tercatat.

**Kasus.** Pasien baru dari IGD, obat X diresepkan, riwayat obat A tidak ada.

Keluaran:
- Kriteria "gagal obat A": `TIDAK_DIKETAHUI` bila riwayat memang tidak ada, bukan `TIDAK_TERPENUHI`.
- Status: `DATA_KURANG`, bila kondisi mendesak izinkan lanjut dengan `GAWAT_DARURAT` retrospektif; bila stabil, minta riwayat obat dari pasien/fasilitas sebelumnya.

## 7. Tanda bukti lemah

- Narasi umum ("sesuai kondisi pasien", "atas pertimbangan dokter") tanpa data.
- Tidak ada tanggal, atau tanggal tidak konsisten dengan kronologi.
- Lab diklaim tetapi tidak ada nilai/tanggal.
- Alasan sama persis lintas pasien.
- Alternatif Fornas tidak disebut sama sekali sebagai sudah dipertimbangkan.
