import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from pymongo.errors import BulkWriteError

#get the .env variables
load_dotenv()

#gets the variables from .env
MONGO_URL = os.getenv('MONGODB_URL')
MONGODB_DB = os.getenv('MONGODB_DB')

#start the connection and select the database
client = MongoClient(MONGO_URL, server_api=ServerApi('1'))
db = client[MONGODB_DB]

if not client:
    raise ValueError("No MongoDB connection")

#get the collections
notifications = db['notifications']
user_profiles = db['user_profiles']
silver_data = db['silver_data']
gold_data = db['gold_data']

def create_indexes():
    notifications.create_index("url", unique=True)
    silver_data.create_index("url", unique=True)
    gold_data.create_index([("profile_id", 1), ("url", 1)], unique=True)
    user_profiles.create_index("user_id")

def insert_many_silver(data_list):
    try:
        silver_data.insert_many(data_list, ordered=False)
    except BulkWriteError:
        print("BulkWriteError: Duplicate URLs detected and ignored.")


def get_silver_jobs(limit=10):
    return list(silver_data.find().sort("scraped_at", -1).limit(limit))


def upsert_gold_job(scored_job):
    gold_data.replace_one(
        {
            "profile_id": scored_job["profile_id"],
            "url": scored_job["url"],
        },
        scored_job,
        upsert=True,
    )


def get_top_gold_jobs(profile_id, limit=5):
    return list(
        gold_data.find({"profile_id": profile_id})
        .sort("ai_score", -1)
        .limit(limit)
    )


create_indexes()
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)
