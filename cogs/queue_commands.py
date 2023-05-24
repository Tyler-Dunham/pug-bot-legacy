import random
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
    
    @commands.command(brief=": Join the PUG Queue", description="Join the PUG Queue with !join <role>")
    async def join(self, ctx, role):
        pass

    @commands.command(brief=": Leave the PUG Queue", description="Join the PUG Queue with !leave")
    async def leave(self, ctx):
        pass

    @commands.command(brief=": Change role in the PUG Queue", description="Join the PUG Queue with !change <new_role>")
    async def change(self, ctx, role):
       pass
    

# Connect ProfileCommands to the bot (client)
async def setup(client):
    await client.add_cog(QueueCommands(client))