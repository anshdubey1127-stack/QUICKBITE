from flask import Blueprint, request, jsonify
from database import get_db
from auth import token_required
from bson.objectid import ObjectId
from datetime import datetime

college_bp = Blueprint('college', __name__, url_prefix='/api/colleges')

@college_bp.route('/', methods=['GET'])
def get_colleges():
    """Get all colleges"""
    try:
        db = get_db()
        colleges_collection = db['colleges']
        
        colleges = list(colleges_collection.find({}))
        
        # Format response
        result = []
        for college in colleges:
            result.append({
                'id': str(college['_id']),
                'name': college['name'],
                'location': college.get('location', ''),
                'image': college.get('image', ''),
                'description': college.get('description', ''),
                'cafeterias': college.get('cafeterias', []),
                'delivery_time': college.get('delivery_time', '30 mins')
            })
        
        return jsonify({
            'success': True,
            'count': len(result),
            'colleges': result
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching colleges: {str(e)}'
        }), 500

@college_bp.route('/<college_id>', methods=['GET'])
def get_college(college_id):
    """Get college by ID"""
    try:
        db = get_db()
        colleges_collection = db['colleges']
        
        college = colleges_collection.find_one({'_id': ObjectId(college_id)})
        if not college:
            return jsonify({
                'success': False,
                'message': 'College not found'
            }), 404
        
        return jsonify({
            'success': True,
            'college': {
                'id': str(college['_id']),
                'name': college['name'],
                'location': college.get('location', ''),
                'image': college.get('image', ''),
                'description': college.get('description', ''),
                'cafeterias': college.get('cafeterias', []),
                'delivery_time': college.get('delivery_time', '30 mins')
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching college: {str(e)}'
        }), 500

@college_bp.route('/cafeterias/<college_id>', methods=['GET'])
def get_cafeterias(college_id):
    """Get cafeterias for a college"""
    try:
        db = get_db()
        cafeterias_collection = db['cafeterias']
        
        cafeterias = list(cafeterias_collection.find({'college_id': college_id}))
        
        result = []
        for cafeteria in cafeterias:
            result.append({
                'id': str(cafeteria['_id']),
                'name': cafeteria['name'],
                'location': cafeteria.get('location', ''),
                'image': cafeteria.get('image', ''),
                'rating': cafeteria.get('rating', 4.5),
                'delivery_time': cafeteria.get('delivery_time', '30 mins'),
                'is_open': cafeteria.get('is_open', True)
            })
        
        return jsonify({
            'success': True,
            'count': len(result),
            'cafeterias': result
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error fetching cafeterias: {str(e)}'
        }), 500

@college_bp.route('/', methods=['POST'])
@token_required
def create_college():
    """Create new college (Admin only)"""
    try:
        if request.user_role != 'admin':
            return jsonify({
                'success': False,
                'message': 'Admin access required'
            }), 403
        
        data = request.get_json()
        required_fields = ['name', 'location']
        
        if not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'message': 'Missing required fields'
            }), 400
        
        db = get_db()
        colleges_collection = db['colleges']
        
        college_doc = {
            'name': data['name'],
            'location': data['location'],
            'image': data.get('image', ''),
            'description': data.get('description', ''),
            'cafeterias': data.get('cafeterias', []),
            'delivery_time': data.get('delivery_time', '30 mins'),
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        
        result = colleges_collection.insert_one(college_doc)
        
        return jsonify({
            'success': True,
            'message': 'College created successfully',
            'college_id': str(result.inserted_id)
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error creating college: {str(e)}'
        }), 500
