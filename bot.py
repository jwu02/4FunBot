import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()
bot_token = os.getenv("BOT_TOKEN")

bot = commands.Bot("!", case_insensitive=True)

@bot.event
async def on_ready():
    print("Bot is ready.")
    await bot.change_presence(activity=discord.Game("with code"))

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong {round(bot.latency * 1000)}ms")

@bot.command()
async def reload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")
    bot.load_extension(f"cogs.{extension}")

# for cogs
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(bot_token)