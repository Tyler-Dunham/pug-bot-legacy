import discord
from discord.ext import commands
from db import connect_db
import json

class QueueCommands(commands.Cog):
    with open('KEYS.json', 'r') as f:
        data = json.load(f)

    # Initialize ProfileCommands
    def __init__(self, client):
        self.client = client
        self.db = connect_db(self.data)
        self.players_collection = self.db["players"]
        self.tank_queue = []
        self.dps_queue = []
        self.support_queue = []
    
    @commands.command()
    async def join(self, ctx, role):
        author = ctx.author

    @commands.command()
    async def leave(self, ctx):
        pass

    @commands.command()
    async def change(self, ctx):
        pass


        


# Connect ProfileCommands to the bot (client)
async def setup(client):
    await client.add_cog(QueueCommands(client))