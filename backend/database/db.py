"""
Database Module
SQLite database operations for blockchain persistence
"""
import sqlite3
import json
from typing import List, Dict, Any


class Database:
    """SQLite database manager"""
    
    def __init__(self, db_path: str = "blockchain.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_tables()
        print(f"💾 Database connected: {db_path}")
    
    def _create_tables(self):
        """Create database schema"""
        # Blocks table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS blocks (
                block_index INTEGER PRIMARY KEY,
                timestamp REAL NOT NULL,
                data TEXT NOT NULL,
                previous_hash TEXT NOT NULL,
                nonce INTEGER NOT NULL,
                hash TEXT UNIQUE NOT NULL,
                miner_id TEXT,
                difficulty INTEGER,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Key epochs table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS key_epochs (
                epoch INTEGER PRIMARY KEY,
                public_key_bytes BLOB NOT NULL,
                start_time TEXT NOT NULL,
                algorithm TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Authority nodes table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS authority_nodes (
                node_id TEXT PRIMARY KEY,
                registered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        """)
        
        self.conn.commit()
    
    def save_block(self, block) -> bool:
        """Save block to database"""
        try:
            self.cursor.execute("""
                INSERT INTO blocks VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (
                block.index,
                block.timestamp,
                json.dumps(block.data),
                block.previous_hash,
                block.nonce,
                block.hash,
                block.miner_id,
                block.difficulty
            ))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error saving block: {e}")
            return False
    
    def load_all_blocks(self) -> List[Dict[str, Any]]:
        """Load all blocks"""
        self.cursor.execute("SELECT * FROM blocks ORDER BY block_index")
        return [
            {
                'index': r[0],
                'timestamp': r[1],
                'data': json.loads(r[2]),
                'previous_hash': r[3],
                'nonce': r[4],
                'hash': r[5],
                'miner_id': r[6],
                'difficulty': r[7]
            }
            for r in self.cursor.fetchall()
        ]
    
    def save_key_epoch(self, epoch: int, public_key_bytes: bytes, 
                       start_time: str, algorithm: str):
        """Save key epoch"""
        try:
            self.cursor.execute("""
                INSERT INTO key_epochs VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (epoch, public_key_bytes, start_time, algorithm))
            self.conn.commit()
        except:
            pass
    
    def save_authority_node(self, node_id: str):
        """Save authority node"""
        try:
            self.cursor.execute("""
                INSERT INTO authority_nodes (node_id) VALUES (?)
            """, (node_id,))
            self.conn.commit()
            return True
        except:
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        self.cursor.execute("SELECT COUNT(*) FROM blocks")
        total_blocks = self.cursor.fetchone()[0]
        
        self.cursor.execute("SELECT COUNT(*) FROM key_epochs")
        total_epochs = self.cursor.fetchone()[0]
        
        return {
            'total_blocks': total_blocks,
            'total_epochs': total_epochs
        }
