# Panduan Notifikasi

Dibaca agent saat menyusun notifikasi dari hasil evaluasi restriksi Fornas. Tenggat, saluran, dan penerima di bawah adalah **default yang disarankan**; sesuaikan dengan kebijakan fasilitas dan tandai sebagai asumsi bila tidak ada konfigurasi.

## Daftar isi
1. Tingkat keparahan
2. Matriks pemicu
3. Templat notifikasi
4. Eskalasi bertahap (gawat darurat retrospektif)
5. Anti alert-fatigue
6. Notifikasi berkala untuk KFT
7. Privasi
8. Contoh

## 1. Tingkat keparahan

| Tingkat | Arti | Perilaku |
|---|---|---|
| `KRITIS` | Potensi bahaya pasien (alergi, kontraindikasi, interaksi berat, restriksi keselamatan dilanggar) | In-app langsung; harus diakui sebelum lanjut; tidak bisa ditekan oleh justifikasi restriksi |
| `PENTING` | Perlu tindakan hari ini (data kurang, persetujuan menunggu, tenggat retrospektif) | In-app; pengingat bila belum ditindaklanjuti |
| `INFO` | Tidak perlu tindakan segera (masa berlaku mendekati habis, tren) | Dikumpulkan dalam ringkasan, tidak mengganggu |

## 2. Matriks pemicu

| Pemicu | Penerima | Tingkat | Tindakan yang diminta |
|---|---|---|---|
| Status `DATA_KURANG` | Penulis resep | PENTING (INFO bila terapi tidak mendesak) | Lengkapi data spesifik yang disebut |
| Status `PERLU_JUSTIFIKASI` | Penulis resep | PENTING | Pilih kode alasan yang didukung data dan lampirkan bukti kurang |
| Justifikasi menunggu persetujuan | Apoteker | PENTING | Setujui, tolak, atau minta data tambahan |
| Penyimpangan restriksi `keselamatan` | Apoteker dan KFT | KRITIS | Tinjau sebelum terapi dilanjutkan, kecuali gawat darurat |
| Status `TIDAK_SESUAI` | Penulis resep | PENTING | Pertimbangkan alternatif Fornas atau ajukan persetujuan khusus |
| `GAWAT_DARURAT` dipakai | Apoteker | PENTING | Lengkapi dokumentasi dalam jendela waktu (retrospektif) |
| Peringatan keselamatan (alergi/kontraindikasi/interaksi) | Penulis resep dan apoteker | KRITIS | Konfirmasi telah ditinjau |
| Restriksi ambigu atau data bertentangan | Apoteker/KFT | PENTING | Tafsirkan teks restriksi atau klarifikasi data |
| Pola ditandai (ada pembanding) | Apoteker/KFT (bukan penulis resep) | PENTING | Tinjau pola, putuskan perlu tindak lanjut atau tidak |
| Pola tanpa pembanding (pengamatan) | Apoteker/KFT | INFO | Nilai konteks; sebut bahwa belum ada data pembanding |
| Restriksi keselamatan dilanggar, urgensi tidak diketahui | Apoteker jaga | KRITIS | Respons cepat; konfirmasi apakah kondisi akut. Terapi tidak ditahan |
| Justifikasi mendekati habis masa berlaku | Penulis resep | INFO | Perbarui bila terapi dilanjutkan |
| Stok alternatif Fornas kosong (`STOK_KOSONG`) | Apoteker | PENTING | Konfirmasi stok dan jalur pengadaan |
| Notifikasi sering diabaikan | KFT | INFO | Tinjau kebisingan atau kebutuhan aturan baru |

Status `SESUAI` dan justifikasi masih berlaku: **tidak ada notifikasi**.

## 3. Templat notifikasi

Setiap notifikasi memuat bidang berikut, singkat dan bisa ditindaklanjuti:

```json
{
  "id_rujukan": "ID resep atau kasus, bukan nama pasien",
  "tingkat": "KRITIS | PENTING | INFO",
  "penerima": "penulis_resep | apoteker | KFT",
  "judul": "maks. ~8 kata, menyebut tindakan",
  "isi": "1-3 kalimat: apa yang terjadi dan kenapa",
  "data_diminta": ["butir spesifik, bukan 'lengkapi data'"],
  "tindakan": ["tombol/aksi yang tersedia"],
  "tenggat": "mis. sebelum kunjungan berikutnya, atau 24 jam; sebut jika asumsi",
  "dapat_menunda_terapi": false,
  "asumsi": ["default yang dipakai karena tidak ada konfigurasi"]
}
```

Pedoman isi:
- Judul memuat tindakan, bukan keluhan: "Lengkapi riwayat obat A" lebih baik daripada "Restriksi tidak terpenuhi".
- `data_diminta` menyebut persis apa: nama obat, rentang tanggal, jenis lab.
- `dapat_menunda_terapi` hanya `true` untuk `KRITIS` yang memang perlu tinjauan sebelum lanjut. Notifikasi gawat darurat selalu `false`.
- Nada netral dan hormat. Jangan menggunakan huruf kapital berlebihan atau kata yang menyiratkan kesalahan.

## 4. Eskalasi bertahap (gawat darurat retrospektif)

Default yang disarankan; sesuaikan dengan jendela waktu kebijakan fasilitas dan aturan yang berlaku:

| Tahap | Waktu | Penerima | Isi |
|---|---|---|---|
| 1 | Saat `GAWAT_DARURAT` dipakai | Penulis resep | Pengingat dokumentasi minimal yang dibutuhkan (waktu, kondisi, penulis resep) |
| 2 | Mendekati tenggat (mis. 50% jendela) | Penulis resep | Pengingat lembut dengan sisa waktu |
| 3 | Lewat tenggat | Apoteker, lalu KFT bila berulang | Dokumentasi belum lengkap; minta tinjauan, bukan sanksi |

Terapi tidak pernah dihentikan karena tahap eskalasi.

## 5. Anti alert-fatigue

- **Gabungkan** notifikasi dari satu resep menjadi satu kartu dengan beberapa butir, bukan beberapa pop-up.
- **Hindari duplikat**: jangan kirim ulang butir yang sama dalam periode pendek, kecuali naik tingkat.
- **Tekan notifikasi yang tidak bisa ditindaklanjuti**, misalnya menyebut masalah tanpa menyebut data yang kurang.
- **Pisahkan keselamatan dan restriksi** sehingga peringatan keselamatan tidak tenggelam.
- **Pantau**: bila lebih dari separuh notifikasi satu jenis diabaikan, usulkan peninjauan aturan ke KFT.
- **Jadikan kasus yang sering dijustifikasi sah sebagai sinyal aturan**, bukan sekadar membombardir pengguna dengan alert yang sama.

## 6. Notifikasi berkala untuk KFT

Ringkasan berkala (mis. bulanan; sesuaikan) berisi, tanpa data pribadi pasien:
- Restriksi yang paling sering memicu justifikasi, beserta kode alasan dominan.
- Jumlah dan hasil persetujuan (disetujui, ditolak, ditunda).
- Pola yang ditandai (deskripsi faktual) dan statusnya.
- Rasio notifikasi yang ditindaklanjuti vs diabaikan.
- Usulan: butir yang mungkin perlu klarifikasi aturan di aplikasi atau diajukan untuk peninjauan kepada pihak berwenang.

## 7. Privasi

- Notifikasi di luar aplikasi hanya memuat `id_rujukan`, jenis tindakan, dan tenggat. Tidak ada nama pasien, nomor identitas, atau diagnosis.
- Isi klinis hanya tampil di dalam aplikasi setelah autentikasi.
- Ringkasan KFT menggunakan angka agregat atau ID anonim.

## 8. Contoh

**Kasus (ilustrasi):** Obat X, kriteria "gagal obat A" tidak diketahui, rawat jalan stabil.

```json
{
  "id_rujukan": "RSP-2026-001234",
  "tingkat": "PENTING",
  "penerima": "penulis_resep",
  "judul": "Lengkapi riwayat obat A",
  "isi": "Diagnosis sesuai indikasi, tetapi syarat 'gagal obat A' belum bisa dinilai karena riwayatnya tidak tercatat.",
  "data_diminta": ["Obat A: dosis, lama pemakaian, respons"],
  "tindakan": ["Isi riwayat", "Pertimbangkan obat A (memenuhi restriksi)"],
  "tenggat": "Sebelum kunjungan berikutnya (asumsi default)",
  "dapat_menunda_terapi": false,
  "asumsi": ["Tenggat memakai default skill karena tidak ada konfigurasi fasilitas"]
}
```

**Kasus (ilustrasi):** Seorang penulis resep memakai `GAWAT_DARURAT` berulang pada pasien rawat jalan stabil.

- Penulis resep menerima hanya pengingat dokumentasi (tahap 1 dan 2).
- Apoteker/KFT menerima: "Dalam 30 hari, kode GAWAT_DARURAT dipakai 9 kali pada unit rawat jalan; 7 kasus tidak mencatat triase. Mohon tinjau pola ini." Tanpa menyebut niat atau menuduh.
