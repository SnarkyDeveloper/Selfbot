import discord
from discord.ext import commands
import sympy
from sympy.abc import x, y, z
from Backend.send import send
class Calculator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='calc', description='Calculate mathematical expressions')
    async def calculate(self, ctx, expression):
        try:
            expression = expression.replace('^', '**')

            safe_dict = {"x": x, "y": y, "z": z}
            result = sympy.sympify(expression, locals=safe_dict)

            simplified = sympy.simplify(result)

            try:
                numeric_result = float(simplified.evalf())
                if numeric_result.is_integer():
                    await send(self.bot, ctx, title="Result", content=f"{int(numeric_result)}", color=0x2ECC71)
                else:
                    await send(self.bot, ctx, title="Result", content=f"{numeric_result}", color=0x2ECC71)
            except:
                await send(self.bot, ctx, title="Result", content=f"{simplified}", color=0x2ECC71)

        except sympy.SympifyError:
            await send(self.bot, ctx, title="Calculator Error", content="Error: Invalid mathematical expression.", color=0xff0000)
        except Exception as e:
            await send(self.bot, ctx, title="Calculator Error", content=f"Error: {str(e)}", color=0xff0000)


async def setup(bot):
    await bot.add_cog(Calculator(bot))