"""Unit tests for InputSanitizer and LinkGuard security engines."""

import pytest
from guppy.backend.security.sanitizer import InputSanitizer
from guppy.backend.security.link_guard import LinkGuard


# -------------------------------------------------------------
# InputSanitizer Tests
# -------------------------------------------------------------
def test_clean_text_strips_xss_scripts():
    malicious_input = "Metformin <script>alert('hacked')</script> 500 mg"
    cleaned = InputSanitizer.clean_text(malicious_input)
    assert "<script>" not in cleaned
    assert "alert" not in cleaned
    assert "Metformin" in cleaned
    assert "500 mg" in cleaned


def test_clean_text_strips_event_handlers():
    malicious_input = '<img src="x" onerror="stealCookies()">'
    cleaned = InputSanitizer.clean_text(malicious_input)
    assert "onerror" not in cleaned
    assert "stealCookies" not in cleaned


def test_clean_text_strips_sql_fragments():
    sql_payload = "Paracetamol'; DROP TABLE users; --"
    cleaned = InputSanitizer.clean_text(sql_payload)
    assert "--" not in cleaned


def test_validate_product_name_preserves_valid_characters():
    valid_name = "Paracetamol + Ibuprofen (200 mg / 5 mL)"
    cleaned = InputSanitizer.validate_product_name(valid_name)
    assert cleaned == "Paracetamol + Ibuprofen (200 mg / 5 mL)"


def test_sanitize_filename_prevents_path_traversal():
    sneaky_path = "../../../windows/system32/cmd.exe"
    clean_filename = InputSanitizer.sanitize_filename(sneaky_path)
    assert ".." not in clean_filename
    assert "/" not in clean_filename
    assert "\\" not in clean_filename
    assert "cmd.exe" in clean_filename


def test_mask_confidential_formula():
    formula = "Metformin HCl 90.5% with Magnesium Stearate 1.5% and Microcrystalline Cellulose 8.0%"
    masked = InputSanitizer.mask_confidential_formula(formula)
    assert "90.5%" not in masked
    assert "[REDACTED]" in masked


# -------------------------------------------------------------
# LinkGuard Tests
# -------------------------------------------------------------
def test_link_guard_approves_official_bpom_domains():
    res1 = LinkGuard.inspect_url("https://jdih.pom.go.id/peraturan/24_2017")
    assert res1["is_safe"] is True
    assert res1["is_official"] is True
    assert "pom.go.id" in res1["domain"]

    res2 = LinkGuard.inspect_url("https://cekbpom.pom.go.id/")
    assert res2["is_safe"] is True
    assert res2["is_official"] is True


def test_link_guard_approves_fda_ema_and_doi():
    res_fda = LinkGuard.inspect_url("https://www.fda.gov/drugs/guidances")
    assert res_fda["is_safe"] is True
    assert res_fda["is_official"] is True

    res_doi = LinkGuard.inspect_url("https://doi.org/10.1002/jps.21077")
    assert res_doi["is_safe"] is True
    assert res_doi["is_official"] is True


def test_link_guard_blocks_javascript_schemes():
    res = LinkGuard.inspect_url("javascript:alert(document.cookie)")
    assert res["is_safe"] is False
    assert res["threat_level"] == "CRITICAL"
    assert "javascript" in res["reason"].lower()


def test_link_guard_blocks_data_schemes():
    res = LinkGuard.inspect_url("data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==")
    assert res["is_safe"] is False
    assert res["threat_level"] == "CRITICAL"


def test_link_guard_blocks_ssrf_and_private_ips():
    res_localhost = LinkGuard.inspect_url("http://127.0.0.1:8080/admin")
    assert res_localhost["is_safe"] is False
    assert "SSRF" in res_localhost["reason"]

    res_metadata = LinkGuard.inspect_url("http://169.254.169.254/latest/meta-data")
    assert res_metadata["is_safe"] is False
    assert "SSRF" in res_metadata["reason"]


def test_link_guard_flags_unverified_external_domains():
    res = LinkGuard.inspect_url("https://unknown-pharma-blog.org/article")
    assert res["is_safe"] is True
    assert res["is_official"] is False
    assert "Waspada" in res["badge"]


def test_link_guard_traffic_light_status():
    # Awalnya lampu hijau
    LinkGuard._DOMAIN_SECURITY_STATUS.clear()
    assert LinkGuard.get_security_light()["color"] == "HIJAU"

    # Uji lampu orange (dibatasi sementara)
    LinkGuard.set_domain_status("kemkes.go.id", "RESTRICTED", "Pemeriksaan integritas")
    assert LinkGuard.get_security_light()["color"] == "ORANGE"
    inspect_res = LinkGuard.inspect_url("https://kemkes.go.id/pedoman")
    assert inspect_res["is_safe"] is False
    assert "DIBATASI SEMENTARA" in inspect_res["reason"]

    # Uji lampu merah (ditutup permanen)
    LinkGuard.set_domain_status("bad-hacker-site.com", "BLOCKED", "Ancaman peretasan terkonfirmasi")
    assert LinkGuard.get_security_light()["color"] == "MERAH"

    # Reset kembali ke hijau
    LinkGuard._DOMAIN_SECURITY_STATUS.clear()
    assert LinkGuard.get_security_light()["color"] == "HIJAU"
