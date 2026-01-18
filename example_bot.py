from discord.ext import commands
import discord
import random
import asyncio
import os 
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

async def load_extensions():
    await bot.load_extension('cogs.greetings')
    await bot.load_extension('cogs.economy')
    await bot.load_extension('cogs.confirmation')
    await bot.load_extension('cogs.jokes')
    await bot.load_extension('cogs.crypto')

bot.setup_hook = load_extensions

@bot.event
async def on_ready():
    print(f'We have logged as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.reply('Hello')

@bot.command()
async def say(ctx, *, input):
    await ctx.reply(input)

@bot.command()
async def roll(ctx, sides: int):
    number = random.randint(1, sides)
    await ctx.reply(f'You rolled a {number}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.reply("Please enter a valid number!")

@bot.command()
async def info(ctx):
    embed = discord.Embed(title='Bot Info', description='my cool bot', color=discord.Color.blue())
    embed.add_field(name='Creator', value='Shozab', inline=False)
    embed.add_field(name='Version', value='1.0.0', inline=True)
    embed.add_field(name='Server Count', value=len(bot.guilds), inline=True)
    await ctx.reply(embed=embed)

@bot.command()
async def pic(ctx):
    picture = discord.File("minecraft_sheep.jpg")

    await ctx.reply(file=picture)

token = os.getenv('DISCORD_TOKEN')
if token is None:
    raise ValueError("DISCORD_TOKEN environment variable is not set")
bot.run(token)