import discord
from discord.ext import commands
import random
from mysql.connector import MySQLConnection, Error
from kaz_bot_mysql_dbconfig import read_db_config

class Quotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def add_quote(self, ctx, *, quote):
        try:
            dbconfig = read_db_config()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()

            query = """INSERT INTO quotes (quote, added_by) VALUES (%s, %s)"""
            args = (quote, ctx.author.name+"#"+ctx.author.discriminator)
            cursor.execute(query, args)

            conn.commit()
            await ctx.send("Quote added.")

        except Error as e:
            print(e)
            await ctx.send("Internal server error encountered.")

        finally:
            cursor.close()
            conn.close()

    @add_quote.error
    async def add_quote_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Enter a quote after the command!")

    @commands.command()
    async def quote(self, ctx, quote_id=None):
        if quote_id:
            try:
                quote_id = int(quote_id)

                dbconfig = read_db_config()
                conn = MySQLConnection(**dbconfig)
                cursor = conn.cursor()

                query = """SELECT * FROM quotes WHERE quote_id=%s"""
                # require comma if single arg? to make args a tuple
                args = (quote_id,)
                cursor.execute(query, args)

                # fetch the next row in the result set
                row = cursor.fetchone()

                if row is not None:
                    quote_id = row[0]
                    quote = row[1]
                    await ctx.send(f'**Quote {str(quote_id)}:** {quote}')
                else:
                    await ctx.send("No quote with given ID was found.")

            except ValueError:
                await ctx.send("Enter a number for the quote ID.")

            except Error as e:
                print(e)
                await ctx.send("Internal server error encountered.")

            finally:
                cursor.close()
                conn.close()

        else:
            try: 
                dbconfig = read_db_config()
                conn = MySQLConnection(**dbconfig)
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM quotes ORDER BY RAND() LIMIT 1')

                # fetch the next row in the result set
                row = cursor.fetchone()
                
                quote_id = row[0]
                quote = row[1]
                await ctx.send(f'**Quote {str(quote_id)}:** {quote}')
            
            except Error as e:
                print(e)
                await ctx.send("Internal server error encountered.")

            finally:
                cursor.close()
                conn.close()

    @quote.error
    async def quote_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("No quotes has been added.")

    @commands.command()
    async def remove_quote(self, ctx, quote_id):
        try:
            quote_id = int(quote_id)

            dbconfig = read_db_config()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()

            query = """SELECT * FROM quotes WHERE quote_id=%s"""
            # require comma if single arg? to make args a tuple
            args = (quote_id,)
            cursor.execute(query, args)
            row = cursor.fetchone()

            if row is not None:
                query = """DELETE FROM quotes WHERE quote_id=%s"""
                cursor.execute(query, args)

                conn.commit()
                await ctx.send(f"Removed quote {str(row[0])}: {row[1]}")
            else:
                await ctx.send("No quote with given ID was found.")

        except ValueError:
            await ctx.send("Enter a number for the quote ID.")

        except Error as e:
            print(e)
            await ctx.send("Internal server error encountered.")

        finally:
            cursor.close()
            conn.close()

    @remove_quote.error
    async def remove_quote_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Enter a quote ID after the command.")

    @commands.command()
    async def update_quote(self, ctx, quote_id, *, new_quote):
        try:
            quote_id = int(quote_id)

            dbconfig = read_db_config()
            conn = MySQLConnection(**dbconfig)
            cursor = conn.cursor()

            query = """SELECT * FROM quotes 
                       WHERE quote_id = %s"""
            args1 = (quote_id,)
            cursor.execute(query, args1)
            row = cursor.fetchone()

            if row is not None:
                query = """UPDATE quotes
                        SET quote = %s
                        WHERE quote_id = %s"""
                args2 = (new_quote, quote_id)
                cursor.execute(query, args2)

                conn.commit()
                await ctx.send(f"Quote {quote_id} has been updated successfully to: {new_quote}")
            else:
                await ctx.send("No quote with given ID was found.")

        except ValueError:
            await ctx.send("Enter a number for the quote ID.")
        
        except Error as e:
            print(e)
            await ctx.send("Internal server error encountered.")

        finally:
            cursor.close()
            conn.close()

    @update_quote.error
    async def update_quote_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Enter a quote ID and a quote after the command.")

def setup(bot):
    bot.add_cog(Quotes(bot))