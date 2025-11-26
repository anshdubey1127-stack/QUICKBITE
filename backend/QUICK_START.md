╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                             ║
║           🚀 QUICKBITE BACKEND - QUICK START GUIDE (5 MINUTES) 🚀         ║
║                                                                             ║
║                Get your backend running in 5 simple steps!                  ║
║                                                                             ║
╚═══════════════════════════════════════════════════════════════════════════╝


════════════════════════════════════════════════════════════════════════════
✅ PREREQUISITES (Check These First!)
════════════════════════════════════════════════════════════════════════════

Python installed?
  python3 --version

MongoDB installed?
  mongosh --version

If not installed, download:
  • Python: https://www.python.org/downloads/
  • MongoDB: https://www.mongodb.com/try/download/community


════════════════════════════════════════════════════════════════════════════
🚀 5-STEP QUICK START
════════════════════════════════════════════════════════════════════════════

STEP 1: Start MongoDB
─────────────────────────────────────────────────────────────────────────────

Terminal 1:
  brew services start mongodb-community

Wait for:
  ✓ MongoDB started (or shows "already running")


STEP 2: Navigate to Backend Directory
─────────────────────────────────────────────────────────────────────────────

Terminal 2:
  cd /Users/anshdubey1127/QUICKBITE/backend


STEP 3: Create & Activate Virtual Environment
─────────────────────────────────────────────────────────────────────────────

Create virtual environment:
  python3 -m venv venv

Activate it:
  source venv/bin/activate

You should see: (venv) before your terminal prompt ✓


STEP 4: Install Dependencies
─────────────────────────────────────────────────────────────────────────────

Install packages:
  pip install -r requirements.txt

Wait for completion (2-3 minutes)

Verify:
  python3 -c "import flask; print('✅ Flask installed')"


STEP 5: Run the Server
─────────────────────────────────────────────────────────────────────────────

Start Flask server:
  python3 app.py

You should see:
  ╔════════════════════════════════════════════════════════════════╗
  ║                     QUICKBITE BACKEND                          ║
  ║                  Python Flask + MongoDB                        ║
  ║
  ║  ✅ MongoDB Connected: mongodb://localhost:27017/quickbite     ║
  ║  🚀 Server starting on http://localhost:5000                   ║
  ║                                                                ║
  ║  Available Endpoints:                                          ║
  ║    POST   /api/auth/register                                   ║
  ║    POST   /api/auth/login                                      ║
  ║    GET    /api/colleges                                        ║
  ║    POST   /api/orders/create                                   ║
  ║    ...                                                         ║
  ╚════════════════════════════════════════════════════════════════╝

🎉 BACKEND IS RUNNING! ✅


════════════════════════════════════════════════════════════════════════════
🧪 TEST THE BACKEND (5 MINUTES)
════════════════════════════════════════════════════════════════════════════

Terminal 3: Test API with curl

1. Check Health:
──────────────────────────────────────────────────────────────────────────────
curl http://localhost:5000/api/health

Expected Response:
{
  "success": true,
  "message": "QuickBite Backend is running",
  "version": "1.0.0"
}


2. Get All Colleges:
──────────────────────────────────────────────────────────────────────────────
curl http://localhost:5000/api/colleges

Expected Response:
{
  "success": true,
  "count": 0,
  "colleges": []
}

(No data yet - add sample data with seed.py next!)


3. Register a User:
──────────────────────────────────────────────────────────────────────────────
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@college.edu",
    "password": "password123",
    "phone": "9876543210",
    "college": "ABES Engineering College"
  }'

Expected Response:
{
  "success": true,
  "message": "User registered successfully",
  "user": {...},
  "token": "eyJhbGciOiJIUzI1NiIs..."
}

👉 COPY THE TOKEN - You'll need it for next requests!


4. Get User Profile:
──────────────────────────────────────────────────────────────────────────────
curl -X GET http://localhost:5000/api/auth/profile \
  -H "Authorization: Bearer <PASTE_YOUR_TOKEN_HERE>"

Expected Response:
{
  "success": true,
  "user": {
    "id": "...",
    "name": "Test User",
    "email": "test@college.edu",
    "college": "ABES Engineering College"
  }
}


════════════════════════════════════════════════════════════════════════════
📊 SEED DATABASE WITH SAMPLE DATA
════════════════════════════════════════════════════════════════════════════

Terminal 4 (Keep other terminals running):

  cd /Users/anshdubey1127/QUICKBITE/backend
  source venv/bin/activate  # If not already activated
  python3 seed.py

You should see:
  🌱 Starting database seeding...
  🏫 Adding colleges...
  ✅ Added 3 colleges
  🍽️  Adding cafeterias...
  ✅ Added 2 cafeterias
  🍔 Adding menu items...
  ✅ Added 8 menu items
  
  ✅ DATABASE SEEDING COMPLETED SUCCESSFULLY!

Now test colleges endpoint again:
  curl http://localhost:5000/api/colleges

Should show 3 colleges with full details! ✅


════════════════════════════════════════════════════════════════════════════
🎯 NEXT STEPS
════════════════════════════════════════════════════════════════════════════

✅ Backend running → Test with Postman (optional)
✅ Database populated → Create test orders
✅ All endpoints working → Connect to frontend

1. IMPORT POSTMAN COLLECTION (Optional - for better testing)
   - Open Postman
   - Click: Import
   - Select: QUICKBITE_API.postman_collection.json
   - Set base_url variable: http://localhost:5000
   - Start testing endpoints!

2. TEST ORDER CREATION
   - Get colleges list
   - Get menu items
   - Create order
   - Verify QR code generation

3. CONNECT TO FRONTEND
   - Update frontend/api.js base URL: http://localhost:5000
   - Update signup to call /api/auth/register
   - Update login to call /api/auth/login
   - Update order creation to call /api/orders/create

4. TEST QR CODE & TOKEN VERIFICATION
   - Create order → Get order token & QR code
   - Test seller verification:
     POST /api/orders/<order_id>/verify-token
     POST /api/orders/<order_id>/verify-qr


════════════════════════════════════════════════════════════════════════════
🔧 COMMON ISSUES & SOLUTIONS
════════════════════════════════════════════════════════════════════════════

❌ "MongoDB Connection Error"
   ✅ Start MongoDB: brew services start mongodb-community
   ✅ Check status: brew services list

❌ "pip: command not found"
   ✅ Use: pip3 instead of pip
   ✅ Or: python3 -m pip

❌ "Address already in use (:5000)"
   ✅ Kill process: lsof -ti:5000 | xargs kill -9
   ✅ Or change PORT in .env

❌ "Module not found: flask"
   ✅ Check virtual environment is activated: (venv) in prompt
   ✅ Reinstall: pip install -r requirements.txt

❌ "Permission denied"
   ✅ Make seed.py executable: chmod +x seed.py
   ✅ Or run: python3 seed.py (instead of ./seed.py)


════════════════════════════════════════════════════════════════════════════
📝 FILE STRUCTURE CREATED
════════════════════════════════════════════════════════════════════════════

/Users/anshdubey1127/QUICKBITE/backend/
├── app.py                          # Main Flask app
├── config.py                       # Configuration
├── database.py                     # MongoDB connection
├── auth.py                         # Authentication
├── utils.py                        # Utilities (QR, tokens)
├── seed.py                         # Sample data
├── requirements.txt                # Python packages
├── .env                            # Environment config
│
├── routes/
│   ├── auth.py                     # Auth endpoints
│   ├── colleges.py                 # College endpoints
│   ├── menu.py                     # Menu endpoints
│   └── orders.py                   # Order endpoints
│
├── BACKEND_SETUP_GUIDE.md          # Full documentation
├── QUICKBITE_API.postman_collection.json
└── README_BACKEND.md               # Backend README


════════════════════════════════════════════════════════════════════════════
📚 KEY ENDPOINTS TO TEST
════════════════════════════════════════════════════════════════════════════

MUST TEST THESE:

1. ✅ Health Check
   GET /api/health

2. ✅ Register User
   POST /api/auth/register

3. ✅ Login
   POST /api/auth/login

4. ✅ Get Colleges
   GET /api/colleges

5. ✅ Get Menu
   GET /api/menu

6. ✅ Create Order
   POST /api/orders/create

7. ✅ Get Order Details
   GET /api/orders/<order_id>

8. ✅ Verify Token (Seller)
   POST /api/orders/<order_id>/verify-token


════════════════════════════════════════════════════════════════════════════
💡 QUICK REFERENCE
════════════════════════════════════════════════════════════════════════════

API Base URL:
  http://localhost:5000

Database:
  mongodb://localhost:27017/quickbite

Authentication:
  Header: Authorization: Bearer <token>

Port:
  5000 (configurable in .env)

Environment:
  Development (set FLASK_ENV=production for production)


════════════════════════════════════════════════════════════════════════════
🎉 YOU'RE DONE!
════════════════════════════════════════════════════════════════════════════

Your QUICKBITE backend is now:
  ✅ Running on http://localhost:5000
  ✅ Connected to MongoDB
  ✅ Ready for testing
  ✅ Ready for frontend integration
  ✅ Ready to handle real orders!

Questions? Read: BACKEND_SETUP_GUIDE.md

Ready to deploy? Follow: BACKEND_SETUP_GUIDE.md → Deployment section


════════════════════════════════════════════════════════════════════════════
Date: November 14, 2025
Version: 1.0.0 - Production Ready
════════════════════════════════════════════════════════════════════════════
