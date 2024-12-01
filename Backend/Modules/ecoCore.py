import json
import os
from datetime import datetime
from contextlib import contextmanager
import asyncio

def read_eco():
    try:
        with open('data/economy/eco.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        # Initialize with empty structure if file doesn't exist
        default_data = {"users": []}
        write_eco(default_data)
        return default_data

def write_eco(data):
    # Ensure directory exists
    os.makedirs('data/economy', exist_ok=True)
    with open('data/economy/eco.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

class Economy:
    def __init__(self, bot):
        self.bot = bot
        self.lock = asyncio.Lock()
        self.setup()

    def setup(self):
        os.makedirs("data/economy", exist_ok=True)
        # Initialize file if it doesn't exist
        if not os.path.exists("data/economy/eco.json"):
            write_eco({"users": []})
    
    def get_cooldown(self, user_id, cooldown_type):
        """Get the timestamp of the last cooldown action for a user"""
        data = read_eco()
        for entry in data["users"]:
            if entry["user"] == str(user_id):
                return entry.get(cooldown_type, 0)  # Returns 0 if cooldown doesn't exist
        return 0

    def get_balance(self, user_id):
        data = read_eco()
        for entry in data["users"]:
            if entry["user"] == str(user_id):
                return entry["balance"]
        return 0

    def user_exists(self, user_id):
        data = read_eco()
        for entry in data["users"]:
            if entry["user"] == str(user_id):
                return True
                
        user_entry = {
            "user": str(user_id),
            "balance": 0,
            "last_daily": 0,
            "last_work": 0,
            "last_steal": 0,
            "last_stripper": 0,
            "last_mafia": 0
        }
        data["users"].append(user_entry)
        write_eco(data)
        return False

    def add_balance(self, user_id, amount):
        data = read_eco()
        for entry in data["users"]:
            if entry["user"] == str(user_id):
                entry["balance"] += amount
                write_eco(data)
                return
        self.user_exists(user_id)
        self.add_balance(user_id, amount)
    def remove_balance(self, user_id, amount):
        data = read_eco()
        for entry in data["users"]:
            if entry["user"] == str(user_id):
                entry["balance"] = max(0, entry["balance"] - amount)  # Prevent negative balance
                write_eco(data)
                return
        self.user_exists(user_id)
        self.remove_balance(user_id, amount)

    async def daily(self, user_id):
        data = read_eco()
        for entry in data["users"]:
            if entry["user"] == str(user_id):
                entry["last_daily"] = datetime.now().timestamp()
                write_eco(data)
                return
        self.user_exists(user_id)
        await self.daily(user_id)

    def work(self, user_id):
        data = read_eco()
        for entry in data["users"]:
            if entry["user"] == str(user_id):
                entry["last_work"] = datetime.now().timestamp()
                write_eco(data)
                return
        self.user_exists(user_id)
        self.work(user_id)

    def steal(self, thief_id, target_id, amount):
        data = read_eco()
        thief_found = False
        target_found = False
        
        for entry in data["users"]:
            if entry["user"] == str(thief_id):
                entry["last_steal"] = datetime.now().timestamp()
                entry["balance"] += amount
                thief_found = True
            elif entry["user"] == str(target_id):
                entry["balance"] = max(0, entry["balance"] - amount)
                target_found = True
                
            if thief_found and target_found:
                write_eco(data)
                return

        if not thief_found:
            self.user_exists(thief_id)
        if not target_found:
            self.user_exists(target_id)
        self.steal(thief_id, target_id, amount)

    def leaderboard(self, limit=10):
        data = read_eco()
        # Sort users by balance in descending order
        sorted_users = sorted(data["users"], key=lambda x: x["balance"], reverse=True)
        return sorted_users[:limit]

    def read_eco(self):
        return read_eco()

    def write_eco(self, data):
        write_eco(data)

async def setup(bot):
    eco_cog = Economy(bot)
    eco_cmd = eco_cog.eco_cmd
    eco_cmd.name = "eco"
    bot.eco.add_command(eco_cmd)
    await bot.add_cog(eco_cog)
