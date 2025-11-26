╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║              📚 WHERE TO SEE YOUR DATABASE DATA - COMPLETE GUIDE 📚        ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝

Your QUICKBITE project stores data in MongoDB with 4 collections:
  1. users (with unique User IDs)
  2. colleges
  3. menuitems  
  4. orders


════════════════════════════════════════════════════════════════════════════
FASTEST WAY: MONGODB COMPASS (Visual - Recommended!)
════════════════════════════════════════════════════════════════════════════

This is the easiest way for beginners!

Step 1: Download MongoDB Compass
  Visit: https://www.mongodb.com/products/compass
  Download and install (2-3 minutes)

Step 2: Open Compass

Step 3: Connect
  URL: mongodb://localhost:27017
  Click "Connect"

Step 4: Browse Collections
  Left panel → quickbite database
  Click on collections:
    ✓ users → See all users with their IDs
    ✓ colleges → See all colleges
    ✓ menuitems → See all menu items
    ✓ orders → See all orders

Step 5: See your data in nice tables!

PROS:
  ✓ Visual and easy
  ✓ No terminal commands needed
  ✓ See data in formatted tables
  ✓ Export data easily


════════════════════════════════════════════════════════════════════════════
QUICK WAY: MONGODB SHELL (Terminal - Most Powerful!)
════════════════════════════════════════════════════════════════════════════

Step 1: Keep server running
  Terminal 1: npm run dev

Step 2: Open new terminal
  Terminal 2: mongosh

Step 3: Select database
  mongosh> use quickbite

Step 4: View data - Copy & Paste Commands:

  See ALL USERS (with IDs):
    db.users.find().pretty()
    
  See ALL COLLEGES:
    db.colleges.find().pretty()
    
  See ALL MENU ITEMS:
    db.menuitems.find().pretty()
    
  See ALL ORDERS:
    db.orders.find().pretty()

Step 5: Exit
  mongosh> exit

PROS:
  ✓ Fast and powerful
  ✓ Search and filter easily
  ✓ Complex queries possible
  ✓ No software to install


════════════════════════════════════════════════════════════════════════════
BEST WAY: REST API (Using curl)
════════════════════════════════════════════════════════════════════════════

Step 1: Keep server running
  Terminal 1: npm run dev

Step 2: Open new terminal
  Terminal 2: Use curl commands

Step 3: Get data - Copy & Paste Commands:

  Get ALL COLLEGES:
    curl http://localhost:3000/api/colleges
    
  Get ALL MENU ITEMS:
    curl http://localhost:3000/api/menu
    
  Get MENU by CAFETERIA:
    curl "http://localhost:3000/api/menu?cafeteria=Main%20Cafeteria"
    
  Get VEGETARIAN ITEMS:
    curl "http://localhost:3000/api/menu?veg=true"

Output is JSON format - perfect for integration!

PROS:
  ✓ Programmatic access
  ✓ Easy to integrate with frontend
  ✓ Same endpoint as your app uses
  ✓ Test your API


════════════════════════════════════════════════════════════════════════════
BEFORE YOU START: POPULATE DATABASE
════════════════════════════════════════════════════════════════════════════

Your database is currently EMPTY. Add sample data first:

Step 1: Keep server running
  Terminal 1: npm run dev

Step 2: New terminal
  Terminal 2: cd /Users/anshdubey1127/QUICKBITE

Step 3: Seed database
  Terminal 2: node seed.js

Wait for:
  ✓ Connected to MongoDB
  ✓ 6 colleges seeded
  ✓ 8 menu items seeded
  ✓ Database seeded successfully!

NOW you have data to view!


════════════════════════════════════════════════════════════════════════════
COMPLETE COPY-PASTE WORKFLOW
════════════════════════════════════════════════════════════════════════════

TERMINAL 1 (Keep running):
  npm run dev

TERMINAL 2 (New terminal):
  cd /Users/anshdubey1127/QUICKBITE
  node seed.js
  mongosh
  
MONGOSH COMMANDS:
  use quickbite
  db.users.find().pretty()
  db.colleges.find().pretty()
  db.menuitems.find().pretty()
  exit


════════════════════════════════════════════════════════════════════════════
UNDERSTAND YOUR DATA STRUCTURE
════════════════════════════════════════════════════════════════════════════

USERS Collection Example:
{
  "_id": ObjectId("673d8f1a2c4e5f6a7b8c9d0e"),  ← USER ID (What you asked for!)
  "name": "John Doe",
  "email": "john@example.com",
  "password": "$2a$10$...",  (securely hashed)
  "college": "ABES Engineering College",
  "phone": "9876543210",
  "createdAt": ISODate("2025-11-14T10:30:00.000Z"),
  "updatedAt": ISODate("2025-11-14T10:30:00.000Z")
}

The _id field is the UNIQUE USER ID!


COLLEGES Collection Example:
{
  "_id": ObjectId("..."),
  "name": "ABES Engineering College",
  "location": "Ghaziabad",
  "cafeterias": ["Main Cafeteria", "Food Court", "QuickBite Corner"],
  "image": "https://...",
  "description": "Premier engineering college..."
}


MENUITEMS Collection Example:
{
  "_id": ObjectId("..."),
  "name": "Masala Dosa",
  "price": 60,
  "category": "Breakfast",
  "veg": true,
  "cafeteria": "Main Cafeteria",
  "description": "Crispy dosa with potato filling",
  "available": true
}


ORDERS Collection Example:
{
  "_id": ObjectId("..."),
  "user": ObjectId("673d8f1a2c4e5f6a7b8c9d0e"),  ← Links to User ID
  "items": [
    {
      "menuItem": ObjectId("..."),
      "quantity": 2,
      "price": 60
    }
  ],
  "college": "ABES Engineering College",
  "cafeteria": "Main Cafeteria",
  "totalPrice": 120,
  "status": "Pending",
  "orderToken": "ORD12345678"
}


════════════════════════════════════════════════════════════════════════════
COMMANDS BY COLLECTION
════════════════════════════════════════════════════════════════════════════

USERS:
  db.users.find().pretty()              # See all users
  db.users.countDocuments()             # Count total users
  db.users.findOne({email: "..."})      # Find by email
  db.users.findOne({_id: ObjectId("...")}) # Find by ID

COLLEGES:
  db.colleges.find().pretty()           # See all colleges
  db.colleges.countDocuments()          # Count colleges (should be 6)
  db.colleges.findOne({name: "..."})    # Find specific college

MENUITEMS:
  db.menuitems.find().pretty()          # See all items
  db.menuitems.countDocuments()         # Count items (should be 8)
  db.menuitems.find({veg: true})        # Find vegetarian items
  db.menuitems.find({cafeteria: "..."}) # Find by cafeteria

ORDERS:
  db.orders.find().pretty()             # See all orders
  db.orders.countDocuments()            # Count orders
  db.orders.find({status: "Pending"})   # Find pending orders
  db.orders.find({user: ObjectId("...")}) # Find orders by user


════════════════════════════════════════════════════════════════════════════
RECOMMENDED READING ORDER
════════════════════════════════════════════════════════════════════════════

1. This file (you're reading it!) ✓
2. POPULATE_DATABASE.md - Add sample data first
3. VIEW_DATA_QUICK_GUIDE.md - 3-step visual guide
4. DB_QUICK_REFERENCE.md - Quick command reference
5. VIEW_DATABASE.md - Detailed database guide


════════════════════════════════════════════════════════════════════════════
QUICK SUMMARY TABLE
════════════════════════════════════════════════════════════════════════════

Method          | Speed | Easiness | Best For
───────────────────────────────────────────────────────────────────────────
MongoDB Compass | Fast  | Very Easy | Beginners, Visual People
MongoDB Shell   | Super | Medium    | Power Users, Complex Queries
REST API        | Fast  | Easy      | Developers, Integration
───────────────────────────────────────────────────────────────────────────


════════════════════════════════════════════════════════════════════════════
NEXT STEPS AFTER VIEWING DATA
════════════════════════════════════════════════════════════════════════════

✓ Register new users via API
  curl -X POST http://localhost:3000/api/auth/signup \
    -H "Content-Type: application/json" \
    -d '{"name":"Jane","email":"jane@example.com","password":"pass123"}'

✓ Place orders
✓ Connect frontend (script.js) to use the database
✓ Deploy to production
✓ Add more features


════════════════════════════════════════════════════════════════════════════
TROUBLESHOOTING
════════════════════════════════════════════════════════════════════════════

No data showing?
  → Run: node seed.js (first time only)

Can't connect to MongoDB?
  → Start it: brew services start mongodb-community

mongosh not found?
  → Install: brew install mongosh

Port error?
  → Check if server is running: npm run dev

Data disappearing?
  → Don't worry, it's saved in MongoDB!
  → Check with: db.collections.countDocuments()


════════════════════════════════════════════════════════════════════════════

                    ✨ YOU NOW KNOW HOW TO: ✨

✓ View all users (with User IDs)
✓ View all colleges
✓ View all menu items
✓ View all orders
✓ Search and filter data
✓ Understand your data structure
✓ Populate the database

Pick your favorite method and start exploring!

════════════════════════════════════════════════════════════════════════════

Date: November 14, 2025
Status: ✅ Complete Guide Ready
Next: Follow POPULATE_DATABASE.md
