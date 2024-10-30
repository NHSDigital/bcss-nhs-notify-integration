from pymongo import MongoClient


class MongoDBHandler:
    def __init__(self, uri: str, db_name: str):
        # Connect to MongoDB
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def create_document(self, collection_name, data):
        # Insert a document into the specified collection
        collection = self.db[collection_name]
        result = collection.insert_one(data)
        return result.inserted_id

    def read_document(self, collection_name, query={}):
        # Find documents in the specified collection based on a query
        collection = self.db[collection_name]
        return list(collection.find(query))

    def update_document(self, collection_name, query, update_data):
        # Update a document in the specified collection
        collection = self.db[collection_name]
        result = collection.update_one(query, {"$set": update_data})
        return result.matched_count

    def delete_document(self, collection_name, query):
        # Delete a document from the specified collection
        collection = self.db[collection_name]
        result = collection.delete_one(query)
        return result.deleted_count
