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

    def join_queue(self, role, document):
        # Make sure desired role is open and valid as well as check for duplicate queues
        role = role.lower()
        if (role == "tank"): 
            if (len(self.tank_queue) < 2):
                if not document in (self.tank_queue or self.dps_queue or self.support_queue):
                    self.tank_queue.append(document)
                else:
                    message = "Already in queue. !change <role> to change roles."
                    return message
            else:
                message = "Tank queue full"
                return message
        
        elif (role == "dps"):
            if (len(self.dps_queue) < 4):
                if not document in (self.tank_queue or self.dps_queue or self.support_queue):
                    self.dps_queue.append(document)
                else:
                    message = "Already in queue. !change <role> to change roles."
                    return message
            else:
                message = "DPS queue full"
                return message

        elif (role == "support"):
            if (len(self.support_queue) < 4):
                if not document in (self.tank_queue or self.dps_queue or self.support_queue):
                    self.support_queue.append(document)
                else:
                    message = "Already in queue. !change <role> to change roles."
                    return message
            else:
                message = "Support queue full"
                return message
        # Invalid role was given
        else:
            message = "Please enter a valid role (tank, dps, support)."
            return
        

        message = "Success! You joined the queue."
        return message
            

    def leave_queue(self, document):
        # Find what queue the player is in and leave it.
        if document in self.tank_queue:
            self.tank_queue.remove(document)
        elif document in self.dps_queue:
            self.dps_queue.remove(document)
        elif document in self.support_queue:
            self.support_queue.remove(document)
        # Player is not in queue
        else:
            message = "Not in queue. Join queue with !join <role>"
            return message
        
        message = "Successfully left queue!"
        return message
    
    @commands.command(brief=": Join the PUG Queue", description="Join the PUG Queue with !join <role>")
    async def join(self, ctx, role):
        author = ctx.author

        # Check if user has an account
        document = self.players_collection.find_one({"name": str(author)})
        # User does not have an account
        if not document:
            await ctx.send(f"{author.mention} You do not have an account. Use !create to make one.")
            return
        
        # Join queue and get correct message 
        message = self.join_queue(role, document)
        await ctx.send(f"{author.mention} {message}")  


    @commands.command(brief=": Leave the PUG Queue", description="Join the PUG Queue with !leave")
    async def leave(self, ctx):
        author = ctx.author

        # Check if user has an account
        document = self.players_collection.find_one({"name": str(author)})
        # User does not have an account
        if not document:
            await ctx.send(f"{author.mention} You do not have an account. Use !create to make one.")
            return
        
        # Join queue and get correct message 
        message = self.leave_queue(document)
        await ctx.send(f"{author.mention} {message}") 

    @commands.command(brief=": Change role in the PUG Queue", description="Join the PUG Queue with !change <new_role>")
    async def change(self, ctx, role):
        author = ctx.author

        # Check if user has an account
        document = self.players_collection.find_one({"name": str(author)})
        # User does not have an account
        if not document:
            await ctx.send(f"{author.mention} You do not have an account. Use !create to make one.")
            return
        
        # Leave and rejoin queue
        self.leave_queue(document)
        message = self.join_queue(role, document)
        await ctx.send(f"{author.mention} {message}")
    
    @commands.command(brief=": Check each queue", description="Check each role queue. !join <role> to join the queue!")
    async def check(self, ctx):
        mention = ctx.author.mention

        # Send a message of the current status of each queue
        await ctx.send(f"{mention}\nTank Queue: {len(self.tank_queue)}/2\nDPS Queue: {len(self.dps_queue)}/4\nSupport Queue: {len(self.support_queue)}/4")
    

# Connect ProfileCommands to the bot (client)
async def setup(client):
    await client.add_cog(QueueCommands(client))