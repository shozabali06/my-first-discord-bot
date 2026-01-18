import discord
from discord.ext import commands
import json
import random

class Economy(commands.Cog):
    shop_items = {
        "watch": 100,
        "laptop": 500,
        "mansion": 10000
    }

    def __init__(self, bot):
        self.bot = bot

    # We will add our helper functions here
    def load_data(self):
        with open('bank.json', 'r') as f:
            users = json.load(f)
        return users
    
    def save_data(self, users):
        with open('bank.json', 'w') as f:
            json.dump(users, f)

    @commands.command()
    async def balance(self, ctx):
        # loading data
        users = self.load_data()

        # checking if user is available
        user_id = str(ctx.author.id)

        if user_id not in users:
            users[user_id] = {"balance": 100}
            self.save_data(users)
        
        balance = users[user_id]["balance"]
        await ctx.reply(f'Your balance is {balance} coins.')

    @commands.command()
    async def beg(self, ctx):
        users = self.load_data()
        user_id = str(ctx.author.id)

        if user_id not in users:
            users[user_id] = {"balance": 100}
            self.save_data(users)
            await ctx.reply(f"Welcome new user, here's is your welcome bonus. 100 coins")
        
        users[user_id]["balance"] += random.randint(1, 20)
        self.save_data(users)
        await ctx.reply(f'You begged and received some coins! Your new balance is {users[user_id]["balance"]} coins.')

    @commands.command()
    async def shop(self, ctx):
        menu = ""
        for item, price in self.shop_items.items():
            menu += f"{item} : {price} coins\n"
        
        await ctx.reply(menu)

    @commands.command()
    async def buy(self, ctx, item_name):
        users = self.load_data()
        if str(ctx.author.id) not in users:
            await ctx.reply("You don't have an account. Type !balance to create an account.")
            return

        if item_name not in self.shop_items:
            await ctx.reply(f"{item_name} is not available.")
            return
        
        item_price = self.shop_items[item_name]
        
        if users[str(ctx.author.id)]["balance"] < item_price:
            await ctx.reply("You do not have sufficient balance to buy this item.")
            return
        
        users[str(ctx.author.id)]["balance"] -= item_price
        self.save_data(users)

        await ctx.reply(f"You have bought {item_name}")

async def setup(bot):
    await bot.add_cog(Economy(bot))