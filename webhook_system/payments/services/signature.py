import hmac
import hashlib
from typing import Optional

def compute_signature(secret: str, raw_body: bytes) -> str:
    return hmac.new(secret.encode("utf-8"), raw_body, hashlib.sha256).hexdigest()

def verify_signature(secret: str, raw_body: bytes, provided: Optional[str]) -> bool:
    if not provided:
        return False
    expected = compute_signature(secret, raw_body)
    return hmac.compare_digest(expected, provided)