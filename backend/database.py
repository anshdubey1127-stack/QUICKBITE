from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    """MongoDB database connection handler"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.client = None
            cls._instance.db = None
        return cls._instance
    
    def connect(self):
        """Connect to MongoDB"""
        try:
            mongo_uri = os.getenv('DATABASE_URI', 'mongodb://localhost:27017/quickbite')
            self.client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            # Test the connection
            self.client.admin.command('ping')
            self.db = self.client['quickbite']
            print(f"✅ MongoDB Connected: {mongo_uri}")
            return self.db
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            print(f"❌ MongoDB Connection Error: {str(e)}")
            raise Exception(f"Failed to connect to MongoDB: {str(e)}")
    
    def get_db(self):
        """Get database instance"""
        if self.db is None:
            self.connect()
        return self.db
    
    def close(self):
        """Close database connection"""
        if self.client:
            self.client.close()
            print("✅ MongoDB Connection Closed")

# Singleton instance
db_manager = Database()

def get_db():
    """Helper function to get database"""
    return db_manager.get_db()
