import discord
from discord.ext import commands
from db import connect_db
import json

#Profile commands 
class ProfileCommands(commands.Cog):
    with open('KEYS.json', 'r') as f:
        data = json.load(f)
        connect_db(data)

    # Initialize ProfileCommands
    def __init__(self, client):
        self.client = client

    # Command for users to create accounts on our database
    #TODO: Insert these values (tank, dps, support, id, author) to database under profile in profile collection
    @commands.command()
    async def create(self, ctx, tank_elo: int, dps_elo: int, support_elo: int):
        author = ctx.author
        author_id = ctx.author.id
        await ctx.send(f"Tank: {tank_elo} | Dps: {dps_elo} | Support: {support_elo}")

    # Command for users to update accounts on our database
    #TODO: Update these values in the database under desired profile
    @commands.command()
    async def update(self, ctx, role: str, elo: int):
        author_id = ctx.author.id # For database search purposes, ctx.author works as well but id is unique
        await ctx.send(f"New {role} sr: {elo}")

    # Command for users to view accounts on our database
    #TODO: Search the database for the designated user and display desired info (tank, dps, support elo for now)
    @commands.command()
    async def view(self, ctx, user: str=None):
        # Handles no parameters auto searching for ctx.author
        if user is None:
            user_to_find = ctx.author
        # If a user is specified, search for the specified user
        else:
            user_to_find = user

        await ctx.send(f"Searching for {user_to_find}...")

    

# Connect ProfileCommands to the bot (client)
async def setup(client):
    await client.add_cog(ProfileCommands(client))