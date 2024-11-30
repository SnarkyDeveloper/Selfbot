from discord.ext import commands
from Backend.utils import check_permissions, read_users, write_users

class perms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Add a user to the allowed list')
    async def add(self, ctx, user_mention: str):
        if int(ctx.author.id) != int(self.bot.user.id):
            await ctx.send("You are not allowed to use this command")
            return
        
        user_id = user_mention.strip('<@!>')
        users_data = read_users()
        users_data["users"].append({
            "id": str(user_id),
            "name": f"User_{user_id}"
        })
        write_users(users_data)
        await ctx.send(f'Added user with ID: {user_id}')

    @commands.command(description='Removes a user from allowed list')
    async def remove(self, ctx, user_mention: str):
        if int(ctx.author.id) != int(self.bot.user.id):
            if not check_permissions(ctx.author):
                return
            await ctx.send("You are not allowed to use this command")
        
        user_id = user_mention.strip('<@!>')
        users_data = read_users()
        users_data["users"] = [u for u in users_data["users"] if u["id"] != str(user_id)]
        write_users(users_data)
        await ctx.send(f'Removed user with ID: {user_id}')

async def setup(bot):
    await bot.add_cog(perms(bot))