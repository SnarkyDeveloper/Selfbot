import json
from Backend.bot import bot
import os
path = os.path.dirname(os.path.dirname(__file__))
def read_messages():
    try:
        with open(f'{path}/data/messages/messages.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"messages": []}

def write_messages(data):
    try:
        with open(f'{path}/data/messages/messages.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"Error writing to messages file: {e}")

@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return
    user = message.author
    messages_data = read_messages()
    messages_data["messages"].append({
            "user": str(user),
            "message": message.content,
            "type": "delete",
            "server": message.guild.id if message.guild else 'DM'
    })
    write_messages(messages_data)

@bot.event
async def on_message_edit(before, after):
    if before.author.bot:
        return
    messages_data = read_messages()
    messages_data["messages"].append({
        "user": str(before.author),
        "message_before": before.content,
        "message_after": after.content,
        "type": "edit",
        "server": before.guild.id if before.guild else 'DM',
        "message_link": f"https://discord.com/channels/{before.guild.id if before.guild else '@me'}/{before.channel.id}/{before.id}"
    })
    write_messages(messages_data)

