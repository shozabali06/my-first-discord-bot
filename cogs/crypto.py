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

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                print(f"Status Code: {response.status}")
                if response.status == 200:
                    data = await response.json()
                    
                    # ERROR CHECK: If the coin name is wrong, the dictionary is empty: {}
                    if coin_id not in data:
                        await ctx.reply("I couldn't find that coin! 📉")
                        return

                    embed = discord.Embed(
                        title="Bitcoin Price", 
                        description="Current market value", 
                        color=discord.Color.gold()
                    )
                    embed.add_field(name="Price (USD)", value="$96,500")
                    await ctx.send(embed=embed)  

                elif response.status == 429:
                    await ctx.reply("Whoa, slow down! We hit the rate limit. ⏳")
                elif response.status == 403:
                    await ctx.reply("CoinGecko blocked us! 🛡️")
                else:
                    await ctx.reply(f"The API is down! (Error: {response.status})")

async def setup(bot):
    await bot.add_cog(Crypto(bot))