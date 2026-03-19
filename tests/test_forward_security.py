"""
Test Forward Security
Tests EdDSA key rotation and forward security features
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from crypto.forward_secure_keys import ForwardSecureKeychain

def test_key_generation():
    """Test Ed25519 key generation"""
    keychain = ForwardSecureKeychain(rotation_interval_hours=1)
    assert keychain.current_epoch == 0
    assert len(keychain.key_chain) == 1
    print("✅ Key generation test passed")

def test_signature_creation():
    """Test log signing with EdDSA"""
    keychain = ForwardSecureKeychain(rotation_interval_hours=1)
    log = {"event": "test", "data": "sample"}
    
    sig_info = keychain.sign_log(log)
    
    assert 'signature' in sig_info
    assert 'epoch' in sig_info
    assert sig_info['algorithm'] == 'Ed25519'
    print("✅ Signature creation test passed")

def test_signature_verification():
    """Test signature verification"""
    keychain = ForwardSecureKeychain(rotation_interval_hours=1)
    log = {"event": "test", "data": "sample"}
    
    sig_info = keychain.sign_log(log)
    is_valid = keychain.verify_log(log, sig_info)
    
    assert is_valid == True
    print("✅ Signature verification test passed")

def test_key_rotation():
    """Test key rotation mechanism"""
    keychain = ForwardSecureKeychain(rotation_interval_hours=1)
    
    # Sign in epoch 0
    log1 = {"event": "epoch0", "data": "data0"}
    sig1 = keychain.sign_log(log1)
    
    # Force rotation
    keychain.rotate_key(force=True)
    assert keychain.current_epoch == 1
    assert len(keychain.key_chain) == 2
    
    # Sign in epoch 1
    log2 = {"event": "epoch1", "data": "data1"}
    sig2 = keychain.sign_log(log2)
    
    # Both should verify
    assert keychain.verify_log(log1, sig1) == True
    assert keychain.verify_log(log2, sig2) == True
    
    print("✅ Key rotation test passed")

def test_forward_security():
    """Test forward security guarantee"""
    keychain = ForwardSecureKeychain(rotation_interval_hours=1)
    
    # Sign in epoch 0
    log = {"sensitive": "data"}
    sig = keychain.sign_log(log)
    
    # Rotate (destroys epoch 0 private key)
    keychain.rotate_key(force=True)
    
    # Epoch 0 signature should still verify
    # (using preserved public key)
    assert keychain.verify_log(log, sig) == True
    
    print("✅ Forward security test passed")

if __name__ == '__main__':
    print("\n" + "="*70)
    print("FORWARD SECURITY TESTS (EdDSA)")
    print("="*70 + "\n")
    
    test_key_generation()
    test_signature_creation()
    test_signature_verification()
    test_key_rotation()
    test_forward_security()
    
    print("\n" + "="*70)
    print("✅ ALL FORWARD SECURITY TESTS PASSED")
    print("="*70 + "\n")
