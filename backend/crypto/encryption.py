"""
Encryption Module
Additional encryption utilities
"""
import hashlib
import base64
from cryptography.fernet import Fernet

def generate_encryption_key() -> bytes:
    """Generate Fernet encryption key"""
    return Fernet.generate_key()


def encrypt_data(data: str, key: bytes) -> str:
    """
    Encrypt data using Fernet symmetric encryption
    
    Args:
        data: Data to encrypt
        key: Encryption key
    
    Returns:
        str: Encrypted data (base64)
    """
    f = Fernet(key)
    encrypted = f.encrypt(data.encode())
    return base64.b64encode(encrypted).decode()


def decrypt_data(encrypted_data: str, key: bytes) -> str:
    """
    Decrypt data
    
    Args:
        encrypted_data: Encrypted data (base64)
        key: Decryption key
    
    Returns:
        str: Decrypted data
    """
    f = Fernet(key)
    encrypted = base64.b64decode(encrypted_data)
    decrypted = f.decrypt(encrypted)
    return decrypted.decode()


def hash_password(password: str) -> str:
    """
    Hash password using SHA-256
    
    Args:
        password: Plain password
    
    Returns:
        str: Hashed password
    """
    return hashlib.sha256(password.encode()).hexdigest()
