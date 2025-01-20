from discord.ext import commands
from Backend.utils import read_users, write_users, read_settings
from Backend.send import send
class perms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.owner_id = int(read_settings()["main"]["owner_id"])

    @commands.command(description='Add a user to the allowed list')
    async def adduser(self, ctx, user_mention: str):
        if int(ctx.author.id) == int(self.bot.user.id) or int(ctx.author.id) == self.owner_id:
            user = await commands.UserConverter().convert(ctx, user_mention)
            users_data = read_users()
            if user_mention in [u["id"] for u in users_data["users"]]:
                await send(self.bot, ctx, title='Error', content=f'User already whitelisted!', color=0xff0000)
                return
            users_data["users"].append({
                "id": str(user.id),
                "name": f"{user.name}"
            })
            write_users(users_data)
            await send(self.bot, ctx, title='Success', content=f'Added user with ID: {user.id}', color=0x2ECC71)
        else:
            await send(self.bot, ctx, title='Error', content="You are not allowed to use this command", color=0xff0000)

    @commands.command(description='Removes a user from allowed list')
    async def removeuser(self, ctx, user_mention: str):
        if int(ctx.author.id) == int(self.bot.user.id) or int(ctx.author.id) == self.owner_id:
            user_id = user_mention.strip('<@!>')
            users_data = read_users()
            if user_mention in [u["id"] for u in users_data["users"]]:
                users_data["users"] = [u for u in users_data["users"] if u["id"] != str(user_id)]
                write_users(users_data)
                await send(self.bot, ctx, title='Success', content=f'Removed user with ID: {user_id}', color=0xE74C3C)
            else:
                await send(self.bot, ctx, title='Error', content=f'User not whitelisted!', color=0xff0000)
        else:
            await send(self.bot, ctx, title='Error', content="You are not allowed to use this command", color=0xff0000)
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
            await send(self.bot, ctx, title='Success', content=f'Added server with ID: {ctx.guild.id}', color=0x2ECC71)
        else:
            await send(self.bot, ctx, title='Error', content="You are not allowed to use this command", color=0xff0000)
    @commands.command(description='Removes a server from allowed list')
    async def removeserver(self, ctx):
        if int(ctx.author.id) == int(self.bot.user.id) or int(ctx.author.id) == self.owner_id:
            users_data = read_users()
            if "guilds" in users_data:
                users_data["guilds"] = [g for g in users_data["guilds"] if g["id"] != ctx.guild.id]
                write_users(users_data)
                await send(self.bot, ctx, title='Success', content=f'Removed server with ID: {ctx.guild.id}', color=0xE74C3C)
            else:
                await send(self.bot, ctx, title='Error', content=f'Server not whitelisted!', color=0xff0000)
        else:
            await send(self.bot, ctx, title='Error', content="You are not allowed to use this command", color=0xff0000)

async def setup(bot):
    await bot.add_cog(perms(bot))

