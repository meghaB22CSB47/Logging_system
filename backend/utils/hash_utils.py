"""
Hash Utilities
Helper functions for hashing operations
"""
import hashlib


def sha256_hash(data: str) -> str:
    """Compute SHA-256 hash"""
    return hashlib.sha256(data.encode()).hexdigest()


def sha512_hash(data: str) -> str:
    """Compute SHA-512 hash"""
    return hashlib.sha512(data.encode()).hexdigest()


def double_sha256(data: str) -> str:
    """Double SHA-256 (like Bitcoin)"""
    first_hash = hashlib.sha256(data.encode()).digest()
    return hashlib.sha256(first_hash).hexdigest()
