def connect_db(data):
	from pymongo import MongoClient

	CONNECTION_STRING = data['DB_CONN_STRING']
	# Create an instance of the mongo client
	client = MongoClient(CONNECTION_STRING)
	# Get the database
	db = client.get_database("pugs")
	# Get players collection
	players_collection = db["players"]