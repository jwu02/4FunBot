import discord
from discord.ext import commands
import json
import random

class Quotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add_quote(self, ctx, *, quote):
        with open("quotes.json", "r") as f:
            quotes = json.load(f)

        quote_ids = [quoteObj["quoteId"] for quoteObj in quotes["quotes"]]
        if len(quote_ids) == 0:
            last_quote_id = 0
        else:
            last_quote_id = quote_ids[-1]
        
        quotes["quotes"].append({"quoteId": last_quote_id+1, "quote": quote})

        with open("quotes.json", "w") as f:
            json.dump(quotes, f, indent=4)

        await ctx.send("Quote added.")

    @add_quote.error
    async def add_quote_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Enter a quote after the command!")

    @commands.command()
    async def quote(self, ctx):
        with open("quotes.json", "r") as f:
            quotes = json.load(f)
        
        random_quote = random.choice(quotes["quotes"])
        
        await ctx.send("**Quote "+str(random_quote["quoteId"])+":** "+random_quote["quote"])
    
    @quote.error
    async def quote_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("No quotes has been added.")

    @commands.command()
    async def remove_quote(self, ctx, number):
        with open("quotes.json", "r") as f:
            quotes = json.load(f)

        try:
            number = int(number)

            for quote in quotes["quotes"]:
                if quote["quoteId"] == int(number):
                    removed_quote = quotes["quotes"].pop(quotes["quotes"].index(quote))
                    await ctx.send("Removed "+"quote "+str(removed_quote["quoteId"])+": "+removed_quote["quote"])

                with open("quotes.json", "w") as f:
                    json.dump(quotes, f, indent=4)
        except ValueError:
            await ctx.send("Enter a number for the quote ID.")

    @remove_quote.error
    async def remove_quote_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Enter a quote ID after the command.")

def setup(bot):
    bot.add_cog(Quotes(bot))