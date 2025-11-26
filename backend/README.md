# 🚀 QUICKBITE Backend - Complete Solution

**College Food Pre-Ordering System with QR Code & Token Verification**

![Status](https://img.shields.io/badge/status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.3-blue)
![MongoDB](https://img.shields.io/badge/MongoDB-6.0%2B-green)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [Testing](#testing)
- [Deployment](#deployment)
- [Support](#support)

---

## 🎯 Overview

**QUICKBITE** is a modern food pre-ordering system designed for college canteens with:

- **User Registration & Authentication** - Secure JWT-based auth with bcryptjs
- **College Management** - Multiple colleges with cafeterias
- **Food Ordering** - Browse menu, place orders with customization
- **Pickup Scheduling** - Pre-defined time slots for food pickup
- **QR Code Verification** - Scannable QR codes for contactless verification
- **Token-Based System** - Simple 6-digit tokens for verification
- **Seller Dashboard** - Manage orders, verify customers
- **Order Tracking** - Real-time order status updates
- **Payment Integration** - Ready for Razorpay/Stripe

---

## ✨ Features

### User Features
- ✅ Register with college, phone, email
- ✅ Secure login with JWT tokens
- ✅ Browse colleges and menus
- ✅ View food by category (Breakfast, Lunch, Dinner, Snacks, etc.)
- ✅ Filter vegetarian/non-veg items
- ✅ Place pre-orders with pickup time
- ✅ View order history
- ✅ Get QR code + Token for order
- ✅ Track order status

### Seller Features
- ✅ View orders for their cafeteria
- ✅ Scan QR code to verify customer
- ✅ Enter token to verify order
- ✅ Update order status (pending → ready → completed)
- ✅ Add/manage menu items
- ✅ Set item availability

### Admin Features
- ✅ Manage colleges
- ✅ Manage cafeterias
- ✅ View all orders
- ✅ User management

---

## 🛠️ Tech Stack

### Backend
- **Python 3.8+** - Programming language
- **Flask 2.3.3** - Web framework
- **PyJWT 2.8.1** - JSON Web Tokens
- **bcryptjs 1.7.1** - Password hashing
- **QRCode 7.4.2** - QR code generation
- **python-dotenv** - Environment variables

### Database
- **MongoDB 6.0+** - NoSQL database
- **PyMongo 4.5.0** - MongoDB driver

### Optional
- **Razorpay 1.3.0** - Payment gateway

---

## 🚀 Quick Start

### Prerequisites
```bash
# Check Python version (3.8+ required)
python3 --version

# Check MongoDB is installed
mongosh --version
```

### Installation (5 minutes)

**Step 1: Start MongoDB**
```bash
brew services start mongodb-community
```

**Step 2: Navigate to backend**
```bash
cd /Users/anshdubey1127/QUICKBITE/backend
```

**Step 3: Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Step 4: Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 5: Run server**
```bash
python3 app.py
```

✅ Server running on `http://localhost:5000`

---

## 📚 API Documentation

### Base URL
```
http://localhost:5000
```

### Authentication
All protected endpoints require:
```
Authorization: Bearer <token>
```

### Core Endpoints

#### 🔐 Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/verify` - Verify token
- `GET /api/auth/profile` - Get user profile

#### 🏫 Colleges
- `GET /api/colleges` - Get all colleges
- `GET /api/colleges/<id>` - Get college details
- `GET /api/colleges/cafeterias/<id>` - Get cafeterias

#### 🍔 Menu
- `GET /api/menu` - Get menu items
- `GET /api/menu/<id>` - Get item details
- `POST /api/menu` - Create menu item (Seller)
- `GET /api/menu?veg_only=true` - Filter vegetarian

#### 📦 Orders
- `POST /api/orders/create` - Create order
- `GET /api/orders/<id>` - Get order details
- `GET /api/orders/user/orders` - Get user orders
- `POST /api/orders/<id>/verify-qr` - Verify by QR (Seller)
- `POST /api/orders/<id>/verify-token` - Verify by token (Seller)
- `GET /api/orders/available-slots` - Get pickup slots

---

## 📊 Database Schema

### Collections

#### Users
```javascript
{
  _id: ObjectId,
  name: String,
  email: String (unique),
  password: String (bcryptjs hash),
  phone: String,
  college: String,
  role: String (user|seller|admin),
  created_at: Date,
  updated_at: Date
}
```

#### Colleges
```javascript
{
  _id: ObjectId,
  name: String (unique),
  location: String,
  image: String,
  description: String,
  cafeterias: [String],
  delivery_time: String,
  created_at: Date,
  updated_at: Date
}
```

#### Menu Items
```javascript
{
  _id: ObjectId,
  name: String,
  description: String,
  price: Number,
  category: String,
  is_veg: Boolean,
  image: String,
  available: Boolean,
  cafeteria_id: String,
  college_id: String,
  seller_id: ObjectId,
  created_at: Date,
  updated_at: Date
}
```

#### Orders
```javascript
{
  _id: ObjectId,
  user_id: ObjectId,
  user_email: String,
  college_id: String,
  cafeteria_id: String,
  items: [{
    item_id: String,
    name: String,
    price: Number,
    quantity: Number,
    subtotal: Number
  }],
  total_price: Number,
  order_token: String (unique),
  pickup_time: String,
  special_instructions: String,
  status: String (pending|confirmed|preparing|ready|completed|cancelled),
  payment_status: String (pending|completed|failed),
  qr_code: String (base64),
  created_at: Date,
  updated_at: Date
}
```

---

## 🧪 Testing

### Health Check
```bash
curl http://localhost:5000/api/health
```

### Register User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@college.edu",
    "password": "password123",
    "phone": "9876543210",
    "college": "ABES Engineering College"
  }'
```

### Seed Sample Data
```bash
python3 seed.py
```

### Using Postman
1. Import `QUICKBITE_API.postman_collection.json`
2. Set `base_url` variable to `http://localhost:5000`
3. Set `token` variable after login
4. Test all endpoints

---

## 📦 Sample Data

Run seed script to populate database:
```bash
python3 seed.py
```

This adds:
- 3 colleges with cafeterias
- 8 food items (Indian & international cuisines)
- Categories: Breakfast, Lunch, Dinner, Snacks, Beverages, Desserts

---

## 🔐 Security Features

- ✅ Password hashing with bcryptjs (10 rounds)
- ✅ JWT tokens with 7-day expiration
- ✅ CORS protection
- ✅ Input validation on all endpoints
- ✅ Role-based access control (User, Seller, Admin)
- ✅ SQL injection prevention
- ✅ Unique email constraint
- ✅ Hashed passwords in database

---

## 🌐 Environment Configuration

Create `.env` file:
```properties
DATABASE_URI=mongodb://localhost:27017/quickbite
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000
JWT_SECRET=your_secure_secret_key_here
JWT_EXPIRY=604800
RAZORPAY_KEY_ID=your_key_id
RAZORPAY_KEY_SECRET=your_secret
CORS_ORIGIN=http://localhost:3000
```

---

## 🚀 Deployment

### Heroku
```bash
heroku create quickbite
git push heroku main
heroku config:set JWT_SECRET=your_secret
```

### AWS EC2
```bash
# SSH into instance
ssh -i key.pem ec2-user@instance-ip
cd /home/ec2-user
git clone your-repo
cd quickbite/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```

### Docker (Optional)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python3", "app.py"]
```

---

## 📝 File Structure

```
backend/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── database.py                 # MongoDB connection
├── auth.py                     # Authentication utilities
├── utils.py                    # Helper functions
├── seed.py                     # Sample data
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
│
├── routes/
│   ├── __init__.py
│   ├── auth.py                 # Authentication routes
│   ├── colleges.py             # College routes
│   ├── menu.py                 # Menu routes
│   └── orders.py               # Order routes
│
├── BACKEND_SETUP_GUIDE.md      # Full setup documentation
├── QUICK_START.md              # 5-minute quick start
├── QUICKBITE_API.postman_collection.json
└── README.md                   # This file
```

---

## 🐛 Troubleshooting

### MongoDB Connection Error
```bash
# Start MongoDB
brew services start mongodb-community

# Check status
brew services list
```

### Port Already in Use
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Or change port in .env
PORT=5001
```

### Module Not Found
```bash
# Check virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

---

## 📞 Support

For detailed documentation:
- 📖 **Setup Guide**: See `BACKEND_SETUP_GUIDE.md`
- 🚀 **Quick Start**: See `QUICK_START.md`
- 📚 **API Reference**: See this README

---

## 🎯 Next Steps

1. ✅ Run backend server
2. ✅ Seed sample data
3. ✅ Test with Postman
4. ✅ Connect frontend
5. ✅ Add payment integration
6. ✅ Deploy to production

---

## 📄 License

MIT License - Free to use and modify

---

## 👨‍💻 Author

Built for QUICKBITE - College Food Pre-Ordering System

---

## 🎉 Ready to Launch!

Your complete backend is production-ready. Customize for your college's needs and launch!

**Last Updated**: November 14, 2025  
**Status**: ✅ Production Ready  
**Version**: 1.0.0
