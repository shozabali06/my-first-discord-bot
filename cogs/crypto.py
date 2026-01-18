import discord
from discord.ext import commands
import aiohttp

class Crypto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def price(self, ctx, coin_name):
        # API requires lowercase (e.g., 'Bitcoin' -> 'bitcoin')
        coin_id = coin_name.lower()
        
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    
                    # ERROR CHECK: If the coin name is wrong, the dictionary is empty: {}
                    if coin_id not in data:
                        await ctx.reply("I couldn't find that coin! 📉")
                        return

                    # --- YOUR CODE HERE ---
                    # The data looks like: {'bitcoin': {'usd': 96500}}
                    # 1. Dig into 'data' to get the USD price.
                    # 2. Send a message: "The price of bitcoin is $96500"

                    coin_price = data[coin_name]['usd']

                    await ctx.reply(f'The prrice of {coin_name} is ${coin_price}')
                    
                    
                else:
                    await ctx.reply("The API is currently down! 🔌")

async def setup(bot):
    await bot.add_cog(Crypto(bot))