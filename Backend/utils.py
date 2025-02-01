import json
from discord.ext import commands
import os
path = os.path.dirname(os.path.dirname(__file__))
if os.path.exists(f'{path}/data/users/users.json'):
    pass
else:
    with open(f'{path}/data/users/users.json', 'w') as file:
        json.dump({"users": []}, file, indent=4)
if os.path.exists(f'{path}/data/punishments/punishments.json'):
    pass
else:
    with open(f'{path}/data/punishments/punishments.json', 'w') as file:
        json.dump({"punishments": []}, file, indent=4)

def read_users():
    try:
        with open(f'{path}/data/users/users.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"users": []}
    except IOError as e:
        print(f"Error reading users file: {e}")

def write_users(data):
    with open(f'{path}/data/users/users.json', 'w') as file:
        json.dump(data, file, indent=4)

def read_messages():
    try:
        with open(f'{path}/data/messages/messages.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"messages": []}

def write_messages(data):
    with open(f'{path}/data/messages/messages.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        
def write_punishments(data):
    with open(f'{path}/data/punishments/punishments.json', 'w') as file:
        json.dump(data, file, indent=4)
def read_punishments():
    try:
        with open(f'{path}/data/punishments/punishments.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"punishments": []}
    
def read_settings():
    try:
        with open(f'{path}/settings.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"settings": []}
async def is_owner(ctx):
    id = int(ctx.author.id)
    data = read_settings().get('main')
    if id == ctx.bot.owner_id or id == ctx.bot.user.id:
        return True 
    if data.get('owner_id') is None:
        return False
    elif int(data.get('owner_id')) != id:
        return False
    return True