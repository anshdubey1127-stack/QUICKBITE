from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from database import db_manager
from routes.auth import auth_bp
from routes.colleges import college_bp
from routes.menu import menu_bp
from routes.orders import order_bp
from routes.seller_auth import seller_auth_bp
from routes.seller_dashboard import seller_dashboard_bp
from routes.payments import payment_bp

load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Load config
env = os.getenv('FLASK_ENV', 'development')
from config import config
app.config.from_object(config[env])

# Enable CORS
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://localhost:8000", "*"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(college_bp)
app.register_blueprint(menu_bp)
app.register_blueprint(order_bp)
app.register_blueprint(seller_auth_bp)
app.register_blueprint(seller_dashboard_bp)
app.register_blueprint(payment_bp)

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """API health check"""
    return jsonify({
        'success': True,
        'message': 'QuickBite Backend is running',
        'version': '1.0.0',
        'timestamp': str(__import__('datetime').datetime.utcnow())
    }), 200

@app.route('/', methods=['GET'])
def home():
    """API home endpoint"""
    return jsonify({
        'success': True,
        'message': 'Welcome to QuickBite API',
        'version': '1.0.0',
        'documentation': '/docs'
    }), 200

# 404 handler
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'message': 'Route not found'
    }), 404

# 500 handler
@app.errorhandler(500)
def server_error(error):
    return jsonify({
        'success': False,
        'message': 'Internal server error'
    }), 500

# Before request - connect to DB
@app.before_request
def before_request():
    """Connect to database before each request"""
    try:
        db_manager.get_db()
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Database connection error: {str(e)}'
        }), 503

if __name__ == '__main__':
    PORT = int(os.getenv('PORT', 5000))
    try:
        print("╔════════════════════════════════════════════════════════════════╗")
        print("║                     QUICKBITE BACKEND                          ║")
        print("║                  Python Flask + MongoDB                        ║")
        print("╚════════════════════════════════════════════════════════════════╝")
        print("")
        
        # Connect to database
        db_manager.connect()
        
        print(f"🚀 Server starting on http://localhost:{PORT}")
        print(f"📚 API Documentation: http://localhost:{PORT}/docs")
        print(f"🏥 Health Check: http://localhost:{PORT}/api/health")
        print("")
        print("Available Endpoints:")
        print("  🔐 Customer Authentication:")
        print("     POST   /api/auth/register")
        print("     POST   /api/auth/login")
        print("     POST   /api/auth/verify")
        print("     GET    /api/auth/profile")
        print("")
        print("  🍳 Seller/Canteen Owner Authentication:")
        print("     POST   /api/seller/auth/register")
        print("     POST   /api/seller/auth/login")
        print("     GET    /api/seller/auth/profile")
        print("     PUT    /api/seller/auth/profile")
        print("     POST   /api/seller/auth/change-password")
        print("")
        print("  📊 Seller Dashboard:")
        print("     GET    /api/seller/dashboard/orders")
        print("     GET    /api/seller/dashboard/orders/<order_id>")
        print("     PUT    /api/seller/dashboard/orders/<order_id>/status")
        print("     POST   /api/seller/dashboard/orders/<order_id>/verify-pickup")
        print("     GET    /api/seller/dashboard/statistics")
        print("")
        print("  💳 Payments:")
        print("     POST   /api/payments/create-order")
        print("     POST   /api/payments/verify-online")
        print("     POST   /api/payments/mark-offline")
        print("     GET    /api/payments/history")
        print("     GET    /api/payments/<payment_id>")
        print("")
        print("  🏫 Colleges:")
        print("     GET    /api/colleges")
        print("     GET    /api/colleges/<college_id>")
        print("     GET    /api/colleges/cafeterias/<college_id>")
        print("")
        print("  🍔 Menu:")
        print("     GET    /api/menu")
        print("     GET    /api/menu/<item_id>")
        print("     POST   /api/menu (Seller only)")
        print("")
        print("  📦 Orders:")
        print("     POST   /api/orders/create")
        print("     GET    /api/orders/<order_id>")
        print("     GET    /api/orders/user/orders")
        print("     POST   /api/orders/<order_id>/verify-qr (Seller)")
        print("     POST   /api/orders/<order_id>/verify-token (Seller)")
        print("     GET    /api/orders/available-slots")
        print("")
        
        app.run(debug=True, host='0.0.0.0', port=PORT)
    except Exception as e:
        print(f"❌ Error starting server: {str(e)}")
        exit(1)
