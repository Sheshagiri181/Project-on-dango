import os
from pymongo import MongoClient

def get_db():
    # Use environment variables for credentials
    mongo_uri = os.getenv('MONGO_URI', 'mongodb+srv://gshesha181:Sheshu!123@cluster0.iwh6fjg.mongodb.net/')
    try:
        client = MongoClient(mongo_uri)
        students = client['aagama_pr_1']['student']
        return students
    except Exception as e:
        print(f"Database connection error: {e}")
        return None