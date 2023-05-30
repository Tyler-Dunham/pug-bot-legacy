import discord
from discord.ext import commands
from functions.db import connect_db
import json
from functions.matchmaker import matchmaker
import functions._queue
import time
import random

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
            if ( len(self.tank_queue) + len(self.dps_queue) + len(self.support_queue) ) == 10:
                await ctx.send("10th person has joined and the queue is now closed.\nMatchmaking...\n")

                # End queue, start game
                self.active_queue = False
                self.active_game = True

                # call matchmaker and destructer to get the tank, dps, and support for each team
                team1, team1_average, team2, team2_average, difference = matchmaker(self.tank_queue, self.dps_queue, self.support_queue)
                # display the teams
                await ctx.send(self.display_teams(team1, team2, team1_average, team2_average))

                # Move players to their team's channel 
                await ctx.send("Moving players to voice channels in 5...")
                time.sleep(1)
                for second in range(4, 0, -1):
                    await ctx.send(second + "...")
                    time.sleep(1)
                await ctx.send("Moving players now.")

                guild = self.client.get_guild(ctx.guild.id)
                channel = self.client.get_channel(1107126277971906600) 
                for player in team1:
                    member = guild.get_member(player['_id'])
                    await member.move_to(channel)
                channel = self.client.get_channel(1107126310502932501) 
                for player in team2:
                    member = guild.get_member(player['_id'])
                    await member.move_to(channel)
                
                # Auto-pick a random map
                maps = ["Ilios", "Oasis", "Eichenwalde", "Nepal", "Lijiang Tower", "King's Row", "Dorado", "New Queen's Street", "Midtown", "Gibraltar", "Coloseo", "Esperanca", "Numbani", "Havana", "Antarctic Peninsula", "Circuit Royal", "Ilios"]
                await ctx.send(f"You will be playing on: {random.choice(maps)}. Use `!map` to pick a new map.")

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
    @commands.command(aliases=["close"], brief=": Stops the queue", description="Stop the queue.")
    @commands.has_role("PUG Master")
    async def stop(self, ctx):
        # Close Queue if open
        if self.active_queue == True:
            self.active_queue = False
            await ctx.send("Queue has been stopped.")
        # Queue is already close
        else:
            await ctx.send("There is not an ongoing queue.")


    # Command requires PUG Master role -> admin only
    @commands.command(brief=": End all queue processes", description="Stop all queue related processes and cleanup for the next game.")
    @commands.has_role("PUG Master")
    async def end(self, ctx, winning_team: int):
        # Check if there is actually an ongoing game
        if self.active_game == True:
            # End game
            self.active_game = False

            # move all users that were in the queue back into general voice chat
            guild = self.client.get_guild(ctx.guild.id)
            channel = self.client.get_channel(1107126171285594145) 
            for player in self.tank_queue + self.dps_queue + self.support_queue:
                member = guild.get_member(player['_id'])
                await member.move_to(channel)

            # Clear Queues
            self.tank_queue.clear()
            self.dps_queue.clear()
            self.support_queue.clear()

            # Congratulate Game winner
            if winning_team == 0:
                await ctx.send(f"The game has ended in a draw.")
                return
            else:
                await ctx.send(f"The game has ended. Team {winning_team} wins!")        

        else:
            await ctx.send("There is not an ongoing game.")

# Connect QueueCommands to the bot (client)
async def setup(client):
    await client.add_cog(QueueCommands(client))