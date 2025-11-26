from flask import Blueprint, request, jsonify
from database import get_db
from auth import AuthManager, token_required
from bson.objectid import ObjectId
from datetime import datetime

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register new user"""
    try:
        data = request.get_json()
        
        # Validate input
        required_fields = ['name', 'email', 'password', 'phone', 'college']
        if not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'message': 'Missing required fields'
            }), 400
        
        db = get_db()
        users_collection = db['users']
        
        # Check if user exists
        if users_collection.find_one({'email': data['email']}):
            return jsonify({
                'success': False,
                'message': 'User already exists'
            }), 409
        
        # Hash password
        hashed_password = AuthManager.hash_password(data['password'])
        
        # Create user
        user_doc = {
            'name': data['name'],
            'email': data['email'],
            'password': hashed_password,
            'phone': data['phone'],
            'college': data['college'],
            'role': 'user',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = users_collection.insert_one(user_doc)
        user_id = result.inserted_id
        
        # Generate token
        token = AuthManager.generate_token(user_id, data['email'], 'user')
        
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'user': {
                'id': str(user_id),
                'name': data['name'],
                'email': data['email'],
                'college': data['college'],
                'phone': data['phone']
            },
            'token': token
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Registration error: {str(e)}'
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({
                'success': False,
                'message': 'Email and password required'
            }), 400
        
        db = get_db()
        users_collection = db['users']
        
        # Find user
        user = users_collection.find_one({'email': data['email']})
        if not user:
            return jsonify({
                'success': False,
                'message': 'Invalid credentials'
            }), 401
        
        # Verify password
        if not AuthManager.verify_password(data['password'], user['password']):
            return jsonify({
                'success': False,
                'message': 'Invalid credentials'
            }), 401
        
        # Generate token
        token = AuthManager.generate_token(user['_id'], user['email'], user.get('role', 'user'))
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': {
                'id': str(user['_id']),
                'name': user['name'],
                'email': user['email'],
                'college': user['college'],
                'phone': user['phone']
            },
            'token': token
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Login error: {str(e)}'
        }), 500

@auth_bp.route('/verify', methods=['POST'])
@token_required
def verify_token():
    """Verify token"""
    return jsonify({
        'success': True,
        'message': 'Token is valid',
        'user_id': request.user_id,
        'email': request.user_email
    }), 200

@auth_bp.route('/profile', methods=['GET'])
@token_required
def get_profile():
    """Get user profile"""
    try:
        db = get_db()
        users_collection = db['users']
        
        user = users_collection.find_one({'_id': ObjectId(request.user_id)})
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        return jsonify({
            'success': True,
            'user': {
                'id': str(user['_id']),
                'name': user['name'],
                'email': user['email'],
                'phone': user['phone'],
                'college': user['college'],
                'created_at': user.get('created_at', '').isoformat() if isinstance(user.get('created_at'), datetime) else user.get('created_at')
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching profile: {str(e)}'
        }), 500

@auth_bp.route('/update-profile', methods=['PUT'])
@token_required
def update_profile():
    """Update user profile"""
    try:
        data = request.get_json()
        db = get_db()
        users_collection = db['users']
        
        # Update allowed fields
        update_fields = {}
        if 'name' in data:
            update_fields['name'] = data['name']
        if 'phone' in data:
            update_fields['phone'] = data['phone']
        
        update_fields['updated_at'] = datetime.utcnow()
        
        result = users_collection.update_one(
            {'_id': ObjectId(request.user_id)},
            {'$set': update_fields}
        )
        
        if result.matched_count == 0:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error updating profile: {str(e)}'
        }), 500
