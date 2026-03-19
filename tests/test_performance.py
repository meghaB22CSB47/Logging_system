"""
Test Performance
Benchmark system performance
"""
import sys
import os
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from blockchain.blockchain import Blockchain
from crypto.forward_secure_keys import ForwardSecureKeychain

def benchmark_signature_speed():
    """Benchmark EdDSA signature speed"""
    keychain = ForwardSecureKeychain()
    
    iterations = 100
    start = time.time()
    
    for i in range(iterations):
        log = {"test": f"data_{i}"}
        keychain.sign_log(log)
    
    elapsed = time.time() - start
    per_op = (elapsed / iterations) * 1000
    
    print(f"✅ Signature speed: {per_op:.2f}ms per operation")
    print(f"   ({iterations} signatures in {elapsed:.2f}s)")

def benchmark_verification_speed():
    """Benchmark signature verification speed"""
    keychain = ForwardSecureKeychain()
    
    # Create signatures
    signatures = []
    for i in range(100):
        log = {"test": f"data_{i}"}
        sig = keychain.sign_log(log)
        signatures.append((log, sig))
    
    # Benchmark verification
    start = time.time()
    for log, sig in signatures:
        keychain.verify_log(log, sig)
    
    elapsed = time.time() - start
    per_op = (elapsed / len(signatures)) * 1000
    
    print(f"✅ Verification speed: {per_op:.2f}ms per operation")
    print(f"   ({len(signatures)} verifications in {elapsed:.2f}s)")

def benchmark_mining_speed():
    """Benchmark PoW mining speed"""
    bc = Blockchain(difficulty=3)
    
    iterations = 5
    start = time.time()
    
    for i in range(iterations):
        bc.add_block({"log": f"Block {i}"}, "NODE")
    
    elapsed = time.time() - start
    per_block = elapsed / iterations
    
    print(f"✅ Mining speed: {per_block:.2f}s per block (difficulty 3)")
    print(f"   ({iterations} blocks in {elapsed:.2f}s)")

def benchmark_hybrid_consensus():
    """Benchmark hybrid consensus performance"""
    bc = Blockchain(difficulty=3)
    
    # Register authority node
    bc.consensus.register_authority_node("TRUSTED", {'is_verified': True})
    
    # Mine with authority node
    start = time.time()
    bc.add_block({"log": "Authority"}, "TRUSTED")
    authority_time = time.time() - start
    
    # Mine with regular node
    start = time.time()
    bc.add_block({"log": "Regular"}, "REGULAR")
    regular_time = time.time() - start
    
    speedup = regular_time / authority_time
    
    print(f"✅ Hybrid consensus performance:")
    print(f"   Authority node: {authority_time:.2f}s")
    print(f"   Regular node: {regular_time:.2f}s")
    print(f"   Speedup: {speedup:.1f}x")

if __name__ == '__main__':
    print("\n" + "="*70)
    print("PERFORMANCE BENCHMARKS")
    print("="*70 + "\n")
    
    benchmark_signature_speed()
    print()
    benchmark_verification_speed()
    print()
    benchmark_mining_speed()
    print()
    benchmark_hybrid_consensus()
    
    print("\n" + "="*70)
    print("✅ ALL BENCHMARKS COMPLETE")
    print("="*70 + "\n")
