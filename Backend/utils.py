import json
from discord.ext import commands
import os
path = os.path.dirname(os.path.dirname(__file__))
if os.path.exists(f'{path}/data/users/users.json'):
    pass
else:
    with open(f'{path}/data/users/users.json', 'w') as file:
        json.dump({"users": []}, file, indent=4)
class CommandHelper:
    """Helper class for command operations"""
    def __init__(self, ctx):
        self.ctx = ctx
    
    async def send(self, message):
        """Send a message to the channel where the command was invoked"""
        channel = self.ctx.message.channel
        await channel.send(message)

def read_users():
    """Read the users.json file containing allowed users"""
    try:
        with open(f'{path}/data/users/users.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"users": []}
    except IOError as e:
        print(f"Error reading users file: {e}")

def write_users(data):
    """Write to the users.json file"""
    with open(f'{path}/data/users/users.json', 'w') as file:
        json.dump(data, file, indent=4)

def check_permissions(user):
    """Check if a user has permission to use bot commands"""
    user_id = user.id if hasattr(user, 'id') else user
    # Convert all IDs to strings for comparison
    user_id_str = str(user_id)
    allowed_ids = [str(user["id"]) for user in read_users()["users"]]
    
    if user_id_str in allowed_ids:
        return True
    return False

def read_messages():
    """Read the messages.json file containing message history"""
    try:
        with open(f'{path}/data/messages/messages.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"messages": []}

def write_messages(data):
    """Write to the messages.json file"""
    with open(f'{path}/data/messages/messages.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)