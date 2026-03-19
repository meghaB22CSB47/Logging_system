"""
Test Tamper Detection
Tests blockchain tamper detection capabilities
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from blockchain.blockchain import Blockchain

def test_valid_chain():
    """Test that valid chain passes validation"""
    bc = Blockchain(difficulty=2)
    bc.add_block({"log": "Log 1"}, "NODE1")
    bc.add_block({"log": "Log 2"}, "NODE2")
    
    assert bc.is_chain_valid() == True
    print("✅ Valid chain test passed")

def test_data_tampering():
    """Test detection of data tampering"""
    bc = Blockchain(difficulty=2)
    bc.add_block({"log": "Original data"}, "NODE1")
    
    # Tamper with data
    bc.chain[1].data = {"log": "TAMPERED"}
    
    assert bc.is_chain_valid() == False
    print("✅ Data tampering detection test passed")

def test_hash_tampering():
    """Test detection of hash tampering"""
    bc = Blockchain(difficulty=2)
    bc.add_block({"log": "Data"}, "NODE1")
    
    # Tamper with hash
    bc.chain[1].hash = "0000fake_hash"
    
    assert bc.is_chain_valid() == False
    print("✅ Hash tampering detection test passed")

def test_chain_break():
    """Test detection of broken chain links"""
    bc = Blockchain(difficulty=2)
    bc.add_block({"log": "Log 1"}, "NODE1")
    bc.add_block({"log": "Log 2"}, "NODE2")
    
    # Break chain link
    bc.chain[2].previous_hash = "wrong_hash"
    
    assert bc.is_chain_valid() == False
    print("✅ Chain break detection test passed")

if __name__ == '__main__':
    print("\n" + "="*70)
    print("TAMPER DETECTION TESTS")
    print("="*70 + "\n")
    
    test_valid_chain()
    test_data_tampering()
    test_hash_tampering()
    test_chain_break()
    
    print("\n" + "="*70)
    print("✅ ALL TAMPER DETECTION TESTS PASSED")
    print("="*70 + "\n")
