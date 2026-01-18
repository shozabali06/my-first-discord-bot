import discord
from discord.ext import commands
import asyncio

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # -- We will move your commands here --
    def get_polite_msg(self, name):
        return f"Greetings, {name}"
    
    @commands.command()
    async def greet(self, ctx):
        await ctx.reply("What is your name?")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await self.bot.wait_for('message', check=check, timeout=10)
            name = msg.content
            await ctx.reply(self.get_polite_msg(name))
        except asyncio.TimeoutError:
            await ctx.reply("You took too long to reply!")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.system_channel is not None:
            await member.guild.system_channel.send(f"Welcome to the server, {member.mention}!")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        await message.channel.send(f"A message was deleted: {message.content}")


async def setup(bot):
    await bot.add_cog(Greetings(bot))