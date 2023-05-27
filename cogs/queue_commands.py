import discord
from discord.ext import commands
from functions.db import connect_db
import json
from functions.matchmaker import mm_first_draft
import functions._queue

class QueueCommands(commands.Cog, functions._queue.QueueMixin):
    with open('KEYS.json', 'r') as f:
        data = json.load(f)

    # Initialize QueueCommands
    def __init__(self, client):
        self.client = client
        self.db = connect_db(self.data)
        self.players_collection = self.db["players"]

        self.tank_queue = []
        self.dps_queue = []
        self.support_queue = []

        self.active_queue = False
        self.active_game = False

    @commands.command(brief=": Join the PUG Queue", description="Join the PUG Queue with !join <role>")
    async def join(self, ctx, role):
        """
        It is important to note this join command also handles 
        automayically starting the matchmaker when the queue is filled.
        """
        if self.active_queue:
            author = ctx.author

            # Check if user has an account
            document = self.players_collection.find_one({"name": str(author)})
            # User does not have an account
            if not document:
                await ctx.send(f"{author.mention} You do not have an account. Use `!create` to make one.")
                return
            
            # Join queue and get correct message 
            message = self.join_queue(role, document)
            await ctx.send(f"{author.mention} {message}")  

            # Check if queue is filled from most recent join 
            if ( len(self.tank_queue) + len(self.dps_queue) + len(self.support_queue) ) == 1:
                await ctx.send("Matchmaking has started. Queue is closing and matchmaking will begin shortly.")

                # End queue, start game
                self.active_queue = False
                self.active_game = True

                # TODO: Call display_teams(). This function both calls and displays mm_draft()
                # TODO: Move people to their team's channel 
                # TODO: Auto-pick a random map

        else:
            await ctx.send("Queue is not active. Only PUG Masters can start a queue!")


    @commands.command(brief=": Leave the PUG Queue", description="Join the PUG Queue with !leave")
    async def leave(self, ctx):
        if self.active_queue:
            author = ctx.author

            # Check if user has an account
            document = self.players_collection.find_one({"name": str(author)})
            # User does not have an account
            if not document:
                await ctx.send(f"{author.mention} You do not have an account. Use `!create` to make one.")
                return
            
            # Join queue and get correct message 
            message = self.leave_queue(document)
            await ctx.send(f"{author.mention} {message}") 

        else:
            await ctx.send("Queue is not active. Only PUG Masters can start a queue!")

    @commands.command(brief=": Change role in the PUG Queue", description="Join the PUG Queue with !change <new_role>")
    async def change(self, ctx, role):
        if self.active_queue:
            author = ctx.author

            # Check if user has an account
            document = self.players_collection.find_one({"name": str(author)})
            # User does not have an account
            if not document:
                await ctx.send(f"{author.mention} You do not have an account. Use `!create` to make one.")
                return
            
            # Leave and rejoin queue
            self.leave_queue(document)
            message = self.join_queue(role, document)
            await ctx.send(f"{author.mention} {message}")
        else:
            await ctx.send("Queue is not active. Only PUG Masters can start a queue!")
    
    @commands.command(aliases=["status"], brief=": Check each queue", description="Check each role queue. !join <role> to join the queue!")
    async def check(self, ctx):
        # Check if there is an ongoing queue
        if self.active_queue:
            mention = ctx.author.mention

            # Send a message of the current status of each queue
            await ctx.send(f"{mention}\nPlayers queued for each role:\n```Tank:      {len(self.tank_queue)}/2\nDPS:       {len(self.dps_queue)}/4\nSupport:   {len(self.support_queue)}/4```")

        else:
            await ctx.send("Queue is not active. Only PUG Masters can start a queue!")


    # Command requires PUG Master role -> admin only
    @commands.command(aliases=["open"], brief=": Start the queue", description="Start the queue and allow matchmaking to begin automatically.")
    @commands.has_role("PUG Master")
    async def start(self, ctx):
        # Open Queue if closed
        if self.active_queue == False:
            self.active_queue = True
            await ctx.send("Queue has been started.\nJoin with `!join <role>`\nChange roles with `!change <new_role>`\nLeave the queue with `!leave.`")
        # Queue is already open
        else:
            await ctx.send("There is already an ongoing queue.")


    # Command requires PUG Master role -> admin only
    @commands.command(brief=": End all queue processes", description="Stop all queue related processes and cleanup for the next game.")
    @commands.has_role("PUG Master")
    async def end(self, ctx, winning_team: int):
        # Check if there is actually an ongoing game
        if self.active_game == True:
            # End game
            self.active_game = False

            # Clear Queues
            self.tank_queue.clear()
            self.dps_queue.clear()
            self.support_queue.clear()

            # Congratulate Game winner
            if winning_team == 0:
                await ctx.send(f"The game has ended in a draw.")
            else:
                await ctx.send(f"The game has ended. Team {winning_team} wins!")        

        #TODO: update all elos (+25 for winning team, -25 for losing team)
        #TODO: move users back to #Draft channel
        #TODO: cleanup (clear queues)
        
        else:
            await ctx.send("There is not an ongoing game.")
            return

# Connect QueueCommands to the bot (client)
async def setup(client):
    await client.add_cog(QueueCommands(client))