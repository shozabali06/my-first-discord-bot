from discord.ext import commands

class Confirmation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def confirm(self, ctx):
        msg = await ctx.reply("Are you sure?")

        msg.add_reaction("✅")
        msg.add_reaction("❌")

        def check(reaction, user):
            return user == ctx.author and reaction.message.id == msg.id
    
        reaction, user = await self.bot.wait_for('reaction_add', check=check)

        if reaction.emoji == '✅':
            await ctx.reply("Confirmed!")
        else:
            await ctx.reply("Cancelled!")

async def setup(bot):
    await bot.add_cog(Confirmation(bot))