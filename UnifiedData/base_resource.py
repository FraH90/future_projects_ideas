import uuid
from datetime import datetime
from abc import ABC, abstractmethod

class BaseResource(ABC):
    def __init__(self, name: str, tags=None, metadata=None):
        self.internal_id = uuid.uuid4()                  # Unique identifier for each resource
        self.internal_name = name                        # Name of the resource
        self.created_at = datetime.now()                 # Automatically set on creation
        self.modified_at = datetime.now()                # Automatically update on modification
        self.tags = tags or []                           # Tags (list)
        self.metadata = metadata or {}                   # Metadata (dictionary)
        self.db_manager = None  # Will be set by the orchestrator

    def set_database_manager(self, db_manager):
        """Set the database manager instance."""
        self.db_manager = db_manager


    def save_to_db(self):
        """Save or update the resource representation in the database."""
        if not self.db_manager:
            raise ValueError("DatabaseManager is not set.")
    
        """Save or update the resource representation in the database."""
        data = {
            'internal_id': str(self.internal_id),
            'internal_name': self.internal_name,
            'created_at': self.created_at,
            'modified_at': datetime.now(),
            'tags': self.tags,
            'metadata': self.metadata
        }
        collection.update_one({'internal_id': str(self.internal_id)}, {'$set': data}, upsert=True)
        print(f"Resource '{self.internal_name}' saved to database.")
    
    def load_from_db(self):
        """Load the resource data from the database."""
        if not self.db_manager:
            raise ValueError("DatabaseManager is not set.")
        
        collection = self.db_manager.get_collection('resources')
        document = collection.find_one({'internal_id': str(self.internal_id)})
        if document:
            self.internal_name = document['internal_name']
            self.created_at = document['created_at']
            self.modified_at = document['modified_at']
            self.tags = document['tags']
            self.metadata = document['metadata']
            print(f"Resource '{self.internal_name}' loaded from database.")
        else:
            raise ValueError(f"Resource with ID {self.internal_id} not found in database.")
    
    def delete_from_db(self):
        """Delete the resource representation from the database."""
        if not self.db_manager:
            raise ValueError("DatabaseManager is not set.")
        collection = self.db_manager.get_collection('resources')
        collection.delete_one({'_id': str(self.id)})
        print(f"Resource '{self.name}' deleted from database.")
    
    @abstractmethod
    def save_resource(self, destination: str):
        """Save the actual resource to a specified location."""
        pass
    
    @abstractmethod
    def load_resource(self):
        """Load the actual resource from its location."""
        pass
    
    @abstractmethod
    def delete_resource(self):
        """Delete the actual resource."""
        pass
    
    def add_tag(self, tag: str):
        """Add a tag to the resource."""
        if tag not in self.tags:
            self.tags.append(tag)
        self.modified_at = datetime.now()
        print(f"Tag '{tag}' added to resource '{self.internal_name}'.")

    def remove_tag(self, tag: str):
        """Remove a tag from the resource."""
        if tag in self.tags:
            self.tags.remove(tag)
        self.modified_at = datetime.now()
        print(f"Tag '{tag}' removed from resource '{self.internal_name}'.")
    
    def update_metadata(self, key: str, value):
        """Update the metadata for the resource."""
        self.metadata[key] = value
        self.modified_at = datetime.now()
        print(f"Metadata '{key}' updated for resource '{self.internal_name}'.")

    def get_metadata(self, key: str):
        """Retrieve a value from the metadata."""
        return self.metadata.get(key)
    
    def describe(self):
        """Return a description of the resource, including metadata."""
        description = {
            'internal_id': str(self.internal_id),
            'internal_name': self.internal_name,
            'created_at': self.created_at.isoformat(),
            'modified_at': self.modified_at.isoformat(),
            'tags': self.tags,
            'metadata': self.metadata,
        }
        return description
    
    def __str__(self):
        return f"{self.internal_name} (ID: {self.internal_id})"
