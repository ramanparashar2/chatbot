import motor.motor_asyncio
from typing import Optional, Dict, Any
from pymongo.errors import ConnectionFailure
from core.config import settings

class MongoDB:
    def __init__(self, uri: str):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self.client.get_database()  # Set default database if needed

    def get_collection(self, collection_name: str):
        """Fetch a collection from the database."""
        return self.db[collection_name]

    def close(self):
        """Close the MongoDB connection."""
        self.client.close()


# MongoDB Instance
mongodb_instance: Optional[MongoDB] = None

# Dictionary to store dynamically initialized collections
collections: Dict[str, Any] = {}

async def init_db():
    """Initialize the database connection."""
    global mongodb_instance, collections
    if mongodb_instance is None:
        try:
            mongodb_instance = MongoDB(settings.MONGO_URI)
            print("MongoDB Atlas connection established")
        except ConnectionFailure as e:
            print(f"Error connecting to MongoDB Atlas: {e}")
            raise

async def get_collection(collection_name: str):
    """
    Get a collection dynamically. If it is not already initialized, initialize it.
    """
    global collections
    if collection_name not in collections:
        if mongodb_instance is None:
            await init_db()  # Ensure the DB is initialized
        assert mongodb_instance is not None, "MongoDB instance is not initialized"
        collections[collection_name] = mongodb_instance.get_collection(collection_name)
    return collections[collection_name]

async def close_db():
    """Close the MongoDB connection."""
    global mongodb_instance
    if mongodb_instance:
        mongodb_instance.close()
        print("MongoDB Atlas connection closed")
