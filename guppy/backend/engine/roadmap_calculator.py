"""BPOM Submission Roadmap, SLA Calculation, and NIE Decoding Engine."""

from datetime import datetime, timedelta
from typing import Dict, Any, List


class RoadmapCalculator:
    """Calculates official BPOM evaluation timelines (hari kerja) and milestone dates."""

    EVALUATION_PATHS = {
        "jalur_100": {
            "name": "Jalur 100 Hari (Fast Track / Prioritas)",
            "official_days": 100,
            "description": "Obat untuk penyakit mengancam jiwa, obat program nasional, orphan drug, atau obat esensial belum tersedia."
        },
        "jalur_150": {
            "name": "Jalur 150 Hari (Khusus / Lisensi / Generik Pertama)",
            "official_days": 150,
            "description": "Obat Copy Bermerek pertama, obat generik esensial, atau obat yang diproduksi dengan lisensi inovator."
        },
        "jalur_300": {
            "name": "Jalur 300 Hari (Reguler / Obat Baru / Standar)",
            "official_days": 300,
            "description": "Obat Entitas Kimiawi Baru (NCE), produk biologi, atau obat copy konvensional umum."
        },
        "variasi_mayor": {
            "name": "Jalur Variasi Mayor (VaMa)",
            "official_days": 100,
            "description": "Perubahan bermakna terhadap khasiat, keamanan, posologi, atau mutu (spesifikasi/proses pembuatan)."
        },
        "variasi_minor_approval": {
            "name": "Jalur Variasi Minor dengan Persetujuan (VaMi-B)",
            "official_days": 40,
            "description": "Perubahan minor yang memerlukan persetujuan BPOM (misal perubahan kemasan primer tanpa mengubah stabilitas)."
        }
    }

    @classmethod
    def calculate_timeline(
        cls,
        path_key: str,
        start_date: datetime = None,
        estimated_ptd_rounds: int = 1
    ) -> Dict[str, Any]:
        """Calculate working days, estimated calendar completion date, and stage breakdown."""
        if start_date is None:
            start_date = datetime.now()

        path_info = cls.EVALUATION_PATHS.get(path_key, cls.EVALUATION_PATHS["jalur_300"])
        eval_working_days = path_info["official_days"]

        # Pre-registration working days
        prereg_days = 20

        # PTD buffer (40 working days per round if triggered)
        ptd_days = estimated_ptd_rounds * 40

        total_working_days = prereg_days + eval_working_days + ptd_days

        # Convert working days (approx 5 days / week) to calendar days (multiply by ~1.4 + public holidays)
        calendar_duration_days = int(total_working_days * 1.45)
        projected_approval_date = start_date + timedelta(days=calendar_duration_days)

        milestones = [
            {
                "stage": "1. Pra-Registrasi & Pembayaran PNBP",
                "duration_working_days": prereg_days,
                "description": "Pengunggahan dokumen Bagian I dan penilaian jalur registrasi serta penerbitan HPR."
            },
            {
                "stage": "2. Penyerahan Berkas Lengkap ACTD (Parts I - IV)",
                "duration_working_days": 10,
                "description": "Penerbitan Surat Perintah Bayar (SPB) dan verifikasi kelengkapan berkas elektronik di ASROT."
            },
            {
                "stage": f"3. Evaluasi Teknis Komnas Penilai ({path_info['name']})",
                "duration_working_days": eval_working_days,
                "description": "Clock running: Evaluasi mutu (CMC), farmakologi, dan uji bioekivalensi/klinik."
            }
        ]

        if estimated_ptd_rounds > 0:
            milestones.append({
                "stage": f"4. Permintaan Tambahan Data (PTD) x {estimated_ptd_rounds}",
                "duration_working_days": ptd_days,
                "description": "Clock stopped: Pemenuhan pertanyaan klarifikasi evaluator BPOM oleh pendaftar."
            })

        milestones.append({
            "stage": "5. Finalisasi Penandaan & Terbit Nomor Izin Edar (NIE)",
            "duration_working_days": 15,
            "description": "Verifikasi desain kemasan final dan penerbitan sertifikat NIE resmi."
        })

        return {
            "path_name": path_info["name"],
            "path_description": path_info["description"],
            "start_date": start_date.strftime("%Y-%m-%d"),
            "projected_nie_date": projected_approval_date.strftime("%Y-%m-%d"),
            "total_working_days": total_working_days,
            "estimated_calendar_months": round(calendar_duration_days / 30.0, 1),
            "ptd_rounds_modeled": estimated_ptd_rounds,
            "milestones": milestones
        }

    @classmethod
    def decode_nie(cls, nie_code: str) -> Dict[str, Any]:
        """Decodes a 15-digit BPOM NIE code (e.g., 'DKL1234567809A1')."""
        clean = nie_code.replace(" ", "").upper()
        if len(clean) != 15:
            return {
                "valid": False,
                "error": f"Panjang nomor izin edar harus tepat 15 karakter (terdeteksi {len(clean)} karakter)."
            }

        brand_type_code = clean[0]
        class_code = clean[1]
        origin_code = clean[2]
        year_digits = clean[3:5]
        factory_digits = clean[5:8]
        drug_digits = clean[8:11]
        dosage_digits = clean[11:13]
        strength_code = clean[13]
        package_code = clean[14]

        brand_map = {"D": "Obat dengan Nama Dagang", "G": "Obat dengan Nama Generik"}
        class_map = {
            "K": "Obat Keras", "T": "Obat Bebas Terbatas", "B": "Obat Bebas",
            "N": "Narkotika", "P": "Psikotropika"
        }
        origin_map = {
            "L": "Produksi Dalam Negeri (Lokal)", "I": "Produksi Luar Negeri (Impor)",
            "E": "Khusus Keperluan Ekspor", "X": "Keperluan Khusus Uji Klinik"
        }

        return {
            "valid": True,
            "nie": f"{clean[0:3]} {clean[3:5]} {clean[5:8]} {clean[8:11]} {clean[11:13]} {clean[13]} {clean[14]}",
            "brand_type": brand_map.get(brand_type_code, "Tidak Dikenal"),
            "golongan_obat": class_map.get(class_code, "Tidak Dikenal"),
            "asal_produksi": origin_map.get(origin_code, "Tidak Dikenal"),
            "tahun_persetujuan": f"20{year_digits}" if int(year_digits) < 50 else f"19{year_digits}",
            "nomor_pabrik": factory_digits,
            "nomor_urut_obat": drug_digits,
            "kode_bentuk_sediaan": dosage_digits,
            "kekuatan_sediaan": f"Kekuatan/Bentuk ke-{ord(strength_code) - 64 if strength_code.isalpha() else strength_code}",
            "macam_kemasan": f"Kemasan ke-{package_code}"
        }
