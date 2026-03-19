"""
Main Flask Application
Cryptographic Log Security System
"""
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import sys
import time
from datetime import datetime

# Add backend directory to path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

# Now import our modules
try:
    from blockchain.blockchain import Blockchain
    from database.db import Database
except ImportError as e:
    print(f"Import Error: {e}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Python path: {sys.path}")
    print("\nMake sure you have these files:")
    print("  - backend/blockchain/blockchain.py")
    print("  - backend/blockchain/block.py")
    print("  - backend/blockchain/consensus.py")
    print("  - backend/crypto/forward_secure_keys.py")
    print("  - backend/database/db.py")
    print("\nAnd __init__.py files in each folder!")
    sys.exit(1)

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Initialize components
try:
    db = Database("blockchain.db")
    blockchain = Blockchain(difficulty=3)

    # Register authority nodes
    blockchain.consensus.register_authority_node(
        "PRIMARY_NODE",
        {'is_verified': True, 'node_name': 'Primary Node'}
    )

    print("\n" + "="*70)
    print("CRYPTOGRAPHIC LOG SECURITY SYSTEM")
    print("="*70)
    print(f"Dashboard: http://localhost:5000")
    print(f"Current Epoch: {blockchain.keychain.current_epoch}")
    print(f"Authority Nodes: {len(blockchain.consensus.authority_nodes)}")
    print("="*70 + "\n")
except Exception as e:
    print(f"\n❌ ERROR during initialization: {e}")
    print("\nPlease ensure all files are in the correct structure.")
    sys.exit(1)


@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')


@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory('../frontend', path)


@app.route('/api/logs', methods=['POST'])
def add_log():
    """Add new log entry"""
    try:
        data = request.get_json()
        miner_id = data.pop('miner_node_id', 'WEB_CLIENT')
        
        log_entry = {
            'event_type': data.get('event_type'),
            'severity': data.get('severity'),
            'source': data.get('source'),
            'description': data.get('description', ''),
            'timestamp': time.time()
        }
        
        block = blockchain.add_block(log_entry, miner_id)
        
        if block:
            db.save_block(block)
            return jsonify({
                'success': True,
                'block_index': block.index,
                'block_hash': block.hash,
                'signing_epoch': block.data.get('signing_epoch')
            }), 201
        
        return jsonify({'error': 'Failed to add log'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get system statistics"""
    try:
        chain_data = blockchain.get_chain_data()
        
        return jsonify({
            'total_blocks': len(chain_data),
            'chain_valid': blockchain.is_chain_valid(),
            'current_epoch': blockchain.keychain.current_epoch,
            'authority_nodes': len(blockchain.consensus.authority_nodes)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/verify', methods=['POST'])
def verify_log():
    """Verify log integrity"""
    try:
        data = request.get_json()
        block_index = data.get('block_index')
        
        block = blockchain.get_block_by_index(block_index)
        
        if not block:
            return jsonify({'error': 'Block not found'}), 404
        
        # Verify signature
        sig_valid = False
        if 'forward_signature' in block['data']:
            sig_info = block['data']['forward_signature']
            block_copy = {k: v for k, v in block.items()}
            sig_valid = blockchain.keychain.verify_log(block_copy, sig_info)
        
        chain_valid = blockchain.is_chain_valid()
        
        return jsonify({
            'block_valid': True,
            'signature_valid': sig_valid,
            'chain_valid': chain_valid,
            'block_data': block
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
