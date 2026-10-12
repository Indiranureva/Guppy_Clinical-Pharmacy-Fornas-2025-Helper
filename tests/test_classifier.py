"""Unit tests for ProductClassifier."""

import pytest
from guppy.backend.models.product import (
    ProductCase, ActiveIngredient, StabilityProfile, ManufacturingProfile
)
from guppy.backend.engine.classifier import ProductClassifier


def test_classify_metformin_as_ethical_drug():
    case = ProductCase(
        product_name="Metformin HCl Tablet 500 mg",
        active_ingredients=[ActiveIngredient(name="Metformin Hydrochloride", strength=500, unit="mg")],
        dosage_form="Tablet Salut Selaput",
        route_of_administration="Oral",
        intended_indication="Diabetes Melitus Tipe 2",
        stability=StabilityProfile("Zone IVb", "30°C/75% RH", 12, "40°C/75% RH", 6, "Blister"),
        manufacturing=ManufacturingProfile("PT Farma Sejahtera", "Indonesia", True, validation_batches_count=3)
    )
    result = ProductClassifier.classify(case)
    assert result["category"] == "Obat Jadi"
    assert result["sub_category"] == "Obat Keras (Ethical Drug)"
    assert result["prescription_required"] is True
    assert "Lingkaran Merah" in result["symbol"]


def test_classify_high_dose_vitamin_c_as_ethical_drug():
    case = ProductCase(
        product_name="Vitamin C 1500 mg Mega Dose",
        active_ingredients=[ActiveIngredient(name="Vitamin C (Ascorbic Acid)", strength=1500, unit="mg")],
        dosage_form="Tablet Effervescent",
        route_of_administration="Oral",
        intended_indication="Suplemen daya tahan tubuh",
        stability=StabilityProfile("Zone IVb", "30°C/75% RH", 12, "40°C/75% RH", 6, "Tube"),
        manufacturing=ManufacturingProfile("PT Nutri Farma", "Indonesia", True)
    )
    result = ProductClassifier.classify(case)
    assert result["category"] == "Obat Jadi"
    assert result["sub_category"] == "Obat Keras (Ethical Drug)"
    assert "1000 mg" in result["rationale"]


def test_classify_curcuma_standardized_as_oht():
    case = ProductCase(
        product_name="Curcuma Hepa Protect",
        active_ingredients=[ActiveIngredient(name="Ekstrak Rimpang Temulawak", strength=250, unit="mg")],
        dosage_form="Kapsul",
        route_of_administration="Oral",
        intended_indication="Membantu memelihara fungsi hati",
        stability=StabilityProfile("Zone IVb", "30°C/75% RH", 12, "40°C/75% RH", 6, "Botol"),
        manufacturing=ManufacturingProfile("PT Herbal Alam", "Indonesia", True),
        metadata={"has_standardized_extract": True, "has_preclinical_trials": True}
    )
    result = ProductClassifier.classify(case)
    assert result["category"] == "Obat Bahan Alam (OBA)"
    assert result["sub_category"] == "Obat Herbal Terstandar (OHT)"
    assert "Tiga Buah Bintang Hijau" in result["symbol"]
