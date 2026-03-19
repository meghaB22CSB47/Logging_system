"""
Blockchain Module
Main blockchain implementation integrating all components
"""
import time
from typing import List, Dict, Any
from backend.blockchain.block import Block
from backend.blockchain.consensus import HybridConsensus
from backend.crypto.forward_secure_keys import ForwardSecureKeychain


class Blockchain:
    """
    Main Blockchain class with forward security and hybrid consensus
    """
    
    def __init__(self, difficulty: int = 3):
        self.chain: List[Block] = []
        self.difficulty = difficulty
        
        # Initialize hybrid consensus
        self.consensus = HybridConsensus(
            difficulty_trusted=2,
            difficulty_untrusted=difficulty
        )
        
        # Initialize forward-secure keychain
        self.keychain = ForwardSecureKeychain(rotation_interval_hours=24)
        
        # Create genesis block
        self.create_genesis_block()
        
        print(f"✅ Blockchain initialized (difficulty={difficulty})")
    
    def create_genesis_block(self) -> None:
        """Create the first block in the chain"""
        genesis = Block(
            index=0,
            timestamp=time.time(),
            data={"message": "Genesis Block - Cryptographic Log Security System"},
            previous_hash="0",
            miner_id="GENESIS"
        )
        
        # Sign genesis with forward-secure key
        sig_info = self.keychain.sign_log(genesis.to_dict())
        genesis.data['forward_signature'] = sig_info
        genesis.data['signing_epoch'] = sig_info['epoch']
        
        # Mine genesis
        genesis.mine_block(self.difficulty)
        
        self.chain.append(genesis)
        print(f"📦 Genesis block created")
    
    def add_block(self, data: Dict[str, Any], miner_id: str = "SYSTEM") -> Block:
        """Add new block to blockchain"""
        previous = self.chain[-1]
        
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            data=data.copy(),
            previous_hash=previous.hash,
            miner_id=miner_id
        )
        
        # Sign with forward-secure key
        sig_info = self.keychain.sign_log(new_block.to_dict())
        new_block.data['forward_signature'] = sig_info
        new_block.data['signing_epoch'] = sig_info['epoch']
        new_block.data['miner_id'] = miner_id
        
        # Get difficulty from consensus
        difficulty = self.consensus.get_mining_difficulty(miner_id)
        new_block.data['difficulty_used'] = difficulty
        new_block.data['is_authority'] = self.consensus.is_authority_node(miner_id)
        
        # Mine block
        new_block.mine_block(difficulty)
        
        # Validate and add
        if self.consensus.validate_block(new_block, miner_id):
            self.chain.append(new_block)
            return new_block
        
        return None
    
    def is_chain_valid(self) -> bool:
        """Validate entire blockchain"""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            
            # Check hash integrity
            if current.hash != current.calculate_hash():
                print(f"❌ Block {i}: Hash mismatch")
                return False
            
            # Check chain linkage
            if current.previous_hash != previous.hash:
                print(f"❌ Block {i}: Broken link")
                return False
            
            # Check proof-of-work
            miner_id = current.data.get('miner_id', 'UNKNOWN')
            difficulty = self.consensus.get_mining_difficulty(miner_id)
            if not current.hash.startswith("0" * difficulty):
                print(f"❌ Block {i}: Invalid PoW")
                return False
            
            # Check forward-secure signature
            if 'forward_signature' in current.data:
                sig_info = current.data['forward_signature']
                block_data = {k: v for k, v in current.to_dict().items()}
                if not self.keychain.verify_log(block_data, sig_info):
                    print(f"❌ Block {i}: Invalid signature")
                    return False
        
        return True
    
    def get_chain_data(self) -> List[Dict[str, Any]]:
        """Get all blocks as dictionaries"""
        return [block.to_dict() for block in self.chain]
    
    def get_block_by_index(self, index: int) -> Dict[str, Any]:
        """Get specific block"""
        if 0 <= index < len(self.chain):
            return self.chain[index].to_dict()
        return None
