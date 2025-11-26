from flask import Blueprint, request, jsonify
from database import get_db
from auth import token_required, seller_required
from bson.objectid import ObjectId
from datetime import datetime
from utils import QRCodeGenerator, TokenGenerator, TimeScheduler
import json

order_bp = Blueprint('order', __name__, url_prefix='/api/orders')

@order_bp.route('/create', methods=['POST'])
@token_required
def create_order():
    """Create new order"""
    try:
        data = request.get_json()
        
        required_fields = ['items', 'college_id', 'cafeteria_id', 'pickup_time']
        if not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'message': 'Missing required fields'
            }), 400
        
        # Validate payment method
        payment_method = data.get('payment_method', 'offline')  # offline, online (razorpay, upi, card)
        valid_payment_methods = ['offline', 'online', 'razorpay', 'upi', 'card']
        if payment_method not in valid_payment_methods:
            return jsonify({
                'success': False,
                'message': f'Invalid payment method. Valid methods: {", ".join(valid_payment_methods)}'
            }), 400
        
        # Validate pickup time
        if not TimeScheduler.validate_slot(data['pickup_time']):
            return jsonify({
                'success': False,
                'message': f'Invalid pickup time. Available slots: {", ".join(TimeScheduler.get_available_slots())}'
            }), 400
        
        db = get_db()
        orders_collection = db['orders']
        menu_collection = db['menu_items']
        
        # Calculate total price
        total_price = 0
        order_items = []
        
        for item_data in data['items']:
            item = menu_collection.find_one({'_id': ObjectId(item_data['item_id'])})
            if not item:
                return jsonify({
                    'success': False,
                    'message': f'Item {item_data["item_id"]} not found'
                }), 404
            
            if not item.get('available'):
                return jsonify({
                    'success': False,
                    'message': f'Item {item["name"]} is not available'
                }), 400
            
            quantity = item_data.get('quantity', 1)
            item_total = item['price'] * quantity
            total_price += item_total
            
            order_items.append({
                'item_id': str(item['_id']),
                'name': item['name'],
                'price': item['price'],
                'quantity': quantity,
                'subtotal': item_total
            })
        
        # Generate order token and ID
        order_token = TokenGenerator.generate_order_token()
        
        order_doc = {
            'user_id': ObjectId(request.user_id),
            'user_email': request.user_email,
            'college_id': data['college_id'],
            'cafeteria_id': data['cafeteria_id'],
            'items': order_items,
            'total_price': total_price,
            'order_token': order_token,
            'pickup_time': data['pickup_time'],
            'special_instructions': data.get('special_instructions', ''),
            'status': 'pending',  # pending, confirmed, preparing, ready, completed, cancelled
            'payment_status': 'pending',  # pending, completed, failed
            'payment_method': payment_method,  # offline, online, razorpay, upi, card
            'qr_code': None,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = orders_collection.insert_one(order_doc)
        order_id = result.inserted_id
        
        # Generate QR code
        qr_result = QRCodeGenerator.generate_qr(str(order_id), order_token)
        
        # Update order with QR code
        if qr_result['success']:
            orders_collection.update_one(
                {'_id': order_id},
                {'$set': {'qr_code': qr_result['qr_code']}}
            )
        
        return jsonify({
            'success': True,
            'message': 'Order created successfully',
            'order': {
                'id': str(order_id),
                'token': order_token,
                'total_price': total_price,
                'items': order_items,
                'pickup_time': data['pickup_time'],
                'payment_method': payment_method,
                'status': 'pending',
                'qr_code': qr_result.get('qr_code') if qr_result['success'] else None,
                'created_at': order_doc['created_at'].isoformat()
            }
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error creating order: {str(e)}'
        }), 500

@order_bp.route('/<order_id>', methods=['GET'])
@token_required
def get_order(order_id):
    """Get order details"""
    try:
        db = get_db()
        orders_collection = db['orders']
        
        order = orders_collection.find_one({'_id': ObjectId(order_id)})
        if not order:
            return jsonify({
                'success': False,
                'message': 'Order not found'
            }), 404
        
        # Verify user is owner or seller
        if order['user_id'] != ObjectId(request.user_id) and request.user_role not in ['seller', 'admin']:
            return jsonify({
                'success': False,
                'message': 'Not authorized to view this order'
            }), 403
        
        return jsonify({
            'success': True,
            'order': {
                'id': str(order['_id']),
                'user_email': order['user_email'],
                'items': order['items'],
                'total_price': order['total_price'],
                'token': order['order_token'],
                'pickup_time': order['pickup_time'],
                'status': order['status'],
                'payment_status': order['payment_status'],
                'special_instructions': order.get('special_instructions', ''),
                'qr_code': order.get('qr_code'),
                'created_at': order['created_at'].isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching order: {str(e)}'
        }), 500

@order_bp.route('/user/orders', methods=['GET'])
@token_required
def get_user_orders():
    """Get all orders for current user"""
    try:
        db = get_db()
        orders_collection = db['orders']
        
        orders = list(orders_collection.find({'user_id': ObjectId(request.user_id)}).sort('created_at', -1))
        
        result = []
        for order in orders:
            result.append({
                'id': str(order['_id']),
                'items': order['items'],
                'total_price': order['total_price'],
                'token': order['order_token'],
                'pickup_time': order['pickup_time'],
                'status': order['status'],
                'payment_status': order['payment_status'],
                'created_at': order['created_at'].isoformat()
            })
        
        return jsonify({
            'success': True,
            'count': len(result),
            'orders': result
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching orders: {str(e)}'
        }), 500

@order_bp.route('/<order_id>/verify-qr', methods=['POST'])
@seller_required
def verify_qr(order_id):
    """Verify QR code and order (Seller endpoint)"""
    try:
        db = get_db()
        orders_collection = db['orders']
        
        order = orders_collection.find_one({'_id': ObjectId(order_id)})
        if not order:
            return jsonify({
                'success': False,
                'message': 'Order not found'
            }), 404
        
        # Verify order is for seller's cafeteria
        if order['cafeteria_id'] != request.args.get('cafeteria_id'):
            return jsonify({
                'success': False,
                'message': 'Order not for this cafeteria'
            }), 403
        
        # Mark order as ready for pickup
        orders_collection.update_one(
            {'_id': ObjectId(order_id)},
            {'$set': {
                'status': 'ready',
                'updated_at': datetime.utcnow()
            }}
        )
        
        return jsonify({
            'success': True,
            'message': 'Order verified successfully',
            'order': {
                'id': str(order['_id']),
                'token': order['order_token'],
                'items': order['items'],
                'total_price': order['total_price'],
                'status': 'ready',
                'user_email': order['user_email']
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error verifying QR: {str(e)}'
        }), 500

@order_bp.route('/<order_id>/verify-token', methods=['POST'])
@seller_required
def verify_token(order_id):
    """Verify token and order (Seller endpoint)"""
    try:
        data = request.get_json()
        token = data.get('token')
        
        if not token:
            return jsonify({
                'success': False,
                'message': 'Token required'
            }), 400
        
        db = get_db()
        orders_collection = db['orders']
        
        order = orders_collection.find_one({'_id': ObjectId(order_id)})
        if not order:
            return jsonify({
                'success': False,
                'message': 'Order not found'
            }), 404
        
        # Verify token matches
        if order['order_token'] != token:
            return jsonify({
                'success': False,
                'message': 'Invalid token'
            }), 401
        
        # Mark order as ready
        orders_collection.update_one(
            {'_id': ObjectId(order_id)},
            {'$set': {
                'status': 'ready',
                'updated_at': datetime.utcnow()
            }}
        )
        
        return jsonify({
            'success': True,
            'message': 'Token verified successfully',
            'order': {
                'id': str(order['_id']),
                'items': order['items'],
                'total_price': order['total_price'],
                'status': 'ready'
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error verifying token: {str(e)}'
        }), 500

@order_bp.route('/<order_id>/status', methods=['PUT'])
@seller_required
def update_order_status(order_id):
    """Update order status (Seller only)"""
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        valid_statuses = ['pending', 'confirmed', 'preparing', 'ready', 'completed', 'cancelled']
        if new_status not in valid_statuses:
            return jsonify({
                'success': False,
                'message': f'Invalid status. Valid statuses: {", ".join(valid_statuses)}'
            }), 400
        
        db = get_db()
        orders_collection = db['orders']
        
        orders_collection.update_one(
            {'_id': ObjectId(order_id)},
            {'$set': {
                'status': new_status,
                'updated_at': datetime.utcnow()
            }}
        )
        
        return jsonify({
            'success': True,
            'message': f'Order status updated to {new_status}'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error updating order: {str(e)}'
        }), 500

@order_bp.route('/available-slots', methods=['GET'])
def get_pickup_slots():
    """Get available pickup time slots"""
    return jsonify({
        'success': True,
        'slots': TimeScheduler.get_available_slots()
    }), 200
