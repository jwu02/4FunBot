import discord
from discord.ext import commands
import os

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

bot.run("Nzk4MTY2MTA0MDY1MDQ4NTc3.X_xEHA.zNZoWy7WjN1LaF14c0SZqcaPkC8")