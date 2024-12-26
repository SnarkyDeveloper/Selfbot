import json
import os

def read_users():
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        default_users = {"users": []}
        with open('users.json', 'w') as f:
            json.dump(default_users, f, indent=4)
        return default_users

def check_permissions(bot, user):
    if not os.path.exists('users.json'):
        initial_users = {
            "users": [
                {
                    "id": str(bot.user.id),
                    "name": str(bot.user)
                }
            ]
        }
        with open('users.json', 'w') as f:
            json.dump(initial_users, f, indent=4)
    user_id = user.id if hasattr(user, 'id') else user
    if user_id == bot.user.id or user_id in [user["id"] for user in read_users()["users"]]:
        return True
    if hasattr(user, 'guild') and user.guild.id in [guild["id"] for guild in read_users().get("guilds", [])]:
        return True
    return False 