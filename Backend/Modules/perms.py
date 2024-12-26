from discord.ext import commands
from Backend.utils import check_permissions, read_users, write_users, read_settings

class perms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.owner_id = int(read_settings()["main"]["owner_id"])

    @commands.command(description='Add a user to the allowed list')
    async def adduser(self, ctx, user_mention: str):
        if int(ctx.author.id) == int(self.bot.user.id) or int(ctx.author.id) == self.owner_id:
            user_id = user_mention.strip('<@!>')
            users_data = read_users()
            if user_mention in [u["id"] for u in users_data["users"]]:
                await ctx.send(f'User already whitelisted!')
                return
            users_data["users"].append({
                "id": str(user_id),
                "name": f"User_{user_id}"
            })
            write_users(users_data)
            await ctx.send(f'Added user with ID: {user_id}')
        else:
            await ctx.send("You are not allowed to use this command")

    @commands.command(description='Removes a user from allowed list')
    async def removeuser(self, ctx, user_mention: str):
        if int(ctx.author.id) == int(self.bot.user.id) or int(ctx.author.id) == self.owner_id:
            user_id = user_mention.strip('<@!>')
            users_data = read_users()
            if user_mention in [u["id"] for u in users_data["users"]]:
                users_data["users"] = [u for u in users_data["users"] if u["id"] != str(user_id)]
                write_users(users_data)
                await ctx.send(f'Removed user with ID: {user_id}')
            else:
                await ctx.send(f'User not whitelisted!')
        else:
            if not check_permissions(ctx.author):
                await ctx.send("You are not allowed to use this command")
                return
    @commands.command(description='Whitelists entire server')
    async def addserver(self, ctx):
        if int(ctx.author.id) == int(self.bot.user.id) or int(ctx.author.id) == self.owner_id:
            users_data = read_users()
            if "guilds" not in users_data:
                users_data["guilds"] = []
            users_data["guilds"].append({
                "id": ctx.guild.id,
                "name": ctx.guild.name
            })
            write_users(users_data)
            await ctx.send(f'Whitelisted server: {ctx.guild.name}')
        else:
            await ctx.send("You are not allowed to use this command")
    @commands.command(description='Removes a server from allowed list')
    async def removeserver(self, ctx):
        if int(ctx.author.id) == int(self.bot.user.id) or int(ctx.author.id) == self.owner_id:
            users_data = read_users()
            if "guilds" in users_data:
                users_data["guilds"] = [g for g in users_data["guilds"] if g["id"] != ctx.guild.id]
                write_users(users_data)
                await ctx.send(f'Removed server: {ctx.guild.name}')
            else:
                await ctx.send(f'Server not whitelisted!')
        else:
            await ctx.send("You are not allowed to use this command")

async def setup(bot):
    await bot.add_cog(perms(bot))

