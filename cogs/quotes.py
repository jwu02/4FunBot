import discord
from discord.ext import commands
import random

class Quotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add_quote(self, ctx, *, quote):
        with open("quotes.json", "r") as f:
            quotes = json.load(f)

        quote_ids = [quoteObj['quoteId'] for quoteObj in quotes['quotes']]
        if len(quote_ids) == 0:
            last_quote_id = 0
        else:
            last_quote_id = quote_ids[-1]
        
        quotes['quotes'].append({'quoteId': last_quote_id+1, 'quote': quote})

        with open("quotes.json", "w") as f:
            json.dump(quotes, f, indent=4)

        await ctx.send("Quote added.")

    @add_quote.error
    async def add_quote_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Enter a quote after the command!")

    @commands.command()
    async def quote(self, ctx, quote_id=None):
        if quote_id:
            with open("quotes.json", "r") as f:
                quotes = json.load(f)
            
            try:
                quote_id = int(quote_id)
                
                get_quote = None
                for quote in quotes['quotes']:
                    if quote['quoteId'] == quote_id:
                        get_quote = quote['quote']
                        await ctx.send(f"**Quote {quote['quoteId']}:** {quote['quote']}")
                        break

                if not get_quote:
                    await ctx.send("No quote with given ID was found.")
            except ValueError:
                await ctx.send("Enter a number for the quote ID.")
        else:
            with open("quotes.json", "r") as f:
                quotes = json.load(f)
            
            random_quote = random.choice(quotes['quotes'])
            
            await ctx.send(f"**Quote {str(random_quote['quoteId'])}:** {random_quote['quote']}")
    
    @quote.error
    async def quote_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("No quotes has been added.")

    @commands.command()
    async def remove_quote(self, ctx, quote_id):
        with open("quotes.json", "r") as f:
            quotes = json.load(f)

        try:
            quote_id = int(quote_id)

            removed_quote = None
            for quote in quotes['quotes']:
                if quote['quoteId'] == quote_id:
                    removed_quote = quotes['quotes'].pop(quotes['quotes'].index(quote))
                    await ctx.send(f"Removed quote {str(removed_quote['quoteId'])}: {removed_quote['quote']}")
                    break

            with open("quotes.json", "w") as f:
                json.dump(quotes, f, indent=4)

            if not removed_quote:
                await ctx.send("No quote with given ID was found.")
        except ValueError:
            await ctx.send("Enter a number for the quote ID.")

    @remove_quote.error
    async def remove_quote_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Enter a quote ID after the command.")

    @commands.command()
    async def update_quote(self, ctx, quote_id, *, new_quote):
        with open("quotes.json", "r") as f:
            quotes = json.load(f)
        
        try:
            quote_id = int(quote_id)

            updated = False
            for quote in quotes['quotes']:
                if quote['quoteId'] == quote_id:
                    quote['quote'] = new_quote
                    updated = True
                    break
            
            with open("quotes.json", "w") as f:
                json.dump(quotes, f, indent=4)

            if updated:
                await ctx.send(f"Quote {quote_id} has been updated successfully to {new_quote}")
            else:
                await ctx.send("No quote with given ID was found.")
        except ValueError:
            await ctx.send("Enter a number for the quote ID.")

    @update_quote.error
    async def update_quote_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Enter a quote ID and a quote after the command.")

def setup(bot):
    bot.add_cog(Quotes(bot))