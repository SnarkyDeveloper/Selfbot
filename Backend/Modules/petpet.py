import httpx
import discord
from discord.ext import commands
import os
from Backend.send import send
class PetPet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='PetPet a user!')
    async def petpet(self, ctx, user: discord.User = None):
        if not user:
            user = ctx.author
        user = await commands.UserConverter().convert(ctx, user)
        response = httpx.get('https://memeado.vercel.app/api/petpet', params={'image': user.avatar.url})

        if response.status_code == 200:
            with open(f'petpet_{user.id}.gif', 'wb') as f:
                f.write(response.content)
            try:
                await send(self.bot, ctx, title=f'Heh that tickles-', image=f'petpet_{user.id}.gif')
            finally:
                os.remove(f'petpet_{user.id}.gif')
        else:
            await send(self.bot, ctx, title='Error', content='Failed to generate petpet image.', color=0xFF0000)

async def setup(bot):
    await bot.add_cog(PetPet(bot))
