"""Unit tests for DossierGapAnalyzer."""

import pytest
from guppy.backend.models.product import (
    ProductCase, ActiveIngredient, StabilityProfile, ManufacturingProfile
)
from guppy.backend.models.dossier import GapSeverity, EvaluationStatus
from guppy.backend.engine.gap_analyzer import DossierGapAnalyzer


@pytest.fixture
def analyzer():
    return DossierGapAnalyzer()


def test_zone_ii_stability_triggers_critical_gap(analyzer):
    # Non-compliant Zone II stability case
    case = ProductCase(
        product_name="Generic Metformin HCl 500 mg",
        active_ingredients=[ActiveIngredient("Metformin HCl", 500, "mg")],
        dosage_form="Tablet Salut Selaput",
        route_of_administration="Oral",
        intended_indication="Antidiabetes",
        stability=StabilityProfile(
            climatic_zone="Zone II",
            real_time_temp_rh="25°C/60% RH",
            real_time_months=24,
            accelerated_temp_rh="40°C/75% RH",
            accelerated_months=6,
            primary_packaging="PVC/Alu Blister"
        ),
        manufacturing=ManufacturingProfile("PT Farma Indo", "Indonesia", True, validation_batches_count=3),
        be_study_completed=True,
        barcode_2d_present=True
    )

    scorecard = analyzer.evaluate(case)
    assert scorecard.critical_count >= 1
    assert "TIDAK LAYAK SUBMIT" in scorecard.readiness_verdict

    # Verify stability finding
    stab_finding = next(f for f in scorecard.findings if f.section == "II.C.11")
    assert stab_finding.severity == GapSeverity.CRITICAL
    assert stab_finding.status == EvaluationStatus.FAIL
    assert "Zona IVb" in stab_finding.observation


def test_fully_compliant_case_passes(analyzer):
    case = ProductCase(
        product_name="Compliant Metformin HCl 500 mg",
        active_ingredients=[ActiveIngredient("Metformin HCl", 500, "mg")],
        dosage_form="Tablet Salut Selaput",
        route_of_administration="Oral",
        intended_indication="Antidiabetes",
        stability=StabilityProfile(
            climatic_zone="Zone IVb",
            real_time_temp_rh="30°C/75% RH",
            real_time_months=12,
            accelerated_temp_rh="40°C/75% RH",
            accelerated_months=6,
            primary_packaging="PVC/Alu Blister"
        ),
        manufacturing=ManufacturingProfile("PT Farma Indo", "Indonesia", True, validation_batches_count=3),
        be_study_completed=True,
        barcode_2d_present=True
    )

    scorecard = analyzer.evaluate(case)
    assert scorecard.critical_count == 0
    assert scorecard.compliance_score_percent == 100.0
    assert "SIAP SUBMIT" in scorecard.readiness_verdict
