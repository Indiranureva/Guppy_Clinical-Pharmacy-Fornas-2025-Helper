"""Unit tests for RoadmapCalculator and NIE Decoder."""

import pytest
from guppy.backend.engine.roadmap_calculator import RoadmapCalculator


def test_timeline_calculation_jalur_300():
    result = RoadmapCalculator.calculate_timeline("jalur_300", estimated_ptd_rounds=1)
    # Pre-reg (20) + Jalur 300 (300) + 1 PTD round (40) = 360 working days
    assert result["total_working_days"] == 360
    assert result["ptd_rounds_modeled"] == 1
    assert len(result["milestones"]) >= 4


def test_decode_valid_nie():
    # Example NIE: DKL 1234567809 A 1
    nie_str = "DKL 1234567809 A 1"
    decoded = RoadmapCalculator.decode_nie(nie_str)
    assert decoded["valid"] is True
    assert decoded["brand_type"] == "Obat dengan Nama Dagang"
    assert decoded["golongan_obat"] == "Obat Keras"
    assert decoded["asal_produksi"] == "Produksi Dalam Negeri (Lokal)"
    assert decoded["tahun_persetujuan"] == "2012"


def test_decode_invalid_nie():
    decoded = RoadmapCalculator.decode_nie("DKL 123")
    assert decoded["valid"] is False
    assert "15 karakter" in decoded["error"]
