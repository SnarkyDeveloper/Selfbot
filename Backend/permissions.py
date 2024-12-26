import json
import os

path = os.path.dirname(os.path.dirname(__file__))

def read_users():
    try:
        with open(f'{path}/data/users/users.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        default_users = {"users": [], "guilds": []}
        with open(f'{path}/data/users/users.json', 'w') as f:
            json.dump(default_users, f, indent=4)
        return default_users
def check_permissions(bot, message):
    if not os.path.exists('users.json'):
        initial_users = {
            "users": [
                {
                    "id": str(bot.user.id),
                    "name": str(bot.user)
                }
            ],
            "guilds": []
        }
        with open('users.json', 'w') as f:
            json.dump(initial_users, f, indent=4)

    user_id = message.author.id
    users_data = read_users()
    if str(user_id) in [str(user["id"]) for user in users_data["users"]]:
        return True
        
    if message.guild:
        if str(message.guild.id) in [str(guild["id"]) for guild in users_data.get("guilds", [])]:
            return True
            
    return False

