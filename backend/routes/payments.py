from flask import Blueprint, request, jsonify
from database import get_db
from auth import token_required
from bson.objectid import ObjectId
from datetime import datetime
import os
import requests
from dotenv import load_dotenv

load_dotenv()

payment_bp = Blueprint('payment', __name__, url_prefix='/api/payments')

# ============================================================================
# PAYMENT CONFIGURATION
# ============================================================================

RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID', '')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET', '')


# ============================================================================
# CREATE PAYMENT ORDER (FOR ONLINE PAYMENT)
# ============================================================================

@payment_bp.route('/create-order', methods=['POST'])
@token_required
def create_payment_order():
    """Create a payment order for online (Razorpay) payment"""
    try:
        data = request.get_json()
        order_id = data.get('order_id')
        amount = data.get('amount')
        payment_method = data.get('payment_method', 'razorpay')
        
        if not order_id or not amount:
            return jsonify({
                'success': False,
                'message': 'Order ID and amount are required'
            }), 400
        
        if amount <= 0:
            return jsonify({
                'success': False,
                'message': 'Amount must be greater than 0'
            }), 400
        
        db = get_db()
        orders_collection = db['orders']
        payments_collection = db['payments']
        
        # Verify order exists
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
        
        # Check if order already has payment
        if order.get('payment_status') == 'completed':
            return jsonify({
                'success': False,
                'message': 'Order is already paid'
            }), 400
        
        # Create payment record
        payment_doc = {
            'order_id': ObjectId(order_id),
            'amount': amount,
            'currency': 'INR',
            'payment_method': payment_method,
            'status': 'pending',  # pending, processing, completed, failed
            'razorpay_order_id': None,
            'razorpay_payment_id': None,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        payment_result = payments_collection.insert_one(payment_doc)
        payment_id = str(payment_result.inserted_id)
        
        # If using Razorpay
        if payment_method == 'razorpay':
            if not RAZORPAY_KEY_ID or not RAZORPAY_KEY_SECRET:
                return jsonify({
                    'success': False,
                    'message': 'Razorpay credentials not configured'
                }), 500
            
            # Create Razorpay order
            import razorpay
            client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
            
            razorpay_order = client.order.create({
                'amount': int(amount * 100),  # Amount in paise
                'currency': 'INR',
                'receipt': f'quickbite_{order_id}',
                'notes': {
                    'order_id': str(order_id),
                    'user_email': order.get('user_email', '')
                }
            })
            
            # Update payment with Razorpay order ID
            payments_collection.update_one(
                {'_id': ObjectId(payment_id)},
                {'$set': {'razorpay_order_id': razorpay_order['id']}}
            )
            
            return jsonify({
                'success': True,
                'message': 'Payment order created successfully',
                'payment_id': payment_id,
                'razorpay_order_id': razorpay_order['id'],
                'razorpay_key': RAZORPAY_KEY_ID,
                'amount': amount,
                'currency': 'INR'
            }), 201
        
        return jsonify({
            'success': True,
            'message': 'Payment order created successfully',
            'payment_id': payment_id,
            'amount': amount,
            'payment_method': payment_method
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error creating payment: {str(e)}'
        }), 500


# ============================================================================
# VERIFY ONLINE PAYMENT (RAZORPAY)
# ============================================================================

@payment_bp.route('/verify-online', methods=['POST'])
@token_required
def verify_online_payment():
    """Verify online payment (Razorpay)"""
    try:
        data = request.get_json()
        payment_id = data.get('payment_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_signature = data.get('razorpay_signature')
        
        if not payment_id or not razorpay_payment_id or not razorpay_signature:
            return jsonify({
                'success': False,
                'message': 'Missing payment verification details'
            }), 400
        
        db = get_db()
        payments_collection = db['payments']
        orders_collection = db['orders']
        
        # Get payment record
        try:
            payment = payments_collection.find_one({'_id': ObjectId(payment_id)})
        except:
            return jsonify({
                'success': False,
                'message': 'Invalid payment ID'
            }), 400
        
        if not payment:
            return jsonify({
                'success': False,
                'message': 'Payment not found'
            }), 404
        
        # Verify signature with Razorpay
        import razorpay
        client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
        
        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': payment['razorpay_order_id'],
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })
            signature_valid = True
        except:
            signature_valid = False
        
        if not signature_valid:
            # Update payment as failed
            payments_collection.update_one(
                {'_id': ObjectId(payment_id)},
                {
                    '$set': {
                        'status': 'failed',
                        'razorpay_payment_id': razorpay_payment_id,
                        'updated_at': datetime.utcnow()
                    }
                }
            )
            
            return jsonify({
                'success': False,
                'message': 'Payment verification failed'
            }), 401
        
        # Update payment as completed
        payments_collection.update_one(
            {'_id': ObjectId(payment_id)},
            {
                '$set': {
                    'status': 'completed',
                    'razorpay_payment_id': razorpay_payment_id,
                    'updated_at': datetime.utcnow()
                }
            }
        )
        
        # Update order payment status
        orders_collection.update_one(
            {'_id': payment['order_id']},
            {
                '$set': {
                    'payment_status': 'completed',
                    'payment_method': 'online',
                    'razorpay_payment_id': razorpay_payment_id,
                    'updated_at': datetime.utcnow()
                }
            }
        )
        
        return jsonify({
            'success': True,
            'message': 'Payment verified successfully',
            'payment_id': payment_id,
            'order_id': str(payment['order_id'])
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error verifying payment: {str(e)}'
        }), 500


# ============================================================================
# MARK OFFLINE PAYMENT (CASH)
# ============================================================================

@payment_bp.route('/mark-offline', methods=['POST'])
@token_required
def mark_offline_payment():
    """
    Mark an order as paid via offline/cash payment.
    Only sellers can mark orders as paid offline.
    """
    try:
        # Check if user is seller
        if request.user_role != 'seller':
            return jsonify({
                'success': False,
                'message': 'Only sellers can mark orders as paid'
            }), 403
        
        data = request.get_json()
        order_id = data.get('order_id')
        payment_method = data.get('payment_method', 'cash')  # cash, upi, bank_transfer
        
        if not order_id:
            return jsonify({
                'success': False,
                'message': 'Order ID is required'
            }), 400
        
        db = get_db()
        orders_collection = db['orders']
        payments_collection = db['payments']
        sellers_collection = db['sellers']
        
        # Verify seller
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
                'message': 'Unauthorized: Order does not belong to your cafeteria'
            }), 403
        
        # Create payment record for offline payment
        payment_doc = {
            'order_id': ObjectId(order_id),
            'amount': order.get('total_price', 0),
            'currency': 'INR',
            'payment_method': payment_method,
            'status': 'completed',
            'received_by_seller_id': ObjectId(request.user_id),
            'received_by_seller_name': seller['name'],
            'notes': data.get('notes', ''),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        payment_result = payments_collection.insert_one(payment_doc)
        
        # Update order payment status
        orders_collection.update_one(
            {'_id': ObjectId(order_id)},
            {
                '$set': {
                    'payment_status': 'completed',
                    'payment_method': payment_method,
                    'updated_at': datetime.utcnow()
                }
            }
        )
        
        return jsonify({
            'success': True,
            'message': f'Order marked as paid via {payment_method}',
            'payment_id': str(payment_result.inserted_id),
            'order_id': order_id,
            'amount': order.get('total_price', 0)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500


# ============================================================================
# GET PAYMENT HISTORY
# ============================================================================

@payment_bp.route('/history', methods=['GET'])
@token_required
def get_payment_history():
    """Get payment history"""
    try:
        db = get_db()
        payments_collection = db['payments']
        
        # Get query parameters
        limit = int(request.args.get('limit', 50))
        offset = int(request.args.get('offset', 0))
        payment_method = request.args.get('payment_method', None)
        status = request.args.get('status', None)
        
        # Build query
        query = {}
        if payment_method:
            query['payment_method'] = payment_method
        if status:
            query['status'] = status
        
        # For sellers, filter by their orders only
        if request.user_role == 'seller':
            sellers_collection = db['sellers']
            seller = sellers_collection.find_one({'_id': ObjectId(request.user_id)})
            if seller:
                orders_collection = db['orders']
                seller_order_ids = [
                    doc['_id'] for doc in orders_collection.find(
                        {'cafeteria_id': seller['college_id']},
                        {'_id': 1}
                    )
                ]
                query['order_id'] = {'$in': seller_order_ids}
        
        # Get total count
        total = payments_collection.count_documents(query)
        
        # Get payments
        payments = list(
            payments_collection.find(query)
            .sort('created_at', -1)
            .skip(offset)
            .limit(limit)
        )
        
        payment_list = []
        for payment in payments:
            payment_list.append({
                'id': str(payment['_id']),
                'order_id': str(payment['order_id']),
                'amount': payment['amount'],
                'currency': payment.get('currency', 'INR'),
                'payment_method': payment['payment_method'],
                'status': payment['status'],
                'created_at': payment.get('created_at').isoformat() if payment.get('created_at') else None,
                'received_by': payment.get('received_by_seller_name', 'System'),
                'notes': payment.get('notes', '')
            })
        
        return jsonify({
            'success': True,
            'payments': payment_list,
            'pagination': {
                'total': total,
                'limit': limit,
                'offset': offset,
                'count': len(payments)
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching payment history: {str(e)}'
        }), 500


# ============================================================================
# GET PAYMENT DETAILS
# ============================================================================

@payment_bp.route('/<payment_id>', methods=['GET'])
@token_required
def get_payment_details(payment_id):
    """Get payment details"""
    try:
        db = get_db()
        payments_collection = db['payments']
        
        try:
            payment = payments_collection.find_one({'_id': ObjectId(payment_id)})
        except:
            return jsonify({
                'success': False,
                'message': 'Invalid payment ID'
            }), 400
        
        if not payment:
            return jsonify({
                'success': False,
                'message': 'Payment not found'
            }), 404
        
        return jsonify({
            'success': True,
            'payment': {
                'id': str(payment['_id']),
                'order_id': str(payment['order_id']),
                'amount': payment['amount'],
                'currency': payment.get('currency', 'INR'),
                'payment_method': payment['payment_method'],
                'status': payment['status'],
                'razorpay_payment_id': payment.get('razorpay_payment_id'),
                'created_at': payment.get('created_at').isoformat() if payment.get('created_at') else None,
                'updated_at': payment.get('updated_at').isoformat() if payment.get('updated_at') else None,
                'received_by': payment.get('received_by_seller_name', ''),
                'notes': payment.get('notes', '')
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching payment: {str(e)}'
        }), 500
