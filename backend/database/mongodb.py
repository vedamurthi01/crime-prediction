from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure, PyMongoError
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class MongoDB:
    """MongoDB database handler for crime prediction system"""
    
    def __init__(self, uri, db_name):
        """Initialize MongoDB connection"""
        self.uri = uri
        self.db_name = db_name
        self.client = None
        self.db = None
        
    def connect(self):
        """Establish connection to MongoDB"""
        try:
            self.client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
            # Test connection
            self.client.admin.command('ping')
            self.db = self.client[self.db_name]
            self._create_indexes()
            logger.info(f"Successfully connected to MongoDB: {self.db_name}")
            return True
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error connecting to MongoDB: {e}")
            return False
    
    def _create_indexes(self):
        """Create indexes for optimized queries"""
        try:
            crime_collection = self.db.crime_records
            
            # Create indexes
            crime_collection.create_index([("crime_id", ASCENDING)], unique=True)
            crime_collection.create_index([("crime_type", ASCENDING)])
            crime_collection.create_index([("location", ASCENDING)])
            crime_collection.create_index([("date", DESCENDING)])
            crime_collection.create_index([("district", ASCENDING)])
            
            logger.info("Database indexes created successfully")
        except Exception as e:
            logger.warning(f"Error creating indexes: {e}")
    
    def insert_crime_record(self, record):
        """Insert a single crime record"""
        try:
            collection = self.db.crime_records
            result = collection.insert_one(record)
            return result.inserted_id
        except PyMongoError as e:
            logger.error(f"Error inserting record: {e}")
            return None
    
    def insert_many_records(self, records):
        """Insert multiple crime records"""
        try:
            collection = self.db.crime_records
            result = collection.insert_many(records, ordered=False)
            return len(result.inserted_ids)
        except PyMongoError as e:
            logger.error(f"Error inserting records: {e}")
            return 0
    
    def get_all_records(self, limit=None):
        """Retrieve all crime records"""
        try:
            collection = self.db.crime_records
            query = collection.find()
            if limit:
                query = query.limit(limit)
            return list(query)
        except PyMongoError as e:
            logger.error(f"Error retrieving records: {e}")
            return []
    
    def get_record_by_id(self, crime_id):
        """Get a specific crime record by ID"""
        try:
            collection = self.db.crime_records
            return collection.find_one({"crime_id": crime_id})
        except PyMongoError as e:
            logger.error(f"Error retrieving record: {e}")
            return None
    
    def get_records_by_crime_type(self, crime_type):
        """Get all records for a specific crime type"""
        try:
            collection = self.db.crime_records
            return list(collection.find({"crime_type": crime_type}))
        except PyMongoError as e:
            logger.error(f"Error retrieving records: {e}")
            return []
    
    def get_records_by_location(self, location):
        """Get all records for a specific location"""
        try:
            collection = self.db.crime_records
            return list(collection.find({"location": location}))
        except PyMongoError as e:
            logger.error(f"Error retrieving records: {e}")
            return []
    
    def get_crime_statistics(self):
        """Get aggregated crime statistics"""
        try:
            collection = self.db.crime_records
            
            # Total crimes
            total_crimes = collection.count_documents({})
            
            # Crime by type
            crime_by_type = list(collection.aggregate([
                {"$group": {"_id": "$crime_type", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}}
            ]))
            
            # Crime by location
            crime_by_location = list(collection.aggregate([
                {"$group": {"_id": "$location", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$limit": 10}
            ]))
            
            # Crime by district
            crime_by_district = list(collection.aggregate([
                {"$group": {"_id": "$district", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}}
            ]))
            
            return {
                "total_crimes": total_crimes,
                "crime_by_type": crime_by_type,
                "crime_by_location": crime_by_location,
                "crime_by_district": crime_by_district
            }
        except PyMongoError as e:
            logger.error(f"Error retrieving statistics: {e}")
            return {}
    
    def update_record(self, crime_id, update_data):
        """Update a crime record"""
        try:
            collection = self.db.crime_records
            result = collection.update_one(
                {"crime_id": crime_id},
                {"$set": update_data}
            )
            return result.modified_count
        except PyMongoError as e:
            logger.error(f"Error updating record: {e}")
            return 0
    
    def delete_record(self, crime_id):
        """Delete a crime record"""
        try:
            collection = self.db.crime_records
            result = collection.delete_one({"crime_id": crime_id})
            return result.deleted_count
        except PyMongoError as e:
            logger.error(f"Error deleting record: {e}")
            return 0
    
    def clear_collection(self, collection_name="crime_records"):
        """Clear all documents from a collection"""
        try:
            collection = self.db[collection_name]
            result = collection.delete_many({})
            logger.info(f"Cleared {result.deleted_count} documents from {collection_name}")
            return result.deleted_count
        except PyMongoError as e:
            logger.error(f"Error clearing collection: {e}")
            return 0
    
    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")

# Singleton instance
_db_instance = None

def get_db(uri=None, db_name=None):
    """Get or create MongoDB instance"""
    global _db_instance
    if _db_instance is None and uri and db_name:
        _db_instance = MongoDB(uri, db_name)
    return _db_instance
