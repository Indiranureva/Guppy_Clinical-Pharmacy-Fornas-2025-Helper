"""Domain models for dossier evaluation and gap analysis results."""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any


class GapSeverity(str, Enum):
    CRITICAL = "CRITICAL"      # Likely direct rejection or showstopper
    MAJOR = "MAJOR"            # Will trigger formal PTD / Clock-stop
    MODERATE = "MODERATE"      # Administrative fix required prior to NIE
    MINOR = "MINOR"            # Editorial/Clarification
    COMPLIANT = "COMPLIANT"    # Satisfies BPOM requirements


class EvaluationStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    CONDITIONAL = "CONDITIONAL"


@dataclass
class GapFinding:
    rule_id: str
    actd_part: str
    section: str
    title: str
    status: EvaluationStatus
    severity: GapSeverity
    observation: str
    legal_citation: str
    remediation_steps: List[str]


@dataclass
class DossierScorecard:
    product_name: str
    total_checks: int
    passed_checks: int
    failed_checks: int
    compliance_score_percent: float
    critical_count: int
    major_count: int
    moderate_count: int
    findings: List[GapFinding]
    readiness_verdict: str  # 'SIAP SUBMIT', 'PERBAIKAN MINOR (PTD RENDAH)', 'RISIKO PTD TINGGI', 'TIDAK LAYAK SUBMIT'
    summary_message: str
