import discord
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw
import os
from io import BytesIO
from Backend.send import send
path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets', 'quote')
class Quote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name="quote", description="Quote a message", aliases=["q"])
    async def quote(self, ctx, message_id: int = None, mode: str = "black"):         
        if message_id is None:
            if ctx.message.reference:
                message_id = ctx.message.reference.message_id
            else:
                await ctx.send("Please provide a message ID or reply to a message")
                return
                
        try:
            async with ctx.typing():
                message = await ctx.fetch_message(message_id)
                author_name = message.author.name
                image = Image.open(f"{path}/{mode}.png")
                font = ImageFont.truetype(f"{path}/font.otf", 36)
                draw = ImageDraw.Draw(image)
                
                img_width, img_height = image.size
                
                def wrap_text(text, font, max_width):
                    lines = []
                    words = text.split()
                    current_line = []
                    
                    for word in words:
                        test_line = current_line + [word]
                        line_width = draw.textlength(' '.join(test_line), font=font)
                        
                        if line_width <= max_width:
                            current_line.append(word)
                        else:
                            if current_line:
                                lines.append(' '.join(current_line))
                            current_line = [word]
                    
                    if current_line:
                        lines.append(' '.join(current_line))
                    return lines
                
                def get_optimal_font_size(text, max_width, max_height, min_size=12, start_size=36):
                    test_size = start_size
                    while test_size > min_size:
                        font = ImageFont.truetype(f"{path}/font.otf", test_size)
                        lines = wrap_text(text, font, max_width)
                        total_height = len(lines) * (font.size * 1.2)
                        max_line_width = max(draw.textlength(line, font=font) for line in lines)
                        
                        if (total_height <= max_height and 
                            max_line_width <= max_width):
                            return font, lines
                        
                        test_size -= 2
                    
                    font = ImageFont.truetype(f"{path}/font.otf", min_size)
                    return font, wrap_text(text, font, max_width)

                if message.author.avatar:
                    avatar_data = await message.author.avatar.read()
                    avatar_image = Image.open(BytesIO(avatar_data))
                else:
                    avatar_image = Image.open(f"{path}/default_pfp.png")
                
                image = Image.open(f"{path}/{mode}.png").convert('RGBA')
                img_width, img_height = image.size
                
                avatar_width = int(img_height * 1.05)
                avatar_height = img_height
                avatar_image = avatar_image.resize((avatar_width, avatar_height), Image.Resampling.LANCZOS)
                
                mask = Image.new('L', (avatar_width, avatar_height), 255)
                mask_draw = ImageDraw.Draw(mask)
                
                for y in range(avatar_height):
                    for x in range(avatar_width):
                        distance = (x + y) / 2
                        opacity = 255 - int(255 * (distance / (avatar_width + avatar_height) * 1.5))
                        opacity = max(0, min(255, opacity))
                        mask_draw.point((x, y), fill=opacity)
                
                avatar_x = 0
                avatar_y = 0
                image.paste(avatar_image, (avatar_x, avatar_y), mask)
                
                draw = ImageDraw.Draw(image)
                min_x_position = avatar_width + 40
                max_x_position = img_width - 40
                text_area_width = max_x_position - min_x_position
                text_area_height = img_height * 0.7
                
                content = message.content.encode("ascii", errors="ignore").decode()
                for user in message.mentions:
                    content = content.replace(f"@{user.name}", f"@{user.display_name}")
                
                font, lines = get_optimal_font_size(
                    content, 
                    text_area_width,
                    text_area_height
                )
                
                line_height = font.size * 1.2
                total_height = len(lines) * line_height
                start_y = (img_height - total_height) / 2 - line_height

                for i, line in enumerate(lines):
                    y_position = start_y + (i * line_height)
                    draw.text((min_x_position, y_position), line, fill="white", font=font)

                author_text = f"- {message.author.display_name}"
                tag_text = f"@{message.author.name}"
                
                author_y = start_y + (len(lines) * line_height) + line_height
                tag_y = author_y + font.size * 1.2

                author_font = ImageFont.truetype(f"{path}/font.otf", int(font.size * 0.8))
                small_font = ImageFont.truetype(f"{path}/font.otf", int(font.size * 0.6))

                author_width = draw.textlength(author_text, font=author_font)
                tag_width = draw.textlength(tag_text, font=small_font)
                
                if min_x_position + max(author_width, tag_width) > max_x_position:
                    author_font = ImageFont.truetype(f"{path}/font.otf", int(font.size * 0.6))
                    small_font = ImageFont.truetype(f"{path}/font.otf", int(font.size * 0.4))
                
                draw.text((min_x_position, author_y), author_text, fill="white", font=author_font)
                draw.text((min_x_position, tag_y), tag_text, fill="white", font=small_font)
                
                image.save(f"{path}/output.png")
                
            try:
                await send(self.bot, ctx, title=f"Quote by {author_name}", image=f"{path}/output.png")
            finally:
                if os.path.exists(f"{path}/output.png"):
                    os.remove(f"{path}/output.png")
        except discord.NotFound:
            await ctx.send("Message not found")
        except Exception as e:
            await ctx.send(f"Error: {str(e)}")

async def setup(bot):
    await bot.add_cog(Quote(bot))