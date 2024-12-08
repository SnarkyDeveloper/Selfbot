import discord
import discord.ext.commands as commands
from Backend.utils import check_permissions, write_punishment, read_punishment
class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(description="Kick a user from the server")
    async def kick(self, ctx, user: discord.Member, *, reason=None):
        if not check_permissions(ctx.author):
            return
        punishment_data = read_punishment()
        punishment_data["users"].append({
            "id": str(user.user_id),
            "Reason": reason,
            "Type": "Kick"
        })
        await user.kick(reason=reason)
        write_punishment(punishment_data)
        await ctx.send(f"Kicked {user.mention}")
async def setup(bot):
    Kick = Kick(bot)
    kick_cmd = Kick.kick_cmd
    kick_cmd.name = "kick"
    bot.moderation.add_command(kick_cmd)
    await bot.add_cog(Kick)