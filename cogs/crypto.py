import discord
from discord.ext import commands
import aiohttp
import time  # <--- New Import

class Crypto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # The Cache: Stores { 'bitcoin': {'price': 96000, 'time': 17000000} }
        self.cache = {} 

    @commands.command()
    async def price(self, ctx, coin_name):
        coin_id = coin_name.lower()
        
        # 1. CHECK CACHE FIRST 🧠
        current_time = time.time()
        if coin_id in self.cache:
            last_price = self.cache[coin_id]['price']
            last_time = self.cache[coin_id]['time']
            
            # If the data is less than 60 seconds old, use it!
            if current_time - last_time < 60:
                # OPTIONAL: Add a footer to say it's cached
                embed = discord.Embed(title=coin_name.capitalize(), color=discord.Color.green())
                embed.add_field(name="Current Price", value=f"${last_price}")
                embed.set_footer(text="Cached data (updated <1 min ago)")
                await ctx.reply(embed=embed)
                return  # <--- STOP HERE, DO NOT CALL API

        # 2. IF NOT IN CACHE, CALL API 📞
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                
                if response.status == 200:
                    data = await response.json()
                    if coin_id not in data:
                        await ctx.reply("I couldn't find that coin! 📉")
                        return
                    
                    coin_price = data[coin_id]['usd']
                    
                    # 3. SAVE TO CACHE 💾
                    self.cache[coin_id] = {
                        'price': coin_price,
                        'time': current_time
                    }
                    
                    embed = discord.Embed(title=coin_name.capitalize(), color=discord.Color.green())
                    embed.add_field(name="Current Price", value=f"${coin_price}")
                    await ctx.reply(embed=embed)

                elif response.status == 429:
                    # If we still hit the limit, apologize
                    await ctx.reply("Traffic is too high! Try again in a minute. 🚦")
                else:
                    await ctx.reply(f"The API is down! (Error: {response.status})")

async def setup(bot):
    await bot.add_cog(Crypto(bot))