from pymongo import MongoClient

def connect_db(data):
	CONNECTION_STRING = data['DB_CONN_STRING']
	# Create an instance of the mongo client
	client = MongoClient(CONNECTION_STRING)
	# Get the database
	db = client.get_database("pugs")
	return db