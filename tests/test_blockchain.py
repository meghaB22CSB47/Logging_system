"""Test blockchain functionality"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from blockchain.blockchain import Blockchain

def test_blockchain_creation():
    bc = Blockchain(difficulty=2)
    assert len(bc.chain) == 1
    print("✅ Blockchain creation test passed")

def test_add_block():
    bc = Blockchain(difficulty=2)
    bc.add_block({"log": "Test log"}, "TEST_NODE")
    assert len(bc.chain) == 2
    print("✅ Add block test passed")

def test_chain_validation():
    bc = Blockchain(difficulty=2)
    bc.add_block({"log": "Log 1"}, "NODE1")
    assert bc.is_chain_valid()
    print("✅ Chain validation test passed")

if __name__ == '__main__':
    test_blockchain_creation()
    test_add_block()
    test_chain_validation()
    print("\n✅ ALL TESTS PASSED")
