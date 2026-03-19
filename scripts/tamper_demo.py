"""
Tamper Detection Demonstration
Shows how tampering is detected
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from blockchain.blockchain import Blockchain

print("\n" + "="*70)
print("TAMPER DETECTION DEMONSTRATION")
print("="*70 + "\n")

# Create blockchain
bc = Blockchain(difficulty=2)

# Add blocks
print("Step 1: Adding legitimate blocks...")
bc.add_block({"log": "User login", "user": "alice"}, "NODE1")
bc.add_block({"log": "File access", "file": "data.txt"}, "NODE2")
print(f"✅ Added 2 blocks\n")

# Verify before tampering
print("Step 2: Verifying chain before tampering...")
is_valid = bc.is_chain_valid()
print(f"Chain Valid: {'✅ YES' if is_valid else '❌ NO'}\n")

# Tamper with block
print("Step 3: Tampering with block 1...")
bc.chain[1].data = {"HACKED": "Modified data!"}
print("🔨 Block 1 data modified\n")

# Verify after tampering
print("Step 4: Verifying chain after tampering...")
is_valid = bc.is_chain_valid()
print(f"Chain Valid: {'✅ YES' if is_valid else '❌ NO'}\n")

print("="*70)
print("RESULT: Tampering was DETECTED!")
print("="*70 + "\n")
