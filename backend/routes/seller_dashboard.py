from flask import Blueprint, request, jsonify
from database import get_db
from auth import token_required
from bson.objectid import ObjectId
from datetime import datetime, timedelta

seller_dashboard_bp = Blueprint('seller_dashboard', __name__, url_prefix='/api/seller/dashboard')

# ============================================================================
# SELLER ORDERS - GET ALL ORDERS
# ============================================================================

@seller_dashboard_bp.route('/orders', methods=['GET'])
@token_required
def get_seller_orders():
    """Get all orders for a seller's cafeteria"""
    try:
        # Check if user is seller
        if request.user_role != 'seller':
            return jsonify({
                'success': False,
                'message': 'Only sellers can access this endpoint'
            }), 403
        
        db = get_db()
        sellers_collection = db['sellers']
        orders_collection = db['orders']
        
        # Get seller info
        seller = sellers_collection.find_one({'_id': ObjectId(request.user_id)})
        if not seller:
            return jsonify({
                'success': False,
                'message': 'Seller not found'
            }), 404
        
        # Get query parameters
        status = request.args.get('status', None)  # pending, confirmed, preparing, ready, completed, cancelled
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))
        sort_by = request.args.get('sort_by', 'created_at')  # created_at, pickup_time, total_price
        sort_order = int(request.args.get('sort_order', -1))  # -1 for descending, 1 for ascending
        
        # Build query
        query = {
            'cafeteria_id': seller['college_id']  # All orders for this cafeteria
        }
        
        if status:
            query['status'] = status
        
        # Get total count
        total = orders_collection.count_documents(query)
        
        # Get orders
        orders_cursor = orders_collection.find(query).sort(sort_by, sort_order).skip(offset).limit(limit)
        orders = []
        
        for order in orders_cursor:
            orders.append({
                'id': str(order['_id']),
                'user_email': order.get('user_email', 'Unknown'),
                'user_id': str(order.get('user_id', '')),
                'customer_name': order.get('customer_name', 'Unknown'),
                'items': order.get('items', []),
                'total_price': order.get('total_price', 0),
                'order_token': order.get('order_token', ''),
                'pickup_time': order.get('pickup_time', ''),
                'special_instructions': order.get('special_instructions', ''),
                'status': order.get('status', 'pending'),
                'payment_status': order.get('payment_status', 'pending'),
                'payment_method': order.get('payment_method', 'offline'),
                'qr_code': order.get('qr_code', ''),
                'created_at': order.get('created_at').isoformat() if order.get('created_at') else None,
                'updated_at': order.get('updated_at').isoformat() if order.get('updated_at') else None
            })
        
        return jsonify({
            'success': True,
            'orders': orders,
            'pagination': {
                'total': total,
                'limit': limit,
                'offset': offset,
                'count': len(orders)
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching orders: {str(e)}'
        }), 500


# ============================================================================
# GET ORDER DETAILS
# ============================================================================

@seller_dashboard_bp.route('/orders/<order_id>', methods=['GET'])
@token_required
def get_order_details(order_id):
    """Get detailed information about a specific order"""
    try:
        if request.user_role != 'seller':
            return jsonify({
                'success': False,
                'message': 'Only sellers can access this endpoint'
            }), 403
        
        db = get_db()
        sellers_collection = db['sellers']
        orders_collection = db['orders']
        users_collection = db['users']
        
        # Get seller
        seller = sellers_collection.find_one({'_id': ObjectId(request.user_id)})
        if not seller:
            return jsonify({
                'success': False,
                'message': 'Seller not found'
            }), 404
        
        # Get order
        try:
            order = orders_collection.find_one({'_id': ObjectId(order_id)})
        except:
            return jsonify({
                'success': False,
                'message': 'Invalid order ID'
            }), 400
        
        if not order:
            return jsonify({
                'success': False,
                'message': 'Order not found'
            }), 404
        
        # Verify order belongs to this seller's cafeteria
        if order.get('cafeteria_id') != seller['college_id']:
            return jsonify({
                'success': False,
                'message': 'Unauthorized: This order does not belong to your cafeteria'
            }), 403
        
        # Get customer info
        customer = None
        if order.get('user_id'):
            customer = users_collection.find_one({'_id': ObjectId(order['user_id'])})
        
        return jsonify({
            'success': True,
            'order': {
                'id': str(order['_id']),
                'customer': {
                    'id': str(order.get('user_id', '')),
                    'email': order.get('user_email', ''),
                    'name': customer['name'] if customer else 'Unknown',
                    'phone': customer.get('phone', '') if customer else ''
                },
                'items': order.get('items', []),
                'total_price': order.get('total_price', 0),
                'order_token': order.get('order_token', ''),
                'pickup_time': order.get('pickup_time', ''),
                'special_instructions': order.get('special_instructions', ''),
                'status': order.get('status', 'pending'),
                'payment_status': order.get('payment_status', 'pending'),
                'payment_method': order.get('payment_method', 'offline'),
                'qr_code': order.get('qr_code', ''),
                'created_at': order.get('created_at').isoformat() if order.get('created_at') else None,
                'updated_at': order.get('updated_at').isoformat() if order.get('updated_at') else None
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching order: {str(e)}'
        }), 500


# ============================================================================
# UPDATE ORDER STATUS
# ============================================================================

@seller_dashboard_bp.route('/orders/<order_id>/status', methods=['PUT'])
@token_required
def update_order_status(order_id):
    """Update order status (pending -> confirmed -> preparing -> ready -> completed)"""
    try:
        if request.user_role != 'seller':
            return jsonify({
                'success': False,
                'message': 'Only sellers can access this endpoint'
            }), 403
        
        data = request.get_json()
        new_status = data.get('status')
        
        valid_statuses = ['pending', 'confirmed', 'preparing', 'ready', 'completed', 'cancelled']
        if new_status not in valid_statuses:
            return jsonify({
                'success': False,
                'message': f'Invalid status. Valid statuses: {", ".join(valid_statuses)}'
            }), 400
        
        db = get_db()
        sellers_collection = db['sellers']
        orders_collection = db['orders']
        
        # Get seller
        seller = sellers_collection.find_one({'_id': ObjectId(request.user_id)})
        if not seller:
            return jsonify({
                'success': False,
                'message': 'Seller not found'
            }), 404
        
        # Get order
        try:
            order = orders_collection.find_one({'_id': ObjectId(order_id)})
        except:
            return jsonify({
                'success': False,
                'message': 'Invalid order ID'
            }), 400
        
        if not order:
            return jsonify({
                'success': False,
                'message': 'Order not found'
            }), 404
        
        # Verify order belongs to this seller
        if order.get('cafeteria_id') != seller['college_id']:
            return jsonify({
                'success': False,
                'message': 'Unauthorized'
            }), 403
        
        # Update status
        orders_collection.update_one(
            {'_id': ObjectId(order_id)},
            {
                '$set': {
                    'status': new_status,
                    'updated_at': datetime.utcnow()
                }
            }
        )
        
        # If marking as ready, add ready_at timestamp
        if new_status == 'ready':
            orders_collection.update_one(
                {'_id': ObjectId(order_id)},
                {'$set': {'ready_at': datetime.utcnow()}}
            )
        
        return jsonify({
            'success': True,
            'message': f'Order status updated to {new_status}',
            'order_id': order_id,
            'new_status': new_status
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error updating order: {str(e)}'
        }), 500


# ============================================================================
# VERIFY CUSTOMER PICKUP (QR CODE OR TOKEN)
# ============================================================================

@seller_dashboard_bp.route('/orders/<order_id>/verify-pickup', methods=['POST'])
@token_required
def verify_customer_pickup(order_id):
    """
    Verify customer identity before giving order.
    Accept either QR code scan OR token number.
    """
    try:
        if request.user_role != 'seller':
            return jsonify({
                'success': False,
                'message': 'Only sellers can access this endpoint'
            }), 403
        
        data = request.get_json()
        verification_method = data.get('method')  # 'token' or 'qr'
        verification_value = data.get('value')
        
        if not verification_method or not verification_value:
            return jsonify({
                'success': False,
                'message': 'Verification method and value are required'
            }), 400
        
        db = get_db()
        sellers_collection = db['sellers']
        orders_collection = db['orders']
        
        # Get seller
        seller = sellers_collection.find_one({'_id': ObjectId(request.user_id)})
        if not seller:
            return jsonify({
                'success': False,
                'message': 'Seller not found'
            }), 404
        
        # Get order
        try:
            order = orders_collection.find_one({'_id': ObjectId(order_id)})
        except:
            return jsonify({
                'success': False,
                'message': 'Invalid order ID'
            }), 400
        
        if not order:
            return jsonify({
                'success': False,
                'message': 'Order not found'
            }), 404
        
        # Verify order belongs to this seller
        if order.get('cafeteria_id') != seller['college_id']:
            return jsonify({
                'success': False,
                'message': 'Unauthorized'
            }), 403
        
        # Verify order is ready
        if order.get('status') != 'ready':
            return jsonify({
                'success': False,
                'message': f'Order status is {order.get("status")}. It must be ready for pickup.'
            }), 400
        
        # Verify using selected method
        verified = False
        if verification_method == 'token':
            verified = order.get('order_token') == verification_value
        elif verification_method == 'qr':
            # QR code contains order ID, so we verify it matches
            verified = str(order['_id']) in verification_value
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid verification method'
            }), 400
        
        if not verified:
            return jsonify({
                'success': False,
                'message': 'Verification failed. Invalid token or QR code.'
            }), 401
        
        # Mark order as completed
        orders_collection.update_one(
            {'_id': ObjectId(order_id)},
            {
                '$set': {
                    'status': 'completed',
                    'completed_at': datetime.utcnow(),
                    'pickup_verified_by': request.user_id,
                    'pickup_verification_method': verification_method,
                    'updated_at': datetime.utcnow()
                }
            }
        )
        
        # Update seller statistics
        sellers_collection.update_one(
            {'_id': ObjectId(request.user_id)},
            {
                '$inc': {
                    'total_orders': 1,
                    'total_revenue': order.get('total_price', 0)
                }
            }
        )
        
        return jsonify({
            'success': True,
            'message': 'Customer verified successfully. Order marked as completed.',
            'order_id': order_id,
            'customer_name': data.get('customer_name', 'Customer'),
            'amount': order.get('total_price', 0)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error verifying pickup: {str(e)}'
        }), 500


# ============================================================================
# GET SELLER DASHBOARD STATISTICS
# ============================================================================

@seller_dashboard_bp.route('/statistics', methods=['GET'])
@token_required
def get_dashboard_statistics():
    """Get seller dashboard statistics"""
    try:
        if request.user_role != 'seller':
            return jsonify({
                'success': False,
                'message': 'Only sellers can access this endpoint'
            }), 403
        
        db = get_db()
        sellers_collection = db['sellers']
        orders_collection = db['orders']
        
        # Get seller
        seller = sellers_collection.find_one({'_id': ObjectId(request.user_id)})
        if not seller:
            return jsonify({
                'success': False,
                'message': 'Seller not found'
            }), 404
        
        # Get statistics
        cafeteria_id = seller['college_id']
        
        # Count orders by status
        total_orders = orders_collection.count_documents({'cafeteria_id': cafeteria_id})
        pending_orders = orders_collection.count_documents({'cafeteria_id': cafeteria_id, 'status': 'pending'})
        confirmed_orders = orders_collection.count_documents({'cafeteria_id': cafeteria_id, 'status': 'confirmed'})
        preparing_orders = orders_collection.count_documents({'cafeteria_id': cafeteria_id, 'status': 'preparing'})
        ready_orders = orders_collection.count_documents({'cafeteria_id': cafeteria_id, 'status': 'ready'})
        completed_orders = orders_collection.count_documents({'cafeteria_id': cafeteria_id, 'status': 'completed'})
        
        # Calculate total revenue (from completed orders)
        revenue_pipeline = [
            {'$match': {'cafeteria_id': cafeteria_id, 'status': 'completed'}},
            {'$group': {'_id': None, 'total': {'$sum': '$total_price'}}}
        ]
        revenue_result = list(orders_collection.aggregate(revenue_pipeline))
        total_revenue = revenue_result[0]['total'] if revenue_result else 0
        
        # Revenue by payment method
        payment_method_pipeline = [
            {'$match': {'cafeteria_id': cafeteria_id, 'status': 'completed'}},
            {'$group': {
                '_id': '$payment_method',
                'total': {'$sum': '$total_price'},
                'count': {'$sum': 1}
            }}
        ]
        payment_methods = list(orders_collection.aggregate(payment_method_pipeline))
        
        # Today's revenue
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_revenue_pipeline = [
            {'$match': {
                'cafeteria_id': cafeteria_id,
                'status': 'completed',
                'created_at': {'$gte': today_start}
            }},
            {'$group': {'_id': None, 'total': {'$sum': '$total_price'}}}
        ]
        today_revenue_result = list(orders_collection.aggregate(today_revenue_pipeline))
        today_revenue = today_revenue_result[0]['total'] if today_revenue_result else 0
        
        return jsonify({
            'success': True,
            'statistics': {
                'orders': {
                    'total': total_orders,
                    'pending': pending_orders,
                    'confirmed': confirmed_orders,
                    'preparing': preparing_orders,
                    'ready': ready_orders,
                    'completed': completed_orders
                },
                'revenue': {
                    'total': total_revenue,
                    'today': today_revenue,
                    'by_payment_method': [
                        {
                            'method': method['_id'],
                            'total': method['total'],
                            'count': method['count']
                        } for method in payment_methods
                    ]
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching statistics: {str(e)}'
        }), 500
