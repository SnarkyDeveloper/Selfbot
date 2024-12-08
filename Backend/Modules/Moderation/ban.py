import discord
import discord.ext.commands as commands
from Backend.utils import check_permissions, write_punishment, read_punishment
class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(description="Ban a user from the server")
    async def ban(self, ctx, user: discord.Member, *, reason=None):
        if not check_permissions(ctx.author):
            return
        punishment_data = read_punishment()
        punishment_data["users"].append({
            "id": str(user.user_id),
            "Reason": reason,
            "Type": "Ban"
        })
        await user.kick(reason=reason)
        write_punishment(punishment_data)
        await ctx.send(f"Kicked {user.mention}")
async def setup(bot):
    ban = Ban(bot)
    ban_cmd = ban.ban_cmd
    ban_cmd.name = "kick"
    bot.moderation.add_command(ban_cmd)
    await bot.add_cog(Ban)