import discord
from discord.ext import commands
from PIL import Image, ImageFont, ImageDraw
import os
from io import BytesIO
from Backend.utils import check_permissions
path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets', 'quote')
class Quote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name="quote", description="Quote a message", aliases=["q"])
    async def quote(self, ctx, message_id: int = None, mode: str = "black"):
        if not check_permissions(ctx.author):
            return
            
        if message_id is None:
            if ctx.message.reference:
                message_id = ctx.message.reference.message_id
            else:
                await ctx.send("Please provide a message ID or reply to a message")
                return
                
        try:
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
            
            def get_optimal_font_size(text, max_width, max_height, start_size=36):
                test_size = start_size
                font = ImageFont.truetype(f"{path}/font.otf", test_size)
                
                while test_size > 12:
                    font = ImageFont.truetype(f"{path}/font.otf", test_size)
                    lines = wrap_text(text, font, max_width)
                    total_height = len(lines) * (font.size * 1.2)
                    
                    if total_height <= max_height and max(draw.textlength(line, font=font) for line in lines) <= max_width:
                        break
                    
                    test_size -= 2
                return font

            text_area_width = img_width * 0.6
            text_area_height = img_height * 0.7
            
            # Get avatar with fallback
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
            text_area_width = img_width * 0.6
            text_area_height = img_height * 0.6
            
            font = get_optimal_font_size(message.content, text_area_width, text_area_height)
            small_font = ImageFont.truetype(f"{path}/font.otf", int(font.size * 0.7))
            
            lines = wrap_text(message.content, font, text_area_width)
            
            line_height = font.size * 1.2
            total_height = len(lines) * line_height
            start_y = (img_height - total_height) / 2 - line_height
            
            for i, line in enumerate(lines):
                x_position = img_width * 0.98 - draw.textlength(line, font=font)
                y_position = start_y + (i * line_height)
                draw.text((x_position, y_position), line, fill="white", font=font)
            
            author_text = f"- {message.author.display_name}"
            tag_text = f"@{message.author.name}"
            
            author_x = img_width * 0.98 - draw.textlength(author_text, font=font)
            author_y = start_y + (len(lines) * line_height) + line_height
            
            tag_x = img_width * 0.98 - draw.textlength(tag_text, font=small_font)
            tag_y = author_y + font.size * 1.2
            
            draw.text((author_x, author_y), author_text, fill="white", font=font)
            draw.text((tag_x, tag_y), tag_text, fill="white", font=small_font)
            
            image.save(f"{path}/output.png")
            await ctx.send(file=discord.File(f"{path}/output.png"))
            os.remove(f"{path}/output.png")
        except discord.NotFound:
            await ctx.send("Message not found")
        except Exception as e:
            await ctx.send(f"Error: {str(e)}")

async def setup(bot):
    await bot.add_cog(Quote(bot))