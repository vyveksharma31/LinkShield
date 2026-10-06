"""Pydantic schemas for request validation."""
import re
from pydantic import BaseModel, Field, field_validator


DANGEROUS_SCHEMES = ("javascript:", "data:", "file:", "vbscript:", "blob:", "about:")


class AnalyzeRequest(BaseModel):
    """URL analysis request payload."""

    url: str = Field(
        ...,
        min_length=3,
        max_length=2048,
        description="The target URL to analyze for phishing and malicious indicators.",
        examples=["https://secure-login.paypal.com.account-update.xyz/verify"],
    )

    @field_validator("url")
    @classmethod
    def validate_url_syntax(cls, v: str) -> str:
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("URL cannot be empty or whitespace only.")

        lower_url = cleaned.lower()
        for scheme in DANGEROUS_SCHEMES:
            if lower_url.startswith(scheme):
                raise ValueError(f"Dangerous or non-web scheme '{scheme}' is not permitted.")

        # Ensure no embedded control characters or newlines
        if re.search(r"[\r\n\t\x00-\x1f]", cleaned):
            raise ValueError("URL contains illegal control characters.")

        return cleaned
