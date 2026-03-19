"""
Consensus Module
Implements Hybrid Proof-of-Work + Proof-of-Authority consensus mechanism
"""
from typing import Set, Dict, Any


class HybridConsensus:
    """
    Hybrid Consensus Mechanism combining PoW and PoA
    
    Features:
    - Proof-of-Work for untrusted nodes (high difficulty)
    - Proof-of-Authority for trusted nodes (low difficulty)
    - Dynamic difficulty adjustment based on node trust level
    
    Attributes:
        authority_nodes (set): Set of trusted node IDs
        difficulty_trusted (int): Mining difficulty for authority nodes
        difficulty_untrusted (int): Mining difficulty for regular nodes
    """
    
    def __init__(
        self,
        difficulty_trusted: int = 2,
        difficulty_untrusted: int = 4
    ):
        """
        Initialize hybrid consensus
        
        Args:
            difficulty_trusted: PoW difficulty for authority nodes (default: 2)
            difficulty_untrusted: PoW difficulty for regular nodes (default: 4)
        """
        self.authority_nodes: Set[str] = set()
        self.difficulty_trusted = difficulty_trusted
        self.difficulty_untrusted = difficulty_untrusted
        self.total_blocks_mined = 0
        self.blocks_by_authorities = 0
        
        print(f"🔄 Hybrid Consensus initialized:")
        print(f"   Authority (PoA) difficulty: {difficulty_trusted}")
        print(f"   Regular (PoW) difficulty: {difficulty_untrusted}")
    
    def register_authority_node(
        self,
        node_id: str,
        proof: Dict[str, Any]
    ) -> bool:
        """
        Register a node as trusted authority
        
        Args:
            node_id: Unique identifier for the node
            proof: Verification proof (e.g., credentials, signatures)
        
        Returns:
            bool: True if successfully registered, False otherwise
        """
        # Verify proof of authority
        if not proof.get('is_verified', False):
            print(f"❌ {node_id}: Authority verification failed")
            return False
        
        if node_id in self.authority_nodes:
            print(f"⚠️  {node_id}: Already registered as authority")
            return False
        
        self.authority_nodes.add(node_id)
        print(f"✅ {node_id}: Registered as authority node")
        print(f"   Mining difficulty: {self.difficulty_trusted}")
        print(f"   Speedup factor: {self.difficulty_untrusted / self.difficulty_trusted:.1f}x")
        
        return True
    
    def revoke_authority(self, node_id: str) -> bool:
        """
        Revoke authority status from a node
        
        Args:
            node_id: Node to revoke authority from
        
        Returns:
            bool: True if successfully revoked
        """
        if node_id in self.authority_nodes:
            self.authority_nodes.remove(node_id)
            print(f"🔒 {node_id}: Authority revoked")
            return True
        return False
    
    def is_authority_node(self, node_id: str) -> bool:
        """
        Check if node has authority status
        
        Args:
            node_id: Node ID to check
        
        Returns:
            bool: True if node is authority, False otherwise
        """
        return node_id in self.authority_nodes
    
    def get_mining_difficulty(self, node_id: str) -> int:
        """
        Get appropriate mining difficulty for node
        
        Args:
            node_id: Node requesting difficulty
        
        Returns:
            int: Mining difficulty (low for authority, high for regular)
        """
        if self.is_authority_node(node_id):
            return self.difficulty_trusted
        else:
            return self.difficulty_untrusted
    
    def validate_block(self, block, miner_id: str) -> bool:
        """
        Validate block based on consensus rules
        
        Args:
            block: Block to validate
            miner_id: ID of node that mined the block
        
        Returns:
            bool: True if block is valid according to consensus
        """
        # Get expected difficulty for this miner
        expected_difficulty = self.get_mining_difficulty(miner_id)
        required_prefix = "0" * expected_difficulty
        
        # Check if block meets difficulty requirement
        if not block.hash.startswith(required_prefix):
            print(f"❌ Block {block.index}: Invalid PoW")
            print(f"   Expected: {required_prefix}...")
            print(f"   Got: {block.hash[:expected_difficulty]}...")
            return False
        
        # Track statistics
        self.total_blocks_mined += 1
        if self.is_authority_node(miner_id):
            self.blocks_by_authorities += 1
        
        return True
    
    def get_consensus_stats(self) -> Dict[str, Any]:
        """
        Get consensus statistics
        
        Returns:
            dict: Statistics about consensus performance
        """
        authority_percentage = (
            (self.blocks_by_authorities / self.total_blocks_mined * 100)
            if self.total_blocks_mined > 0 else 0
        )
        
        return {
            'total_blocks': self.total_blocks_mined,
            'authority_blocks': self.blocks_by_authorities,
            'regular_blocks': self.total_blocks_mined - self.blocks_by_authorities,
            'authority_percentage': f"{authority_percentage:.1f}%",
            'total_authorities': len(self.authority_nodes),
            'authority_list': list(self.authority_nodes),
            'difficulty_trusted': self.difficulty_trusted,
            'difficulty_untrusted': self.difficulty_untrusted,
            'speedup_factor': f"{self.difficulty_untrusted / self.difficulty_trusted:.1f}x"
        }
    
    def adjust_difficulty(
        self,
        new_trusted: int = None,
        new_untrusted: int = None
    ) -> None:
        """
        Dynamically adjust mining difficulty
        
        Args:
            new_trusted: New difficulty for authority nodes
            new_untrusted: New difficulty for regular nodes
        """
        if new_trusted is not None:
            old_trusted = self.difficulty_trusted
            self.difficulty_trusted = new_trusted
            print(f"🔧 Authority difficulty: {old_trusted} → {new_trusted}")
        
        if new_untrusted is not None:
            old_untrusted = self.difficulty_untrusted
            self.difficulty_untrusted = new_untrusted
            print(f"🔧 Regular difficulty: {old_untrusted} → {new_untrusted}")
    
    def __repr__(self) -> str:
        """String representation"""
        return (
            f"HybridConsensus("
            f"authorities={len(self.authority_nodes)}, "
            f"diff_trusted={self.difficulty_trusted}, "
            f"diff_untrusted={self.difficulty_untrusted})"
        )
