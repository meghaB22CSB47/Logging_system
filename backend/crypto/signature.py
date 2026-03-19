"""
Signature Module
Additional signature utilities and helpers
"""
from backend.crypto.forward_secure_keys import ForwardSecureKeychain

def create_keychain(rotation_hours: int = 24) -> ForwardSecureKeychain:
    """
    Create new forward-secure keychain
    
    Args:
        rotation_hours: Hours between key rotations
    
    Returns:
        ForwardSecureKeychain: Initialized keychain
    """
    return ForwardSecureKeychain(rotation_interval_hours=rotation_hours)


def sign_data(keychain: ForwardSecureKeychain, data: dict) -> dict:
    """
    Sign data with current epoch key
    
    Args:
        keychain: Active keychain
        data: Data to sign
    
    Returns:
        dict: Signature information
    """
    return keychain.sign_log(data)


def verify_signature(keychain: ForwardSecureKeychain, data: dict, signature: dict) -> bool:
    """
    Verify signature
    
    Args:
        keychain: Active keychain
        data: Original data
        signature: Signature information
    
    Returns:
        bool: True if valid
    """
    return keychain.verify_log(data, signature)
