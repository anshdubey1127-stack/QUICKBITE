#!/usr/bin/env python3
"""
Seed MongoDB with sample data for testing
Run: python3 seed.py
"""

from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv('DATABASE_URI', 'mongodb://localhost:27017/quickbite')

def seed_database():
    """Seed database with sample data"""
    try:
        client = MongoClient(MONGO_URI)
        db = client['quickbite']
        
        print("🌱 Starting database seeding...")
        
        # Clear existing data (optional)
        print("📦 Clearing collections...")
        # db['users'].delete_many({})
        # db['colleges'].delete_many({})
        # db['cafeterias'].delete_many({})
        # db['menu_items'].delete_many({})
        # db['orders'].delete_many({})
        
        # Seed Colleges
        print("🏫 Adding colleges...")
        colleges_data = [
            {
                'name': 'ABES Engineering College',
                'location': 'Ghaziabad, Uttar Pradesh',
                'image': 'https://images.unsplash.com/photo-1543269865-cbdf26cecdd7?w=500',
                'description': 'ABES Engineering College is a premier institution for engineering education.',
                'cafeterias': ['Main Canteen', 'South Campus Canteen'],
                'delivery_time': '30 mins',
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'name': 'KIET Group of Institutions',
                'location': 'Ghaziabad, Uttar Pradesh',
                'image': 'https://images.unsplash.com/photo-1514432324607-2e88f1a9ad8b?w=500',
                'description': 'KIET offers quality engineering and management education.',
                'cafeterias': ['Central Cafeteria', 'North Wing Canteen'],
                'delivery_time': '25 mins',
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'name': 'IMS Engineering College',
                'location': 'Ghaziabad, Uttar Pradesh',
                'image': 'https://images.unsplash.com/photo-1552664730-d307ca884978?w=500',
                'description': 'IMS Engineering College - Committed to excellence in education.',
                'cafeterias': ['Main Cafeteria'],
                'delivery_time': '30 mins',
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
        ]
        
        colleges_result = db['colleges'].insert_many(colleges_data)
        college_ids = colleges_result.inserted_ids
        print(f"✅ Added {len(colleges_result.inserted_ids)} colleges")
        
        # Seed Cafeterias
        print("🍽️  Adding cafeterias...")
        cafeterias_data = [
            {
                'name': 'Main Canteen',
                'college_id': str(college_ids[0]),
                'location': 'Ground Floor, Building A',
                'image': 'https://images.unsplash.com/photo-1517521247153-38256322e549?w=500',
                'rating': 4.5,
                'delivery_time': '30 mins',
                'is_open': True,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'name': 'South Campus Canteen',
                'college_id': str(college_ids[0]),
                'location': 'South Campus, Building C',
                'image': 'https://images.unsplash.com/photo-1555939594-58d7cb561601?w=500',
                'rating': 4.3,
                'delivery_time': '35 mins',
                'is_open': True,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
        ]
        
        cafeterias_result = db['cafeterias'].insert_many(cafeterias_data)
        cafeteria_ids = cafeterias_result.inserted_ids
        print(f"✅ Added {len(cafeterias_result.inserted_ids)} cafeterias")
        
        # Seed Menu Items
        print("🍔 Adding menu items...")
        menu_items_data = [
            {
                'name': 'Masala Dosa',
                'description': 'Crispy South Indian dosa with spicy potato filling',
                'price': 80,
                'category': 'Breakfast',
                'is_veg': True,
                'image': 'https://images.unsplash.com/photo-1589301760014-d929314efbf5?w=500',
                'available': True,
                'cafeteria_id': str(cafeteria_ids[0]),
                'college_id': str(college_ids[0]),
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'name': 'Chole Bhature',
                'description': 'Fluffy bhature served with spicy chickpeas',
                'price': 90,
                'category': 'Breakfast',
                'is_veg': True,
                'image': 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=500',
                'available': True,
                'cafeteria_id': str(cafeteria_ids[0]),
                'college_id': str(college_ids[0]),
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'name': 'Paneer Butter Masala',
                'description': 'Soft paneer cubes in creamy tomato sauce',
                'price': 150,
                'category': 'Lunch',
                'is_veg': True,
                'image': 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=500',
                'available': True,
                'cafeteria_id': str(cafeteria_ids[0]),
                'college_id': str(college_ids[0]),
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'name': 'Biryani',
                'description': 'Fragrant basmati rice with tender meat',
                'price': 180,
                'category': 'Lunch',
                'is_veg': False,
                'image': 'https://images.unsplash.com/photo-1585937421612-70a19fb6ff86?w=500',
                'available': True,
                'cafeteria_id': str(cafeteria_ids[0]),
                'college_id': str(college_ids[0]),
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'name': 'Samosa',
                'description': 'Crispy triangular pastry with spiced potato filling',
                'price': 20,
                'category': 'Snacks',
                'is_veg': True,
                'image': 'https://images.unsplash.com/photo-1599599810694-9f6aa01b99b2?w=500',
                'available': True,
                'cafeteria_id': str(cafeteria_ids[0]),
                'college_id': str(college_ids[0]),
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'name': 'Burger',
                'description': 'Juicy burger with fresh vegetables and sauce',
                'price': 120,
                'category': 'Snacks',
                'is_veg': False,
                'image': 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500',
                'available': True,
                'cafeteria_id': str(cafeteria_ids[0]),
                'college_id': str(college_ids[0]),
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'name': 'Chai',
                'description': 'Hot Indian tea with milk and spices',
                'price': 20,
                'category': 'Beverages',
                'is_veg': True,
                'image': 'https://images.unsplash.com/photo-1597318972827-3f47e6b1df15?w=500',
                'available': True,
                'cafeteria_id': str(cafeteria_ids[0]),
                'college_id': str(college_ids[0]),
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'name': 'Gulab Jamun',
                'description': 'Soft milk solids in sugar syrup',
                'price': 50,
                'category': 'Desserts',
                'is_veg': True,
                'image': 'https://images.unsplash.com/photo-1585936686006-bb6a6e936f5f?w=500',
                'available': True,
                'cafeteria_id': str(cafeteria_ids[0]),
                'college_id': str(college_ids[0]),
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
        ]
        
        menu_result = db['menu_items'].insert_many(menu_items_data)
        print(f"✅ Added {len(menu_result.inserted_ids)} menu items")
        
        print("\n" + "="*60)
        print("✅ DATABASE SEEDING COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"\n📊 Summary:")
        print(f"   • Colleges: {len(colleges_result.inserted_ids)}")
        print(f"   • Cafeterias: {len(cafeterias_result.inserted_ids)}")
        print(f"   • Menu Items: {len(menu_result.inserted_ids)}")
        print(f"\n🎯 Next steps:")
        print(f"   1. Run: python3 app.py")
        print(f"   2. Register a test user")
        print(f"   3. Create an order using the menu items above")
        print(f"   4. Check order status and QR code")
        print("\n")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Error seeding database: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    seed_database()
