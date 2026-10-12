# Pedoman Integritas Data & Sistem Terkomputerisasi CPOB (ALCOA+)

Dokumen ini memuat standar pemenuhan Integritas Data (*Data Integrity*) pada seluruh laboratorium pengujian dan fasilitas produksi sesuai prinsip **CPOB 2018 Bab 10** dan **Petunjuk Operasional Integritas Data BPOM / PIC/S PI 041**.

---

## 1. Prinsip Fundamental ALCOA+

Setiap rekaman data (kertas maupun elektronik) wajib memenuhi 9 kriteria ALCOA+:

| Prinsip | Definisi Teknis | Implementasi Nyata di Fasilitas Farmasi |
| :--- | :--- | :--- |
| **Attributable** (Dapat Diatribusikan) | Setiap tindakan atau entri data dapat dilacak secara pasti ke individu yang melakukannya. | Dilarang menggunakan akun bersama (*shared credentials*). Setiap analis QC/operator memiliki username, password unik, atau biometric login. |
| **Legible** (Dapat Dibaca) | Data harus dapat dibaca dan dipahami sepanjang siklus hidup penyimpanan. | Tulisan tangan jelas menggunakan tinta tahan air; data elektronik memiliki viewer perangkat lunak yang didukung. |
| **Contemporaneous** (Tercatat Seketika) | Data dicatat pada saat kegiatan pengujian atau produksi berlangsung. | Dilarang melakukan backdating atau pencatatan tertunda; audit trail instrumen HPLC mencatat stempel waktu otomatis (*time stamp*). |
| **Original** (Asli) | Rekaman asli pertama kali atau salinan resmi yang telah diverifikasi keasliannya (*true copy*). | File data kromatogram mentah (.raw/.dat) harus disimpan, bukan hanya cetakan PDF hasil olahan. |
| **Accurate** (Akurat) | Data bebas dari kesalahan, modifikasi tanpa otorisasi, atau manipulasi. | Integrasi kromatografi manual wajib dijustifikasi tertulis dan disetujui supervisor; timbangan analitik terkalibrasi. |
| **Complete** (Lengkap) | Mencakup seluruh metadata, data uji ulang, dan riwayat revisi. | Uji ulang sampel karena OOS wajib menyertakan laporan investigasi penuh; dilarang menghapus data uji coba (*trial injections*). |
| **Consistent** (Konsisten) | Data tidak saling bertentangan dan mengikuti urutan kronologis yang logis. | Waktu pencetakan tablet dalam BMR selaras dengan catatan waktu penyerahan granul dari ruang pengering. |
| **Enduring** (Tahan Lama) | Media penyimpanan terlindungi dari kerusakan fisik atau degradasi digital. | Backup otomatis berkala ke server off-site terenkripsi dengan proteksi read-only (*WORM storage*). |
| **Available** (Tersedia) | Data dapat diakses kapan saja untuk keperluan inspeksi BPOM atau audit internal. | Prosedur penarikan data arsip (*archival retrieval*) tervalidasi dan siap diuji coba dalam waktu $< 2$ jam saat inspeksi. |

---

## 2. Manajemen Jejak Audit (Audit Trail Review)

1. **Jejak Audit Wajib Aktif**: Fitur audit trail pada software analitik (misal: Waters Empower, Agilent OpenLab) dilarang dinonaktifkan oleh administrator.
2. **Kajian Berkala Audit Trail**:
   - Supervisor QC wajib mengkaji jejak audit sebelum meluluskan setiap bets (*batch release*).
   - Fokus kajian: Perubahan parameter integrasi kromatografi, penghapusan file, perubahan nama sampel, atau penyesuaian waktu sistem (*system clock alteration*).
