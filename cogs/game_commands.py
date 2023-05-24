import random
import discord
from discord.ext import commands
from db import connect_db
import json

class GameCommands(commands.Cog):
    with open('KEYS.json', 'r') as f:
        data = json.load(f)

    # Initialize ProfileCommands
    def __init__(self, client):
        self.client = client
        self.db = connect_db(self.data)
        self.players_collection = self.db["players"]
    
    @commands.command()
    async def map(self, ctx):
        maps = ["Ilios", "Oasis", "Eichenwalde", "Nepal", "Lijiang Tower", "King's Row", "Dorado", "New Queen's Street", "Midtown", "Gibraltar", "Coloseo", "Esperanca", "Numbani", "Havana", "Antarctic Peninsula", "Circuit Royal", "Ilios"]
        decide = random.randint(0,len(maps)-1)
        await ctx.send("You will be playing on: " + maps[decide])

    @commands.command()
    async def bruh(self, ctx):
        await ctx.send("bruh")

    @commands.command()
    async def moogagod(self, ctx):
        await ctx.send("Leo is a corrupt businessman. He repeatedly lies on his taxes and makes illegal deals with overseas companies. However, he goes around loudly accusing other people of corruption and illegal dealings. According to Freud, Leo is dealing with his anxiety about his own bad behavior through which defense mechanism?")
    
    

# Connect ProfileCommands to the bot (client)
async def setup(client):
    await client.add_cog(GameCommands(client))
