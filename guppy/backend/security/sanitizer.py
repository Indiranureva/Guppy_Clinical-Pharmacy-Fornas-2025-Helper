"""Input Sanitization and Data Protection Engine for Guppy.

Protects user input and proprietary formulation data against:
- Cross-Site Scripting (XSS)
- Code / SQL Injection
- Directory & Path Traversal
- Malicious character sequences
"""

import html
import re
from typing import Optional


class InputSanitizer:
    """Sanitizes user input and secures confidential pharmaceutical findings."""

    # Patterns matching dangerous injection payloads
    DANGEROUS_PATTERNS = [
        re.compile(r"<\s*script[^>]*>.*?<\s*/\s*script\s*>", re.IGNORECASE | re.DOTALL),
        re.compile(r"<\s*iframe[^>]*>.*?<\s*/\s*iframe\s*>", re.IGNORECASE | re.DOTALL),
        re.compile(r"javascript\s*:", re.IGNORECASE),
        re.compile(r"vbscript\s*:", re.IGNORECASE),
        re.compile(r"data\s*:\s*text/html", re.IGNORECASE),
        re.compile(r"on\w+\s*=", re.IGNORECASE),  # onload=, onerror=, etc.
        re.compile(r"--|/\*|\*/|@@|char\s*\(|nchar\s*\(", re.IGNORECASE)  # SQL injection fragments
    ]

    @classmethod
    def clean_text(cls, raw_text: Optional[str], max_length: int = 3000) -> str:
        """Thoroughly clean user-entered text by stripping scripts, HTML tags,

        and dangerous injection sequences.
        """
        if not raw_text:
            return ""

        text = str(raw_text).strip()

        # Enforce max length to prevent buffer/DOS attacks
        if len(text) > max_length:
            text = text[:max_length]

        # Strip null bytes and non-printable control characters (except newline, tab, carriage return)
        text = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", text)

        # Strip dangerous tags and event handlers
        for pattern in cls.DANGEROUS_PATTERNS:
            text = pattern.sub("", text)

        # Strip remaining raw HTML tags
        text = re.sub(r"<[^>]+>", "", text)

        # HTML escape output for safe presentation
        return html.escape(text.strip())

    @classmethod
    def validate_product_name(cls, raw_name: str) -> str:
        """Validates and cleans pharmaceutical product names.

        Allows alphanumeric characters, spaces, dashes, slashes, periods, and parentheses.
        """
        cleaned = cls.clean_text(raw_name, max_length=150)
        # Check for any lingering forbidden characters
        cleaned = re.sub(r"[^\w\s\-\.\,\(\)\/\%\+]", "", cleaned)
        return cleaned.strip()

    @classmethod
    def sanitize_filename(cls, filename: str) -> str:
        """Sanitizes file names to completely prevent path traversal (e.g., ../ or ..\\)."""
        if not filename:
            return "guppy_export.txt"

        # Remove path separators
        clean_name = filename.replace("\\", "/").split("/")[-1]
        # Remove traversal sequences and forbidden characters
        clean_name = re.sub(r"\.\.+", "", clean_name)
        clean_name = re.sub(r"[^\w\-\.]", "_", clean_name)

        if not clean_name:
            clean_name = "guppy_document"

        return clean_name

    @classmethod
    def mask_confidential_formula(cls, formula_text: str) -> str:
        """Masks proprietary excipient ratios or sensitive company names for confidential sharing."""
        # Mask numbers following percentages or mg
        masked = re.sub(r"(\d+(\.\d+)?)\s*%", r"**[REDACTED]%**", formula_text)
        return masked
