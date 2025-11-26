from flask import Blueprint, request, jsonify
from database import get_db
from auth import token_required
from bson.objectid import ObjectId
from datetime import datetime

menu_bp = Blueprint('menu', __name__, url_prefix='/api/menu')

@menu_bp.route('/', methods=['GET'])
def get_menu():
    """Get all menu items with optional filtering"""
    try:
        db = get_db()
        menu_collection = db['menu_items']
        
        # Get query parameters for filtering
        cafeteria_id = request.args.get('cafeteria_id')
        category = request.args.get('category')
        college_id = request.args.get('college_id')
        veg_only = request.args.get('veg_only', '').lower() == 'true'
        
        # Build filter
        filter_dict = {}
        if cafeteria_id:
            filter_dict['cafeteria_id'] = cafeteria_id
        if category:
            filter_dict['category'] = category
        if college_id:
            filter_dict['college_id'] = college_id
        if veg_only:
            filter_dict['is_veg'] = True
        
        items = list(menu_collection.find(filter_dict))
        
        result = []
        for item in items:
            result.append({
                'id': str(item['_id']),
                'name': item['name'],
                'description': item.get('description', ''),
                'price': item['price'],
                'category': item.get('category', ''),
                'is_veg': item.get('is_veg', False),
                'image': item.get('image', ''),
                'available': item.get('available', True),
                'cafeteria_id': item.get('cafeteria_id', '')
            })
        
        return jsonify({
            'success': True,
            'count': len(result),
            'items': result
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching menu: {str(e)}'
        }), 500

@menu_bp.route('/<item_id>', methods=['GET'])
def get_menu_item(item_id):
    """Get menu item by ID"""
    try:
        db = get_db()
        menu_collection = db['menu_items']
        
        item = menu_collection.find_one({'_id': ObjectId(item_id)})
        if not item:
            return jsonify({
                'success': False,
                'message': 'Menu item not found'
            }), 404
        
        return jsonify({
            'success': True,
            'item': {
                'id': str(item['_id']),
                'name': item['name'],
                'description': item.get('description', ''),
                'price': item['price'],
                'category': item.get('category', ''),
                'is_veg': item.get('is_veg', False),
                'image': item.get('image', ''),
                'available': item.get('available', True),
                'cafeteria_id': item.get('cafeteria_id', '')
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching menu item: {str(e)}'
        }), 500

@menu_bp.route('/', methods=['POST'])
@token_required
def create_menu_item():
    """Create new menu item (Seller only)"""
    try:
        if request.user_role not in ['seller', 'admin']:
            return jsonify({
                'success': False,
                'message': 'Seller access required'
            }), 403
        
        data = request.get_json()
        required_fields = ['name', 'price', 'cafeteria_id']
        
        if not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'message': 'Missing required fields'
            }), 400
        
        db = get_db()
        menu_collection = db['menu_items']
        
        menu_doc = {
            'name': data['name'],
            'description': data.get('description', ''),
            'price': float(data['price']),
            'category': data.get('category', ''),
            'is_veg': data.get('is_veg', False),
            'image': data.get('image', ''),
            'available': data.get('available', True),
            'cafeteria_id': data['cafeteria_id'],
            'college_id': data.get('college_id', ''),
            'seller_id': request.user_id,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = menu_collection.insert_one(menu_doc)
        
        return jsonify({
            'success': True,
            'message': 'Menu item created successfully',
            'item_id': str(result.inserted_id)
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error creating menu item: {str(e)}'
        }), 500

@menu_bp.route('/<item_id>', methods=['PUT'])
@token_required
def update_menu_item(item_id):
    """Update menu item (Seller only)"""
    try:
        if request.user_role not in ['seller', 'admin']:
            return jsonify({
                'success': False,
                'message': 'Seller access required'
            }), 403
        
        db = get_db()
        menu_collection = db['menu_items']
        
        item = menu_collection.find_one({'_id': ObjectId(item_id)})
        if not item:
            return jsonify({
                'success': False,
                'message': 'Menu item not found'
            }), 404
        
        if item['seller_id'] != request.user_id and request.user_role != 'admin':
            return jsonify({
                'success': False,
                'message': 'Not authorized to update this item'
            }), 403
        
        data = request.get_json()
        update_fields = {}
        
        if 'price' in data:
            update_fields['price'] = float(data['price'])
        if 'available' in data:
            update_fields['available'] = data['available']
        if 'description' in data:
            update_fields['description'] = data['description']
        
        update_fields['updated_at'] = datetime.utcnow()
        
        menu_collection.update_one(
            {'_id': ObjectId(item_id)},
            {'$set': update_fields}
        )
        
        return jsonify({
            'success': True,
            'message': 'Menu item updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error updating menu item: {str(e)}'
        }), 500
