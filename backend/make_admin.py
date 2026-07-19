from pymongo import MongoClient
import certifi

MONGODB_URI = "mongodb+srv://jaypanchal202223_db_user:IEmFQhGZf20s2vQG@cluster0.cdebbwz.mongodb.net/?appName=Cluster0"
DATABASE_NAME = "dealership"

client = MongoClient(MONGODB_URI, tlsCAFile=certifi.where())
db = client[DATABASE_NAME]

email = "jayincubyte@gmail.com"  # your actual login email

result = db.users.update_one({"email": email}, {"$set": {"role": "admin"}})
print("Matched:", result.matched_count, "Modified:", result.modified_count)
for u in db.users.find({}, {"email": 1, "role": 1}):
       print(u)

user = db.users.find_one({"email": email})
print("Current role:", user["role"] if user else "USER NOT FOUND")

print(db.list_collection_names())
print(db.users.count_documents({}))

from pathlib import Path
print(Path(__file__).resolve().parent.parent.parent / ".env")

