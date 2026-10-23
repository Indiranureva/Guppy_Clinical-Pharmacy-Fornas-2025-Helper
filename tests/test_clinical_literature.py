"""Unit tests for ClinicalLiteratureScout with multi-article selection and memo generator."""

import pytest
from guppy.backend.engine.clinical_literature import ClinicalLiteratureScout


def test_curated_topics_structure():
    topics = ClinicalLiteratureScout.get_all_topics()
    assert len(topics) >= 8
    for t in topics:
        assert "topic_id" in t
        assert "title" in t
        assert "category" in t
        assert "drug_inn" in t
        assert "clinical_problem" in t
        assert "articles" in t
        assert len(t["articles"]) >= 2
        # Check articles structure
        has_primary = False
        for art in t["articles"]:
            assert "article_id" in art
            assert "citation" in art
            assert "clinical_finding" in art
            assert "fornas_implication" in art
            c = art["citation"]
            assert "authors" in c
            assert "year" in c
            assert "title" in c
            assert "journal" in c
            assert "quartile" in c
            if art.get("is_primary"):
                has_primary = True
        assert has_primary, f"Topic {t['topic_id']} must have at least one primary recommended article."


def test_get_topic_by_id():
    topic = ClinicalLiteratureScout.get_topic_by_id("metformin_ckd_egfr")
    assert topic is not None
    assert topic["drug_inn"] == "Metformin"
    assert len(topic["articles"]) == 3


def test_search_curated_topics():
    # Search by drug
    results = ClinicalLiteratureScout.search_curated_topics("metformin")
    assert any(t["topic_id"] == "metformin_ckd_egfr" for t in results)

    # Search by condition
    results_geriatric = ClinicalLiteratureScout.search_curated_topics("lansia")
    assert len(results_geriatric) >= 2

    # Search empty
    all_t = ClinicalLiteratureScout.search_curated_topics("")
    assert len(all_t) == len(ClinicalLiteratureScout.get_all_topics())


def test_synonyms_and_deep_search():
    # Indonesian spelling variants matching English INN topics
    res_seftri = ClinicalLiteratureScout.search_curated_topics("seftriakson")
    assert len(res_seftri) >= 1
    assert any("Amoksisilin vs Sefalosporin" in t["title"] or "Ceftriaxone" in t["drug_inn"] for t in res_seftri)

    res_kande = ClinicalLiteratureScout.search_curated_topics("kandesartan")
    assert len(res_kande) >= 1
    assert any("Kandesartan" in t["title"] for t in res_kande)

    res_steroid = ClinicalLiteratureScout.search_curated_topics("deksametason")
    assert len(res_steroid) >= 1
    assert any("Kortikosteroid" in t["title"] for t in res_steroid)

    res_plavix = ClinicalLiteratureScout.search_curated_topics("plavix")
    assert len(res_plavix) >= 1
    assert any("Clopidogrel" in t["title"] or "DAPT" in t["title"] for t in res_plavix)


def test_backward_compatibility_search_clinical_evidence():
    evidence = ClinicalLiteratureScout.search_clinical_evidence("Metformin")
    assert len(evidence) >= 1
    card = ClinicalLiteratureScout.format_evidence_card(evidence[0])
    assert "Metformin" in card
    assert "Sumber Literatur" in card


def test_generate_justification_memo():
    topic = ClinicalLiteratureScout.get_topic_by_id("metformin_ckd_egfr")
    assert topic is not None

    # Pick 2 articles
    selected = topic["articles"][:2]
    patient_info = {
        "nama_pasien": "Tn. Suroso (62 th)",
        "no_rm": "RM-2026-9912",
        "diagnosis": "E11 (DMT2) + N18.3 (CKD Stadium 3a)",
        "dpjp": "dr. Sp.PD-KEMD",
        "ruangan": "Poli Penyakit Dalam",
    }
    notes = "Dosis metformin disesuaikan menjadi 500 mg 2x sehari (1000 mg/hari). Pemantauan eGFR diulang 3 bulan lagi."

    memo = ClinicalLiteratureScout.generate_justification_memo(
        topic=topic,
        selected_articles=selected,
        patient_info=patient_info,
        pharmacist_notes=notes,
        pharmacist_name="Apt. Indira Nureva, S.Farm.",
        sipa_number="SIPA.1995.04.01",
    )

    assert "MEMO JUSTIFIKASI KLINIS" in memo
    assert "Tn. Suroso (62 th)" in memo
    assert "RM-2026-9912" in memo
    assert "Apt. Indira Nureva, S.Farm." in memo
    assert "Dosis metformin disesuaikan" in memo
    assert "Lipska" in memo
    assert "Inzucchi" in memo
    assert "LEMBAR PENGESAHAN" in memo


def test_generate_universal_justification_memo():
    memo = ClinicalLiteratureScout.generate_universal_justification_memo(
        drug_name="Ketorolac",
        justification_reason="Nyeri Pasca Operasi Akut Berat (VAS 8-9)",
        clinical_rationale="Pasien mengalami nyeri akut berat refrakter terhadap parasetamol IV.",
        patient_info={
            "nama_pasien": "Ny. Marlina (45 th)",
            "no_rm": "RM-2026-8810",
            "dpjp": "dr. Sp.An",
        },
        fornas_info={
            "kelas_terapi": "Analgesik Non-Opioid",
            "fasilitas": "FPKTL (Rumah Sakit)",
            "peresepan_maksimal": "Maksimal 2-3 hari untuk nyeri akut",
        },
        pharmacist_name="Apt. Tim Farmasi Klinis",
    )

    assert "MEMO JUSTIFIKASI KLINIS" in memo
    assert "KETOROLAC" in memo
    assert "Ny. Marlina (45 th)" in memo
    assert "Nyeri Pasca Operasi" in memo
    assert "Analgesik Non-Opioid" in memo
    assert "LEMBAR PENGESAHAN" in memo


def test_generate_justification_memo_docx():
    topic = ClinicalLiteratureScout.get_topic_by_id("metformin_ckd_egfr")
    assert topic is not None
    docx_bytes = ClinicalLiteratureScout.generate_justification_memo_docx(
        topic=topic,
        selected_articles=topic["articles"][:2],
        patient_info={"nama_pasien": "Tn. Test", "no_rm": "RM-1234"},
        pharmacist_name="Apt. Test",
    )
    assert isinstance(docx_bytes, bytes)
    assert len(docx_bytes) > 10000  # Valid docx zip archive is ~35-40KB
    assert docx_bytes[:4] == b"PK\x03\x04"  # Standard ZIP / DOCX magic bytes


def test_generate_universal_justification_memo_docx():
    docx_bytes = ClinicalLiteratureScout.generate_universal_justification_memo_docx(
        drug_name="Gentamicin",
        justification_reason="Kultur Bakteri Resisten Sefalosporin",
        clinical_rationale="Pasien mengalami urosepsis resisten terapi lini pertama.",
        patient_info={"nama_pasien": "Ny. Test", "no_rm": "RM-5678"},
        fornas_info={"kelas_terapi": "Aminoglikosida", "fasilitas": "FPKTL"},
        pharmacist_name="Apt. Test",
    )
    assert isinstance(docx_bytes, bytes)
    assert len(docx_bytes) > 10000
    assert docx_bytes[:4] == b"PK\x03\x04"

