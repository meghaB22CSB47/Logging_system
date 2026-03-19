"""
Block Module
Implements individual block structure for blockchain
"""
import hashlib
import json
import time
from typing import Dict, Any


class Block:
    """
    Individual block in the blockchain
    
    Attributes:
        index (int): Position in the blockchain
        timestamp (float): Unix timestamp of block creation
        data (dict): Log data and metadata
        previous_hash (str): Hash of previous block
        nonce (int): Proof-of-work nonce
        hash (str): SHA-256 hash of this block
        miner_id (str): ID of node that mined this block
        difficulty (int): Mining difficulty used
    """
    
    def __init__(
        self,
        index: int,
        timestamp: float,
        data: Dict[str, Any],
        previous_hash: str,
        nonce: int = 0,
        miner_id: str = "SYSTEM"
    ):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.miner_id = miner_id
        self.difficulty = data.get('difficulty_used', 3)
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """
        Calculate SHA-256 hash of block contents
        
        Returns:
            str: Hexadecimal hash string
        """
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "miner_id": self.miner_id
        }, sort_keys=True)
        
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def mine_block(self, difficulty: int) -> None:
        """
        Mine block using Proof-of-Work
        
        Args:
            difficulty (int): Number of leading zeros required in hash
        """
        target = "0" * difficulty
        start_time = time.time()
        attempts = 0
        
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
            attempts += 1
        
        mining_time = time.time() - start_time
        
        print(f"⛏️  Block #{self.index} mined:")
        print(f"   Difficulty: {difficulty}")
        print(f"   Attempts: {attempts:,}")
        print(f"   Time: {mining_time:.2f}s")
        print(f"   Hash: {self.hash[:32]}...")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert block to dictionary
        
        Returns:
            dict: Block data as dictionary
        """
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash,
            "miner_id": self.miner_id,
            "difficulty": self.difficulty
        }
    
    def __repr__(self) -> str:
        """String representation of block"""
        return f"Block(index={self.index}, hash={self.hash[:16]}...)"
