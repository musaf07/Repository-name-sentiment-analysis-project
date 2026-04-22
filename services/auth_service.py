from database.connection import users_collection

def register_user(user):
    users_collection.insert_one(user)
    return {"message": "User registered"}