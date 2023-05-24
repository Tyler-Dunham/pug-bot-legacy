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
    async def pong(self, ctx):
        await ctx.send("pong")


# Connect ProfileCommands to the bot (client)
async def setup(client):
    await client.add_cog(GameCommands(client))
