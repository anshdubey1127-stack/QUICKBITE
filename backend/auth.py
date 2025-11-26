import jwt
import bcrypt
from functools import wraps
from flask import request, jsonify
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

class AuthManager:
    """Handle authentication operations"""
    
    JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key')
    JWT_EXPIRY = int(os.getenv('JWT_EXPIRY', 604800))  # 7 days in seconds
    
    @staticmethod
    def hash_password(password):
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt(10)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    @staticmethod
    def verify_password(password, hashed_password):
        """Verify password against hash"""
        return bcrypt.checkpw(
            password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    
    @staticmethod
    def generate_token(user_id, user_email, role='user'):
        """Generate JWT token"""
        payload = {
            'user_id': str(user_id),
            'email': user_email,
            'role': role,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(seconds=AuthManager.JWT_EXPIRY)
        }
        token = jwt.encode(
            payload,
            AuthManager.JWT_SECRET,
            algorithm='HS256'
        )
        return token
    
    @staticmethod
    def verify_token(token):
        """Verify JWT token"""
        try:
            payload = jwt.decode(
                token,
                AuthManager.JWT_SECRET,
                algorithms=['HS256']
            )
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

def token_required(f):
    """Decorator to require token authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check for token in headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'success': False, 'message': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'success': False, 'message': 'Token is missing'}), 401
        
        payload = AuthManager.verify_token(token)
        if not payload:
            return jsonify({'success': False, 'message': 'Invalid or expired token'}), 401
        
        request.user_id = payload['user_id']
        request.user_email = payload['email']
        request.user_role = payload.get('role', 'user')
        
        return f(*args, **kwargs)
    
    return decorated

def seller_required(f):
    """Decorator to require seller role"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'success': False, 'message': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'success': False, 'message': 'Token is missing'}), 401
        
        payload = AuthManager.verify_token(token)
        if not payload:
            return jsonify({'success': False, 'message': 'Invalid or expired token'}), 401
        
        if payload.get('role') != 'seller':
            return jsonify({'success': False, 'message': 'Seller access required'}), 403
        
        request.user_id = payload['user_id']
        request.user_email = payload['email']
        request.user_role = payload['role']
        
        return f(*args, **kwargs)
    
    return decorated
