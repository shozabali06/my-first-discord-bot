import discord
from discord.ext import commands
import aiohttp # <--- The new library
import asyncio

class Jokes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def joke(self, ctx):
        # 1. Start a session (like opening a browser tab)
        async with aiohttp.ClientSession() as session:
            # 2. Go to the URL
            async with session.get('https://official-joke-api.appspot.com/random_joke') as response:
                
                # 3. Check if the website is working (Status 200 means OK)
                if response.status == 200:
                    # 4. Get the data as JSON
                    data = await response.json()
                    
                    # --- YOUR CODE GOES HERE ---
                    # The 'data' variable is now a dictionary. 
                    # It looks like this: 
                    # {"setup": "Why did the chicken...", "punchline": "...to cross the road"}
                    
                    # Challenge: Can you get the setup and punchline 
                    # and send them to the channel?
                    
                    # Helper Hint:
                    # setup = data["setup"]
                    # punchline = data["punchline"]

                    setup = data["setup"]
                    punchline = data["punchline"]

                    await ctx.reply(f"{setup}")
                    await asyncio.sleep(3)  # Pause before the 
                    await ctx.reply(f"{punchline}")
                    
                else:
                    await ctx.reply("The joke factory is currently broken! 🛠️")

async def setup(bot):
    await bot.add_cog(Jokes(bot))