from pymongo import MongoClient

class DatabaseManager:
    def __init__(self, uri: str = 'mongodb://localhost:27017/', db_name: str = 'resource_database'):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self._setup_collections()
        
    def _setup_collections(self):
        """Set up necessary collections in the database."""
        self.collections = {
            'resources': self.db.resources
        }
        print(f"Database '{self.db.name}' setup with collections: {list(self.collections.keys())}")

    def get_collection(self, name: str):
        """Get a specific collection."""
        if name in self.collections:
            return self.collections[name]
        raise ValueError(f"Collection '{name}' does not exist.")
    
    def close(self):
        """Close the database connection."""
        self.client.close()
        print("Database connection closed.")
