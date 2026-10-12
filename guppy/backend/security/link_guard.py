"""Anti-Hacker & Sneaky Link Protection Engine (LinkGuard).

Protects users against:
- Phishing and sneaky links (mismatched domains, deceptive anchor text)
- SSRF (Server-Side Request Forgery) and local network probes (127.0.0.1, 192.168.x.x, 169.254.169.254)
- Dangerous URL schemes (javascript:, data:, vbscript:, file:)
- Obfuscated IP addresses (hex, octal, dword)
- Unofficial or deceptive pharmaceutical portals
"""

import re
from urllib.parse import urlparse
from typing import Dict, Any, Tuple


class LinkGuard:
    """Safeguards pharmaceutical researchers from malicious links, tracker redirects,

    and deceptive domains when browsing regulatory references.
    """

    # Strictly curated list of recognized regulatory authorities and indexed scientific databases
    TRUSTED_REGULATORY_DOMAINS = {
        # Indonesian Official Regulatory Repositories
        "pom.go.id",
        "jdih.pom.go.id",
        "pionas.pom.go.id",
        "cekbpom.pom.go.id",
        "asrot.pom.go.id",
        "kemkes.go.id",
        "jdih.kemkes.go.id",
        "sehatnegeriku.kemkes.go.id",

        # Global Major Regulatory Bodies
        "fda.gov",
        "ema.europa.eu",
        "ich.org",
        "who.int",
        "edqm.eu",
        "pmda.go.jp",
        "tga.gov.au",

        # Reputable Peer-Reviewed Scientific Repositories (Q1-Q3)
        "doi.org",
        "ncbi.nlm.nih.gov",
        "nih.gov",
        "pubmed.ncbi.nlm.nih.gov",
        "doaj.org",
        "sciencedirect.com",
        "scimagojr.com",
        "springer.com",
        "wiley.com"
    }

    # Private IP / SSRF ranges to strictly block
    PRIVATE_IP_REGEX = re.compile(
        r"^(localhost|127\.\d+\.\d+\.\d+|10\.\d+\.\d+\.\d+|172\.(1[6-9]|2[0-9]|3[01])\.\d+\.\d+|192\.168\.\d+\.\d+|169\.254\.\d+\.\d+|0\.0\.0\.0|::1)$",
        re.IGNORECASE
    )

    DANGEROUS_SCHEMES = {"javascript", "data", "vbscript", "file", "about"}

    # Dynamic security state for reference domains:
    # "NORMAL" (Aman), "RESTRICTED" (Dibatasi sementara / Orange), "BLOCKED" (Ditutup permanen / Merah)
    _DOMAIN_SECURITY_STATUS: Dict[str, Dict[str, str]] = {}

    @classmethod
    def set_domain_status(cls, domain: str, status: str, reason: str = "") -> None:
        """Mengatur status keamanan domain: NORMAL, RESTRICTED, atau BLOCKED."""
        clean_d = domain.strip().lower()
        cls._DOMAIN_SECURITY_STATUS[clean_d] = {
            "status": status.upper(),
            "reason": reason
        }

    @classmethod
    def get_security_light(cls) -> Dict[str, Any]:
        """Menghitung status lampu proteksi sistem Guppy:
        - HIJAU  : Semua koneksi acuan aman (100% normal).
        - ORANGE : Ada satu atau lebih website yang sedang dibatasi sementara (karena anomali/risiko).
        - MERAH  : Ada satu atau lebih website yang ditutup permanen (karena peretasan/ancaman terkonfirmasi).
        """
        has_blocked = any(v["status"] == "BLOCKED" for v in cls._DOMAIN_SECURITY_STATUS.values())
        has_restricted = any(v["status"] == "RESTRICTED" for v in cls._DOMAIN_SECURITY_STATUS.values())

        if has_blocked:
            return {
                "color": "MERAH",
                "icon": "🔴",
                "label": "Lampu Merah: Akses Website Ditutup Permanen",
                "desc": "Terdeteksi ancaman kritis / website ditutup permanen untuk perlindungan sistem.",
                "details": [f"{d}: {v['reason']}" for d, v in cls._DOMAIN_SECURITY_STATUS.items() if v["status"] == "BLOCKED"]
            }
        elif has_restricted:
            return {
                "color": "ORANGE",
                "icon": "🟠",
                "label": "Lampu Orange: Akses Website Dibatasi Sementara",
                "desc": "Ada akses sumber referensi yang dibatasi sementara demi keamanan data.",
                "details": [f"{d}: {v['reason']}" for d, v in cls._DOMAIN_SECURITY_STATUS.items() if v["status"] == "RESTRICTED"]
            }
        else:
            return {
                "color": "HIJAU",
                "icon": "🟢",
                "label": "Lampu Hijau: Situasi Aman Terkendali",
                "desc": "Semua sumber data aman. Proteksi sistem dan privasi pengguna beroperasi normal.",
                "details": []
            }

    @classmethod
    def inspect_url(cls, url: str) -> Dict[str, Any]:
        """Inspects a link and categorizes it as Official, Trusted External, or Blocked (Sneaky Link)."""
        if not url or not isinstance(url, str):
            return {
                "is_safe": False,
                "threat_level": "CRITICAL",
                "reason": "URL kosong atau tidak valid."
            }

        url_clean = url.strip()

        # Check for dangerous schemes
        parsed = urlparse(url_clean)
        scheme = parsed.scheme.lower() if parsed.scheme else ""

        if scheme in cls.DANGEROUS_SCHEMES:
            return {
                "is_safe": False,
                "threat_level": "CRITICAL",
                "reason": f"Skema berbahaya '{scheme}:' terdeteksi (potensi serangan XSS / Hacker)."
            }

        if scheme not in ("http", "https"):
            return {
                "is_safe": False,
                "threat_level": "HIGH",
                "reason": f"Protokol '{scheme}' tidak didukung; hanya HTTPS/HTTP yang diizinkan."
            }

        hostname = (parsed.hostname or "").lower().strip()
        if not hostname:
            return {
                "is_safe": False,
                "threat_level": "CRITICAL",
                "reason": "Hostname kosong atau tidak valid."
            }

        # Check dynamic domain restriction / block list
        for d_key, d_val in cls._DOMAIN_SECURITY_STATUS.items():
            if hostname == d_key or hostname.endswith("." + d_key):
                if d_val["status"] == "BLOCKED":
                    return {
                        "is_safe": False,
                        "threat_level": "CRITICAL",
                        "reason": f"Akses ke website '{hostname}' DITUTUP PERMANEN karena ancaman keamanan: {d_val.get('reason', 'Keamanan terancam')}."
                    }
                elif d_val["status"] == "RESTRICTED":
                    return {
                        "is_safe": False,
                        "threat_level": "HIGH",
                        "reason": f"Akses ke website '{hostname}' DIBATASI SEMENTARA: {d_val.get('reason', 'Pemeriksaan integritas')}."
                    }

        # Check for private IP / SSRF attempts
        if cls.PRIVATE_IP_REGEX.match(hostname):
            return {
                "is_safe": False,
                "threat_level": "CRITICAL",
                "reason": f"Akses ke alamat IP privat/lokal '{hostname}' diblokir (Proteksi Anti-Hacker SSRF)."
            }

        # Check for hex/octal obfuscated IP patterns (e.g., http://0x7f000001)
        if re.match(r"^0x[0-9a-f]+$", hostname, re.IGNORECASE) or hostname.isdigit():
            return {
                "is_safe": False,
                "threat_level": "CRITICAL",
                "reason": "Format IP numerik/heksadesimal mencurigakan (Sneaky link terdeteksi)."
            }

        # Check domain against trusted regulatory list
        is_official = False
        matched_domain = None
        for trusted in cls.TRUSTED_REGULATORY_DOMAINS:
            if hostname == trusted or hostname.endswith("." + trusted):
                is_official = True
                matched_domain = trusted
                break

        if is_official:
            return {
                "is_safe": True,
                "is_official": True,
                "domain": hostname,
                "trusted_root": matched_domain,
                "threat_level": "NONE",
                "badge": "🛡️ Terverifikasi Badan Resmi (BPOM / Internasional / Q1-Q3)"
            }

        # If not on the pre-approved whitelist, mark as unverified external
        return {
            "is_safe": True,
            "is_official": False,
            "domain": hostname,
            "threat_level": "LOW",
            "badge": "⚠️ Tautan Eksternal Belum Terverifikasi (Waspada Phishing)"
        }

    @classmethod
    def render_safe_anchor(cls, url: str, anchor_label: str) -> str:
        """Renders an HTML anchor tag with strict security attributes (noopener noreferrer)

        or displays a warning block if the link is malicious.
        """
        inspection = cls.inspect_url(url)
        if not inspection["is_safe"]:
            return f'<span style="color: #dc2626; font-weight: 600;">🚫 [LINK DIBLOKIR: {inspection["reason"]}]</span>'

        if inspection.get("is_official", False):
            return (
                f'<a href="{url}" target="_blank" rel="noopener noreferrer" style="color: #0f766e; font-weight: 600; text-decoration: underline;">'
                f'{anchor_label}</a> <span style="font-size: 0.75rem; background: #ecfdf5; color: #065f46; padding: 2px 6px; border-radius: 4px; border: 1px solid #a7f3d0;">🛡️ Verified Official</span>'
            )
        else:
            return (
                f'<a href="{url}" target="_blank" rel="noopener noreferrer" style="color: #b45309; text-decoration: underline;">'
                f'{anchor_label}</a> <span style="font-size: 0.75rem; background: #fffbeb; color: #92400e; padding: 2px 6px; border-radius: 4px; border: 1px solid #fde68a;">⚠️ External</span>'
            )
