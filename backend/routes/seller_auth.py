from flask import Blueprint, request, jsonify
from database import get_db
from auth import AuthManager, token_required
from bson.objectid import ObjectId
from datetime import datetime
import re

seller_auth_bp = Blueprint('seller_auth', __name__, url_prefix='/api/seller/auth')

# ============================================================================
# SELLER REGISTRATION
# ============================================================================

@seller_auth_bp.route('/register', methods=['POST'])
def register_seller():
    """Register new seller/canteen owner"""
    try:
        data = request.get_json()
        
        # Validate input
        required_fields = ['name', 'email', 'password', 'phone', 'college_id', 'cafeteria_name']
        if not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'message': 'Missing required fields: ' + ', '.join(required_fields)
            }), 400
        
        # Validate email format
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, data['email']):
            return jsonify({
                'success': False,
                'message': 'Invalid email format'
            }), 400
        
        # Validate password strength
        if len(data['password']) < 6:
            return jsonify({
                'success': False,
                'message': 'Password must be at least 6 characters long'
            }), 400
        
        db = get_db()
        sellers_collection = db['sellers']
        colleges_collection = db['colleges']
        
        # Check if seller email already exists
        if sellers_collection.find_one({'email': data['email']}):
            return jsonify({
                'success': False,
                'message': 'Seller with this email already exists'
            }), 409
        
        # Verify college exists
        try:
            college_id = ObjectId(data['college_id'])
            college = colleges_collection.find_one({'_id': college_id})
            if not college:
                return jsonify({
                    'success': False,
                    'message': 'College not found'
                }), 404
        except:
            return jsonify({
                'success': False,
                'message': 'Invalid college ID format'
            }), 400
        
        # Hash password
        hashed_password = AuthManager.hash_password(data['password'])
        
        # Create seller document
        seller_doc = {
            'name': data['name'].strip(),
            'email': data['email'].lower().strip(),
            'password': hashed_password,
            'phone': data['phone'].strip(),
            'college_id': college_id,
            'cafeteria_name': data['cafeteria_name'].strip(),
            'cafeteria_location': data.get('cafeteria_location', ''),
            'description': data.get('description', ''),
            'role': 'seller',
            'status': 'active',  # active, inactive, suspended
            'verified': False,
            'rating': 0,
            'total_orders': 0,
            'total_revenue': 0,
            'opening_time': data.get('opening_time', '08:00'),
            'closing_time': data.get('closing_time', '18:00'),
            'supported_payment_methods': ['offline'],  # offline, online (razorpay, upi)
            'bank_account': {
                'account_holder': data.get('account_holder', ''),
                'account_number': data.get('account_number', ''),
                'ifsc_code': data.get('ifsc_code', '')
            },
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = sellers_collection.insert_one(seller_doc)
        seller_id = result.inserted_id
        
        # Generate token
        token = AuthManager.generate_token(seller_id, data['email'], 'seller')
        
        return jsonify({
            'success': True,
            'message': 'Seller registered successfully',
            'seller': {
                'id': str(seller_id),
                'name': data['name'],
                'email': data['email'],
                'cafeteria_name': data['cafeteria_name'],
                'college_id': data['college_id'],
                'phone': data['phone'],
                'role': 'seller'
            },
            'token': token
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Registration error: {str(e)}'
        }), 500


# ============================================================================
# SELLER LOGIN
# ============================================================================

@seller_auth_bp.route('/login', methods=['POST'])
def login_seller():
    """Login seller"""
    try:
        data = request.get_json()
        
        if not data.get('email') or not data.get('password'):
            return jsonify({
                'success': False,
                'message': 'Email and password are required'
            }), 400
        
        db = get_db()
        sellers_collection = db['sellers']
        
        # Find seller by email
        seller = sellers_collection.find_one({'email': data['email'].lower().strip()})
        
        if not seller:
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            }), 401
        
        # Check if seller account is active
        if seller.get('status') != 'active':
            return jsonify({
                'success': False,
                'message': f'Account is {seller.get("status")}. Please contact admin.'
            }), 403
        
        # Verify password
        if not AuthManager.verify_password(data['password'], seller['password']):
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            }), 401
        
        # Generate token
        token = AuthManager.generate_token(seller['_id'], seller['email'], 'seller')
        
        # Get college name
        colleges_collection = db['colleges']
        college = colleges_collection.find_one({'_id': seller['college_id']})
        college_name = college['name'] if college else 'Unknown'
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'seller': {
                'id': str(seller['_id']),
                'name': seller['name'],
                'email': seller['email'],
                'cafeteria_name': seller['cafeteria_name'],
                'college_id': str(seller['college_id']),
                'college_name': college_name,
                'phone': seller['phone'],
                'role': 'seller',
                'verified': seller.get('verified', False),
                'rating': seller.get('rating', 0),
                'total_orders': seller.get('total_orders', 0),
                'total_revenue': seller.get('total_revenue', 0)
            },
            'token': token
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Login error: {str(e)}'
        }), 500


# ============================================================================
# SELLER PROFILE
# ============================================================================

@seller_auth_bp.route('/profile', methods=['GET'])
@token_required
def get_seller_profile():
    """Get seller profile"""
    try:
        # Check if user is seller
        if request.user_role != 'seller':
            return jsonify({
                'success': False,
                'message': 'Only sellers can access this endpoint'
            }), 403
        
        db = get_db()
        sellers_collection = db['sellers']
        colleges_collection = db['colleges']
        
        # Get seller
        seller = sellers_collection.find_one({'_id': ObjectId(request.user_id)})
        
        if not seller:
            return jsonify({
                'success': False,
                'message': 'Seller not found'
            }), 404
        
        # Get college info
        college = colleges_collection.find_one({'_id': seller['college_id']})
        college_name = college['name'] if college else 'Unknown'
        
        return jsonify({
            'success': True,
            'seller': {
                'id': str(seller['_id']),
                'name': seller['name'],
                'email': seller['email'],
                'phone': seller['phone'],
                'cafeteria_name': seller['cafeteria_name'],
                'cafeteria_location': seller.get('cafeteria_location', ''),
                'description': seller.get('description', ''),
                'college_id': str(seller['college_id']),
                'college_name': college_name,
                'verified': seller.get('verified', False),
                'rating': seller.get('rating', 0),
                'total_orders': seller.get('total_orders', 0),
                'total_revenue': seller.get('total_revenue', 0),
                'status': seller.get('status', 'active'),
                'opening_time': seller.get('opening_time', '08:00'),
                'closing_time': seller.get('closing_time', '18:00'),
                'supported_payment_methods': seller.get('supported_payment_methods', ['offline']),
                'created_at': seller.get('created_at').isoformat() if seller.get('created_at') else None
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching profile: {str(e)}'
        }), 500


# ============================================================================
# UPDATE SELLER PROFILE
# ============================================================================

@seller_auth_bp.route('/profile', methods=['PUT'])
@token_required
def update_seller_profile():
    """Update seller profile"""
    try:
        # Check if user is seller
        if request.user_role != 'seller':
            return jsonify({
                'success': False,
                'message': 'Only sellers can access this endpoint'
            }), 403
        
        data = request.get_json()
        db = get_db()
        sellers_collection = db['sellers']
        
        # Fields that can be updated
        allowed_fields = ['phone', 'cafeteria_location', 'description', 'opening_time', 
                         'closing_time', 'supported_payment_methods']
        
        update_data = {}
        for field in allowed_fields:
            if field in data:
                update_data[field] = data[field]
        
        # Update bank account info if provided
        if 'bank_account' in data:
            update_data['bank_account'] = data['bank_account']
        
        update_data['updated_at'] = datetime.utcnow()
        
        result = sellers_collection.update_one(
            {'_id': ObjectId(request.user_id)},
            {'$set': update_data}
        )
        
        if result.matched_count == 0:
            return jsonify({
                'success': False,
                'message': 'Seller not found'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Update error: {str(e)}'
        }), 500


# ============================================================================
# CHANGE PASSWORD
# ============================================================================

@seller_auth_bp.route('/change-password', methods=['POST'])
@token_required
def change_password():
    """Change seller password"""
    try:
        # Check if user is seller
        if request.user_role != 'seller':
            return jsonify({
                'success': False,
                'message': 'Only sellers can access this endpoint'
            }), 403
        
        data = request.get_json()
        
        if not data.get('old_password') or not data.get('new_password'):
            return jsonify({
                'success': False,
                'message': 'Old password and new password are required'
            }), 400
        
        if len(data['new_password']) < 6:
            return jsonify({
                'success': False,
                'message': 'New password must be at least 6 characters long'
            }), 400
        
        db = get_db()
        sellers_collection = db['sellers']
        
        # Get seller
        seller = sellers_collection.find_one({'_id': ObjectId(request.user_id)})
        
        if not seller:
            return jsonify({
                'success': False,
                'message': 'Seller not found'
            }), 404
        
        # Verify old password
        if not AuthManager.verify_password(data['old_password'], seller['password']):
            return jsonify({
                'success': False,
                'message': 'Old password is incorrect'
            }), 401
        
        # Hash new password
        hashed_password = AuthManager.hash_password(data['new_password'])
        
        # Update password
        sellers_collection.update_one(
            {'_id': ObjectId(request.user_id)},
            {'$set': {'password': hashed_password, 'updated_at': datetime.utcnow()}}
        )
        
        return jsonify({
            'success': True,
            'message': 'Password changed successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500
