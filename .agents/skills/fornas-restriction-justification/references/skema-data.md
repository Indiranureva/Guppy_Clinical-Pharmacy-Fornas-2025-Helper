# Skema Data

Dipakai agent untuk menyusun keluaran yang konsisten dan bisa diproses aplikasi. Nama field boleh disesuaikan dengan sistem pengguna, tetapi **struktur dan makna** dipertahankan.

## Daftar isi
1. Kriteria restriksi (hasil pemecahan teks Fornas)
2. Ringkasan data pasien
3. Keluaran evaluasi
4. Contoh lengkap
5. Aturan pengisian

## 1. Kriteria restriksi

```json
{
  "obat": "nama generik, sediaan, kekuatan",
  "fornas_versi": "versi/tanggal berlaku yang dipakai",
  "teks_restriksi_asli": "salin persis dari sumber",
  "operator_utama": "DAN | ATAU",
  "kriteria": [
    {
      "id": "K1",
      "jenis": "diagnosis | derajat | lini_terapi | populasi | penulis_resep | fasilitas | kuantitas | penunjang",
      "deskripsi": "ringkas, dalam bahasa klinis",
      "kode_icd10": ["opsional"],
      "ambang": {"parameter": "opsional", "operator": ">=", "nilai": 0, "satuan": ""},
      "sifat": "keselamatan | kendali_biaya | administratif",
      "wajib": true,
      "ambigu": false
    }
  ],
  "peresepan_maksimal": {"jumlah": null, "per": "kunjungan | hari | bulan", "catatan": "dapat berbeda per fasilitas (FPKTP/FPKTL) dan per kekuatan"},
  "tingkat_restriksi": "kelas_terapi | zat_aktif | sediaan (gabungkan ketiganya untuk satu sediaan)",
  "fasilitas": {"fpktp": false, "fpktl": false, "pp": false, "prb": false, "oen": false}
}
```

## 2. Ringkasan data pasien

```json
{
  "usia": {"nilai": 0, "satuan": "tahun | bulan", "tanggal_data": ""},
  "berat_badan_kg": {"nilai": null, "tanggal_data": ""},
  "kehamilan_menyusui": "ya | tidak | tidak_diketahui",
  "diagnosis": [
    {"kode": "", "teks": "", "jenis": "utama | sekunder | komorbid", "status": "kerja | definitif", "tanggal": "", "sumber": ""}
  ],
  "lab": [{"nama": "", "nilai": 0, "satuan": "", "tanggal": ""}],
  "riwayat_obat": [{"obat": "", "dosis": "", "mulai": "", "selesai": "", "alasan_henti": ""}],
  "alergi_intoleransi": [{"agen": "", "reaksi": "", "tanggal": ""}],
  "obat_berjalan": [""],
  "fasilitas": {"tingkat": "FKTP | FKRTL", "penulis_resep": "spesialisasi"}
}
```

Field kosong diisi `null`, jangan ditebak.

## 3. Keluaran evaluasi

```json
{
  "status": "SESUAI | DATA_KURANG | PERLU_JUSTIFIKASI | TIDAK_SESUAI | ESKALASI",
  "evaluasi_kriteria": [
    {
      "id": "K1",
      "hasil": "TERPENUHI | TIDAK_TERPENUHI | TIDAK_DIKETAHUI",
      "bukti": [{"field": "diagnosis[0].kode", "nilai": "", "tanggal": ""}],
      "alasan": "satu kalimat"
    }
  ],
  "justifikasi_disarankan": [
    {
      "kode": "LINI_1_GAGAL",
      "kekuatan_bukti": "kuat | sedang | lemah",
      "bukti_tersedia": [""],
      "bukti_kurang": [""],
      "persetujuan_disarankan": "Otomatis | Apoteker | KFT | Retrospektif",
      "masa_berlaku_disarankan": ""
    }
  ],
  "alternatif_fornas": [{"obat": "", "memenuhi_restriksi": true, "catatan_klinis": ""}],
  "peringatan_keselamatan": [""],
  "pola_ditandai": [""],
  "data_diminta": [""],
  "notifikasi": [
    {"id_rujukan": "", "tingkat": "KRITIS | PENTING | INFO", "penerima": "penulis_resep | apoteker | KFT", "judul": "", "isi": "", "data_diminta": [""], "tindakan": [""], "tenggat": "", "dapat_menunda_terapi": false, "asumsi": [""]}
  ],
  "ringkasan_untuk_penulis_resep": "2-4 kalimat",
  "catatan_kepastian": "apa yang diasumsikan atau tidak bisa diverifikasi"
}
```

## 4. Contoh lengkap (ilustrasi)

Obat X (restriksi ilustrasi: "hanya untuk indikasi Y setelah gagal obat A"). Pasien dengan diagnosis Y definitif, obat A tidak ada di riwayat, kondisi stabil.

```json
{
  "status": "DATA_KURANG",
  "evaluasi_kriteria": [
    {"id": "K1", "hasil": "TERPENUHI", "bukti": [{"field": "diagnosis[0].kode", "nilai": "Y00.1", "tanggal": "2026-08-14"}], "alasan": "Diagnosis definitif sesuai indikasi."},
    {"id": "K2", "hasil": "TIDAK_DIKETAHUI", "bukti": [], "alasan": "Riwayat obat A tidak tercatat; belum jelas apakah pernah dicoba."}
  ],
  "justifikasi_disarankan": [
    {"kode": "DATA_TIDAK_LENGKAP", "kekuatan_bukti": "sedang", "bukti_tersedia": ["Diagnosis sesuai"], "bukti_kurang": ["Riwayat obat A: dosis, durasi, hasil"], "persetujuan_disarankan": "Otomatis", "masa_berlaku_disarankan": "Sampai kunjungan berikutnya"}
  ],
  "alternatif_fornas": [{"obat": "A", "memenuhi_restriksi": true, "catatan_klinis": "Lini 1; pertimbangkan bila belum pernah dicoba dan tidak ada kontraindikasi."}],
  "notifikasi": [{"id_rujukan": "RSP-2026-001234", "tingkat": "PENTING", "penerima": "penulis_resep", "judul": "Lengkapi riwayat obat A", "isi": "Syarat 'gagal obat A' belum bisa dinilai karena riwayat tidak tercatat.", "data_diminta": ["Obat A: dosis, lama, respons"], "tindakan": ["Isi riwayat"], "tenggat": "Sebelum kunjungan berikutnya (asumsi default)", "dapat_menunda_terapi": false, "asumsi": ["Tenggat default skill"]}],
  "peringatan_keselamatan": [],
  "pola_ditandai": [],
  "data_diminta": ["Riwayat penggunaan obat A (dosis, lama, respons)"],
  "ringkasan_untuk_penulis_resep": "Diagnosis memenuhi indikasi, tetapi syarat 'gagal obat A' belum dapat dinilai karena riwayat tidak tercatat. Mohon lengkapi riwayat obat A. Bila belum pernah dicoba dan tidak ada kontraindikasi, obat A memenuhi restriksi dan dapat menjadi pilihan.",
  "catatan_kepastian": "Teks restriksi diambil dari data aplikasi; versi Fornas dicatat di fornas_versi."
}
```

## 5. Aturan pengisian

- `bukti` selalu merujuk ke field data pasien nyata; jangan menulis bukti yang tidak ada.
- `alasan` satu kalimat, tanpa pengulangan teks restriksi.
- Jika `status` bukan `SESUAI`, `ringkasan_untuk_penulis_resep` wajib berisi langkah berikutnya yang konkret.
- `pola_ditandai` hanya diisi dengan deskripsi fakta (apa yang teramati), tanpa menuduh niat.
- `alternatif_fornas` hanya berisi obat dari daftar formularium di data aplikasi; bila daftar tidak tersedia, kosongkan dan jelaskan di `catatan_kepastian`.
- `notifikasi` kosong bila status `SESUAI`. Lihat `notifikasi.md` untuk aturan penerima, tingkat, dan privasi.
- `catatan_kepastian` jujur tentang apa yang tidak bisa diverifikasi (mis. regulasi terbaru).
