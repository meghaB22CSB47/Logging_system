const API_BASE = 'http://localhost:5000/api';

// Load statistics
async function loadStats() {
    try {
        const response = await fetch(`${API_BASE}/stats`);
        const data = await response.json();
        
        document.getElementById('totalBlocks').textContent = data.total_blocks;
        document.getElementById('chainStatus').textContent = 
            data.chain_valid ? '✅ VALID' : '❌ INVALID';
        document.getElementById('currentEpoch').textContent = data.current_epoch;
        document.getElementById('authorityNodes').textContent = data.authority_nodes;
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Handle form submission
document.getElementById('logForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const logData = {
        event_type: document.getElementById('eventType').value,
        severity: document.getElementById('severity').value,
        source: document.getElementById('source').value,
        description: document.getElementById('description').value,
        miner_node_id: 'WEB_CLIENT'
    };
    
    try {
        const response = await fetch(`${API_BASE}/logs`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(logData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showMessage('✅ Log added successfully!', 'success');
            document.getElementById('logForm').reset();
            loadStats();
        } else {
            showMessage('❌ Failed to add log', 'error');
        }
    } catch (error) {
        showMessage('❌ Error: ' + error.message, 'error');
    }
});

function showMessage(text, type) {
    const msg = document.getElementById('message');
    msg.textContent = text;
    msg.className = `message ${type}`;
    setTimeout(() => msg.style.display = 'none', 3000);
}

// Load stats on page load
loadStats();
setInterval(loadStats, 5000);
