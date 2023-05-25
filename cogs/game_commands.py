import random
import discord
from discord.ext import commands
from functions.db import connect_db
import json

class GameCommands(commands.Cog):
    with open('KEYS.json', 'r') as f:
        data = json.load(f)

    # Initialize GameCommands
    def __init__(self, client):
        self.client = client
        self.db = connect_db(self.data)
        self.players_collection = self.db["players"]
    
    @commands.command()
    async def map(self, ctx):
        maps = ["Ilios", "Oasis", "Eichenwalde", "Nepal", "Lijiang Tower", "King's Row", "Dorado", "New Queen's Street", "Midtown", "Gibraltar", "Coloseo", "Esperanca", "Numbani", "Havana", "Antarctic Peninsula", "Circuit Royal", "Ilios"]
        await ctx.send("You will be playing on: " + random.choice(maps))

    @commands.command()
    async def bruh(self, ctx):
        await ctx.send("bruh")

    @commands.command()
    async def moogagod(self, ctx):
        await ctx.send("Leo is a corrupt businessman. He repeatedly lies on his taxes and makes illegal deals with overseas companies. However, he goes around loudly accusing other people of corruption and illegal dealings. According to Freud, Leo is dealing with his anxiety about his own bad behavior through which defense mechanism?")

    @commands.command()
    async def wins(self, ctx, user: str= commands.parameter(default=None, description=": Discord tag to search")):
        if user is None:
            user_to_find = str(ctx.author)
        # If a user is specified, search for the specified user
        else:
            user_to_find = user
        
        # Look for document with the given name
        document = self.players_collection.find_one({"name": user_to_find})
        # Check if no document was found
        if not document:
            # User is the author AND no account in the database
            if user is None:
                await ctx.send("You don't have an account. Use !create to make one, or !help create for further instruction.")
                return
            
            await ctx.send("We couldn't find an account with that name.")
            return

        await ctx.send(f"Wins: {document['num_wins']}")
    
    @commands.command()
    async def losses(self, ctx, user: str= commands.parameter(default=None, description=": Discord tag to search")):
        if user is None:
            user_to_find = str(ctx.author)
        # If a user is specified, search for the specified user
        else:
            user_to_find = user
        
        # Look for document with the given name
        document = self.players_collection.find_one({"name": user_to_find})
        # Check if no document was found
        if not document:
            # User is the author AND no account in the database
            if user is None:
                await ctx.send("You don't have an account. Use !create to make one, or !help create for further instruction.")
                return
            
            await ctx.send("We couldn't find an account with that name.")
            return

        await ctx.send(f"Losses: {document['num_losses']}")

    @commands.command()
    async def winrate(self, ctx, user: str= commands.parameter(default=None, description=": Discord tag to search")):
        if user is None:
            user_to_find = str(ctx.author)
        # If a user is specified, search for the specified user
        else:
            user_to_find = user
        
        # Look for document with the given name
        document = self.players_collection.find_one({"name": user_to_find})
        # Check if no document was found
        if not document:
            # User is the author AND no account in the database
            if user is None:
                await ctx.send("You don't have an account. Use !create to make one, or !help create for further instruction.")
                return
            
            await ctx.send("We couldn't find an account with that name.")
            return
        
        if document['num_wins'] == 0:
            await ctx.send("Your winrate is 0%")
            return
        
        if document['num_losses'] == 0:
            await ctx.send("Your winrate is 100%")
            return
   
        
        rate = float(document['num_wins'] / (document['num_wins'] + document['num_losses'])) * 100

        await ctx.send("Your winrate is " + rate + ".")
    

# Connect GameCommands to the bot (client)
async def setup(client):
    await client.add_cog(GameCommands(client))
