"""
Database Models
Data structure definitions
"""
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class BlockModel:
    """Block data model"""
    index: int
    timestamp: float
    data: Dict[str, Any]
    previous_hash: str
    nonce: int
    hash: str
    miner_id: str
    difficulty: int


@dataclass
class KeyEpochModel:
    """Key epoch data model"""
    epoch: int
    public_key_bytes: bytes
    start_time: str
    algorithm: str


@dataclass
class AuthorityNodeModel:
    """Authority node data model"""
    node_id: str
    registered_at: str
    is_active: bool
