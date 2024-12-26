import discord
from discord.ext import commands
from ollama import chat
from ollama import ChatResponse
import asyncio
import concurrent.futures
from diffusers import StableDiffusionPipeline
import os
import torch
from torch.amp import autocast

torch.backends.cudnn.benchmark = True
torch.backends.cudnn.enabled = True

async def loading(ctx, interval=0.5, type="text"):
    if type == "image":
        x = await ctx.send("Generating image... This may take a while. You'll be notified when it's done.")
    else:
        x = await ctx.send("Generating response...")
    load = await ctx.send("**↺**")
    try:
        while True:
            await load.edit(content="**↺**")
            await asyncio.sleep(interval)
            await load.edit(content="**⟲**") 
            await asyncio.sleep(interval)
    finally:
        await x.delete()
        await load.delete()

class Ollama(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pipeline = StableDiffusionPipeline.from_pretrained(
            "stabilityai/stable-diffusion-2-1",
            torch_dtype=torch.float16
        )
        
        self.pipeline.enable_model_cpu_offload()
        self.pipeline.enable_vae_slicing()
        torch.cuda.empty_cache()

    @commands.command(description="Ask an AI a question")
    async def ask(self, ctx, question):
        loading_message = await ctx.send("Generating response...")
        load_symbol = await ctx.send("**↺**")
        
        try:
            while_loading = True

            async def animate_loading():
                while while_loading:
                    await load_symbol.edit(content="**↺**")
                    await asyncio.sleep(0.5)
                    if not while_loading: break
                    await load_symbol.edit(content="**⟲**")
                    await asyncio.sleep(0.5)
            
            loading_task = asyncio.create_task(animate_loading())
            
            with concurrent.futures.ThreadPoolExecutor() as pool:
                response = await asyncio.get_event_loop().run_in_executor(
                    pool,
                    lambda: chat(
                        model='llama3.2',
                        messages=[{'role': 'user', 'content': question}],
                        stream=True
                    )
                )
                
                while_loading = False
                await loading_task
                await loading_message.delete()
                await load_symbol.delete()
                
                full_response = ""
                current_message = await ctx.send("_ _")
                
                for chunk in response:
                    if chunk and 'message' in chunk and 'content' in chunk['message']:
                        content = chunk['message']['content']
                        full_response += content
                        
                        if len(full_response) >= 1900:
                            try:
                                await current_message.edit(content=full_response)
                                full_response = ""
                                current_message = await ctx.send("_ _")
                            except discord.HTTPException:
                                current_message = await ctx.send(full_response)
                                full_response = ""
                        elif len(full_response) % 250 < len(content):
                            try:
                                await current_message.edit(content=full_response)
                            except discord.HTTPException:
                                current_message = await ctx.send(full_response)
                                full_response = ""
                
                if full_response:
                    try:
                        await current_message.edit(content=full_response)
                    except discord.HTTPException:
                        await ctx.send(full_response)        
        except Exception as e:
            while_loading = False
            await loading_message.delete()
            await load_symbol.delete()
            await ctx.send(f"An error occurred: {str(e)}")

    @commands.command(description="Generate an image", aliases=["img", "imagine"])
    async def generate(self, ctx, prompt):
        loading_message = await ctx.send("Generating image... This may take a while. You'll be notified when it's done.")
        load_symbol = await ctx.send("**↺**")
        
        try:
            while_loading = True

            async def animate_loading():
                while while_loading:
                    await load_symbol.edit(content="**↺**")
                    await asyncio.sleep(0.5)
                    if not while_loading: break
                    await load_symbol.edit(content="**⟲**")
                    await asyncio.sleep(0.5)
            
            loading_task = asyncio.create_task(animate_loading())
            
            with concurrent.futures.ThreadPoolExecutor() as pool:
                try:
                    with autocast('cuda'):
                        image = await asyncio.get_event_loop().run_in_executor(
                            pool,
                            lambda: self.pipeline(
                                prompt,
                                num_inference_steps=15
                            ).images[0]
                        )
                except torch.cuda.OutOfMemoryError:
                    print("Not enough GPU memory. Trying CPU fallback.")
                    self.pipeline.to('cpu')
                while_loading = False
                await loading_task
                await loading_message.delete()
                await load_symbol.delete()
                
                image.save(f'{ctx.author.id}.png')
                message = await ctx.send(file=discord.File(f'{ctx.author.id}.png'))
                await message.reply(f'{prompt} | Generated by {ctx.author.mention}')
                os.remove(f'{ctx.author.id}.png')
                torch.cuda.empty_cache()
                
        except Exception as e:
            while_loading = False
            await loading_message.delete()
            await load_symbol.delete()
            await ctx.send(f"An error occurred: {str(e)}")

async def setup(bot):
    await bot.add_cog(Ollama(bot))
