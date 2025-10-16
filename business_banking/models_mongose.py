from pymongo import MongoClient
import bcrypt
from bson.objectid import ObjectId

# Replace with your MongoDB URI
MONGO_URI = "mongodb://localhost:27017/"

client = MongoClient(MONGO_URI)
db = client['straive']  # Use your database name here
users_collection = db['users']


def init_db():
    # Drops existing collection if any
    users_collection.drop()
    # MongoDB creates collection automatically when inserting data
    print("Database initialized (users collection dropped)")


# def insert_user(user):
#     # Insert or replace by UserID (upsert)
#     users_collection.update_one(
#         {"UserID": user['UserID']},
#         {"$set": user},
#         upsert=True
#     )
def insert_user(user):
    # Hash the password before inserting
    if 'Password' in user:
        # bcrypt expects bytes, so encode string
        hashed_pw = bcrypt.hashpw(user['Password'].encode('utf-8'), bcrypt.gensalt())
        # Store hashed password as a decoded string (utf-8)
        user['Password'] = hashed_pw.decode('utf-8')

    # Insert or replace by UserID (upsert)
    users_collection.update_one(
        {"UserID": user['UserID']},
        {"$set": user},
        upsert=True
    )



def get_user_by_id(user_id):
    user = users_collection.find_one({"UserID": user_id}, {"_id": 0})
    return user


# def get_user_by_credentials(user_id, password):
#     user = users_collection.find_one({"UserID": user_id, "Password": password}, {"_id": 0})
#     if user:
#         print("User found:", user)
#     else:
#         print("No user found with given credentials.")
#     return user

def get_user_by_credentials(user_id, password):
    user = users_collection.find_one({"UserID": user_id}, {"_id": 0})

    if user:
        hashed_pw = user.get('Password')
        if hashed_pw and bcrypt.checkpw(password.encode('utf-8'), hashed_pw.encode('utf-8')):
            print("User found:", user)
            return user
        else:
            print("Password mismatch for user:", user_id)
            return None
    else:
        print("No user found with given credentials.")
        return None



def get_user_by_name(name):
    user = users_collection.find_one({"UserName": name}, {"_id": 0})
    return user


def get_all_users():
    users = list(users_collection.find({}, {"_id": 0}))
    return users


def update_pan_tan(user_id, pan=None, tan=None):
    update_fields = {}
    if pan is not None:
        update_fields['PAN'] = pan
    if tan is not None:
        update_fields['TAN'] = tan

    if not update_fields:
        return False  # nothing to update

    result = users_collection.update_one(
        {"UserID": user_id},
        {"$set": update_fields}
    )
    return result.modified_count > 0


def delete_user_by_id(user_id):
    result = users_collection.delete_one({"UserID": user_id})
    return result.deleted_count > 0

def update_balance(user_id, amount_delta):
    result = users_collection.update_one(
        {"UserID": user_id},
        {"$inc": {"Balance": amount_delta}}
    )
    return result.modified_count > 0

def update_user(user_id, update_fields):
    # from your_app import mongo  # or however you imported it

    result = users_collection.update_one(
        {"UserID": user_id},
        {"$set": update_fields}
    )
    return result.modified_count > 0

