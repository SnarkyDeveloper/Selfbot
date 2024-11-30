import json
import os

def read_users():
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Create default users file if it doesn't exist
        default_users = {"users": []}
        with open('users.json', 'w') as f:
            json.dump(default_users, f, indent=4)
        return default_users

def check_permissions(bot, user):
    user_id = user.id if hasattr(user, 'id') else user
    if user_id == bot.user.id or user_id in [user["id"] for user in read_users()["users"]]:
        return True
    return False 