from .mongo_db_handler import MongoDBHandler
from dotenv import dotenv_values


class DataAccess:
    def __init__(self, uri, database_name, collection_name):
        self.collection_name = collection_name
        self.db_handler = MongoDBHandler(uri, database_name)

    def create_data(self, data):
        return self.db_handler.create_document(self.collection_name, data)

    def get_data(self, filter_query):
        return self.db_handler.read_document(self.collection_name, filter_query)

    def update_data(self, filter_query, update_data):
        return self.db_handler.update_document(
            self.collection_name, filter_query, update_data
        )

    def delete_data(self, filter_query):
        return self.db_handler.delete_document(self.collection_name, filter_query)
