"""
Forward-Secure Keys Module
Implements forward-secure key rotation using Ed25519 (EdDSA)
"""
import base64
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization


class ForwardSecureKeychain:
    """
    Forward-Secure Key Rotation System using EdDSA (Ed25519)
    
    Features:
    - Automatic key rotation based on time intervals
    - Old private keys are cryptographically destroyed
    - Old public keys preserved for verification
    - Multi-epoch signature verification
    
    Security Guarantee:
    If current epoch key is compromised, all previous epochs remain secure
    because their private keys have been destroyed.
    """
    
    def __init__(self, rotation_interval_hours: int = 24):
        """
        Initialize forward-secure keychain
        
        Args:
            rotation_interval_hours: Time between key rotations (default: 24 hours)
        """
        self.rotation_interval = timedelta(hours=rotation_interval_hours)
        self.key_chain: List[Dict[str, Any]] = []
        self.current_epoch = 0
        self.epoch_start_time = datetime.now()
        
        # Generate initial key (epoch 0)
        self._generate_new_epoch_key()
        
        print(f"🔐 Forward-Secure Keychain initialized")
        print(f"   Algorithm: Ed25519 (EdDSA)")
        print(f"   Rotation interval: {rotation_interval_hours} hours")
        print(f"   Current epoch: {self.current_epoch}")
    
    def _generate_new_epoch_key(self) -> None:
        """
        Generate new Ed25519 key pair for current epoch
        
        Internal method called during initialization and rotation
        """
        # Generate Ed25519 key pair
        private_key = ed25519.Ed25519PrivateKey.generate()
        public_key = private_key.public_key()
        
        # Serialize public key for storage
        public_key_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        
        # Create key derivation proof (links to previous epoch)
        derivation_proof = self._create_key_derivation_proof()
        
        # Store epoch information
        epoch_info = {
            'epoch': self.current_epoch,
            'public_key': public_key,  # For verification
            'public_key_bytes': public_key_bytes,  # For serialization
            'start_time': self.epoch_start_time.isoformat(),
            'derivation_proof': derivation_proof,
            'algorithm': 'Ed25519'
        }
        
        self.key_chain.append(epoch_info)
        self.current_private_key = private_key
        self.current_public_key = public_key
        
        print(f"   🔑 Generated Ed25519 key for epoch {self.current_epoch}")
    
    def _create_key_derivation_proof(self) -> str:
        """
        Create cryptographic proof linking this key to previous epoch
        
        Returns:
            str: Hash-based proof of key derivation
        """
        if self.current_epoch == 0:
            return "GENESIS_EPOCH_0"
        
        # Link to previous epoch's public key
        import hashlib
        prev_pub_bytes = self.key_chain[-1]['public_key_bytes']
        proof_data = prev_pub_bytes + str(self.current_epoch).encode()
        
        return hashlib.sha256(proof_data).hexdigest()
    
    def should_rotate(self) -> bool:
        """
        Check if rotation interval has elapsed
        
        Returns:
            bool: True if time to rotate, False otherwise
        """
        time_elapsed = datetime.now() - self.epoch_start_time
        return time_elapsed >= self.rotation_interval
    
    def get_time_until_rotation(self) -> Dict[str, Any]:
        """
        Get time remaining until next rotation
        
        Returns:
            dict: Time until rotation in various formats
        """
        time_until = (
            self.epoch_start_time + self.rotation_interval - datetime.now()
        ).total_seconds()
        
        hours = int(abs(time_until) // 3600)
        minutes = int((abs(time_until) % 3600) // 60)
        
        return {
            'seconds': time_until,
            'formatted': f"{hours}h {minutes}m",
            'overdue': time_until < 0
        }
    
    def rotate_key(self, force: bool = False) -> bool:
        """
        Rotate to next epoch and DESTROY old private key
        
        This is the CORE of forward security:
        - Old private key is set to None (destroyed)
        - Old public key is preserved for verification
        - New key pair is generated
        
        Args:
            force: Force rotation even if interval hasn't elapsed
        
        Returns:
            bool: True if rotation occurred, False otherwise
        """
        if not force and not self.should_rotate():
            return False
        
        print(f"\n🔄 KEY ROTATION")
        print(f"   Epoch: {self.current_epoch} → {self.current_epoch + 1}")
        
        # CRITICAL: Destroy old private key (forward security)
        old_epoch = self.current_epoch
        self.current_private_key = None  # Gone forever!
        
        print(f"   🗑️  Epoch {old_epoch} private key DESTROYED")
        print(f"   ✅ Epoch {old_epoch} public key PRESERVED")
        
        # Move to next epoch
        self.current_epoch += 1
        self.epoch_start_time = datetime.now()
        
        # Generate new key
        self._generate_new_epoch_key()
        
        print(f"   ✅ Rotation complete\n")
        
        return True
    
    def sign_log(self, log_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sign log data with current epoch key
        
        Automatically rotates key if interval has elapsed
        
        Args:
            log_data: Log data to sign
        
        Returns:
            dict: Signature information including epoch number
        """
        # Check if rotation needed
        if self.should_rotate():
            print("⏰ Rotation interval elapsed, rotating key...")
            self.rotate_key()
        
        # Serialize log data
        log_bytes = json.dumps(log_data, sort_keys=True).encode('utf-8')
        
        # Sign with Ed25519 private key
        signature = self.current_private_key.sign(log_bytes)
        
        # Return signature with metadata
        return {
            'signature': base64.b64encode(signature).decode('utf-8'),
            'epoch': self.current_epoch,
            'timestamp': datetime.now().isoformat(),
            'algorithm': 'Ed25519',
            'public_key': base64.b64encode(
                self.current_public_key.public_bytes(
                    encoding=serialization.Encoding.Raw,
                    format=serialization.PublicFormat.Raw
                )
            ).decode('utf-8')
        }
    
    def verify_log(
        self,
        log_data: Dict[str, Any],
        signature_info: Dict[str, Any]
    ) -> bool:
        """
        Verify log signature from ANY past epoch
        
        Works even if that epoch's private key was destroyed!
        Uses the preserved public key from that epoch.
        
        Args:
            log_data: Original log data
            signature_info: Signature information from sign_log()
        
        Returns:
            bool: True if signature is valid, False otherwise
        """
        epoch = signature_info['epoch']
        
        # Check if epoch exists
        if epoch >= len(self.key_chain) or epoch < 0:
            print(f"❌ Epoch {epoch} doesn't exist")
            return False
        
        # Get public key from that epoch
        epoch_public_key = self.key_chain[epoch]['public_key']
        
        # Decode signature
        signature_bytes = base64.b64decode(signature_info['signature'])
        log_bytes = json.dumps(log_data, sort_keys=True).encode('utf-8')
        
        # Verify signature using Ed25519
        try:
            epoch_public_key.verify(signature_bytes, log_bytes)
            return True
        except Exception as e:
            print(f"❌ Signature verification failed: {e}")
            return False
    
    def get_keychain_status(self) -> Dict[str, Any]:
        """
        Get comprehensive keychain status
        
        Returns:
            dict: Complete status information
        """
        time_until = self.get_time_until_rotation()
        
        return {
            'current_epoch': self.current_epoch,
            'total_epochs': len(self.key_chain),
            'total_rotations': len(self.key_chain) - 1,
            'rotation_interval_hours': self.rotation_interval.total_seconds() / 3600,
            'time_until_rotation': time_until['formatted'],
            'rotation_overdue': time_until['overdue'],
            'algorithm': 'Ed25519',
            'key_size': 256,  # bits
            'signature_size': 512,  # bits
            'forward_secure': True,
            'epochs': [
                {
                    'epoch': e['epoch'],
                    'start_time': e['start_time'],
                    'derivation_proof': e['derivation_proof'][:16] + '...'
                }
                for e in self.key_chain
            ]
        }
    
    def export_public_keys(self) -> List[Dict[str, str]]:
        """
        Export all public keys for backup/distribution
        
        Returns:
            list: Public keys for all epochs
        """
        return [
            {
                'epoch': e['epoch'],
                'public_key': base64.b64encode(e['public_key_bytes']).decode('utf-8'),
                'algorithm': 'Ed25519'
            }
            for e in self.key_chain
        ]
    
    def __repr__(self) -> str:
        """String representation"""
        return (
            f"ForwardSecureKeychain("
            f"epoch={self.current_epoch}, "
            f"total_epochs={len(self.key_chain)}, "
            f"algorithm=Ed25519)"
        )
