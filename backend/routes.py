"""API Routes"""
from flask import Blueprint, jsonify, request
from datetime import datetime
import time

api = Blueprint('api', __name__)

@api.route('/api/logs', methods=['POST'])
def add_log():
    """Add new log entry"""
    from app import blockchain, db
    
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


@api.route('/api/stats', methods=['GET'])
def get_stats():
    """Get system statistics"""
    from app import blockchain
    
    chain_data = blockchain.get_chain_data()
    
    return jsonify({
        'total_blocks': len(chain_data),
        'chain_valid': blockchain.is_chain_valid(),
        'current_epoch': blockchain.keychain.current_epoch,
        'authority_nodes': len(blockchain.consensus.authority_nodes)
    })


@api.route('/api/verify', methods=['POST'])
def verify_log():
    """Verify log integrity"""
    from app import blockchain
    
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
