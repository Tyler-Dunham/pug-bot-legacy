import discord
from discord.ext import commands
from db import connect_db
import json

#Profile commands 
class ProfileCommands(commands.Cog):
    with open('KEYS.json', 'r') as f:
        data = json.load(f)

    # Initialize ProfileCommands
    def __init__(self, client):
        self.client = client
        self.db = connect_db(self.data)
        self.players_collection = self.db["players"]

    def check_valid_elo(self, elos: list):
        new_elos = []

        # Check if elo is in range
        for elo in elos:
            if (elo) not in range(0, 5001):          
                return None
            # Finalize elos in new_elos (Default elos if 0)
            elo = elo if elo != 0 else 2500
            new_elos.append(elo)
        
        return new_elos
      


    # Command for users to create accounts on our database
    @commands.command(brief=": Create your profile", description="Create your profile with !create <tank_elo> <dps_elo> <support_elo>")
    async def create(self, ctx, tank_elo: int = commands.parameter(description=": Your tank elo"), 
                     dps_elo: int = commands.parameter(description=": Your dps elo"), 
                     support_elo: int= commands.parameter(description=": Your support elo")):
        author = str(ctx.author)
        author_id = ctx.author.id

        # Check if document with this name already exists 
        document = self.players_collection.find_one({"name": author})
        if document:
            await ctx.send("You already have an account! Use !view to see your elo.")
            return

        # Check if elos are valid
        elos = [tank_elo, dps_elo, support_elo] # List because check_valid_elo takes a list
        if self.check_valid_elo(elos) is None: # A length of 0 means an empty list was returned, meaning there was an invalid elo entered
            await ctx.send("Invalid elo entered. Command suspended.")
            return
        else:
            # Assign elos (default if 0)
            tank_elo, dps_elo, support_elo = self.check_valid_elo(elos)

        # Create the player object to be inserted
        player = {
            "_id": author_id,
            "name": author,
            "tank": tank_elo,
            "dps": dps_elo,
            "support": support_elo
        }

        # Insert the document
        insert_result = self.players_collection.insert_one(player)

        # Check if the adding failed
        if not insert_result.acknowledged:
            ctx.send("Internal Server Error. We cannot create your account at this time.")
            return

        await ctx.send(f"Successfully created account!\nTank: {tank_elo} | DPS: {dps_elo} | Support: {support_elo}")


    # Command for users to update accounts on our database
    @commands.command(brief=": Update your profile", description="Update a specific role with !update <role> <role_elo>")
    async def update(self, ctx, role: str = commands.parameter(description=": Desired role to update"), 
                     elo: int= commands.parameter(description=": New elo of desired role")):
        author_id = ctx.author.id # For database search purposes, ctx.author works as well but id is unique

        # check that a valid role was given
        role = role.lower()
        if (role != "tank" and role != "dps" and role != "support"):
            await ctx.send("Please enter a valid role (tank, dps, support)")
            return
        
        elos = [elo] #check_valid_elo takes in a list
        if self.check_valid_elo(elos)is None: # A length of 0 means an empty list was returned, meaning there was an invalid elo entered
            await ctx.send("Invalid elo entered. Command suspended.")
            return
        else:
            elo = self.check_valid_elo(elos)[0] # 0th index because check_valid_elo returns a list. In this case it will always be of length 1

        # update the account with the given id to have the given role be the given elo
        query = {"_id": author_id}
        update = {"$set": {role: elo}}
        update_result = self.players_collection.update_one(query, update)

        # check if update failed i.e. no modifications
        if update_result.modified_count <= 0:
            await ctx.send("Internal Server Error. We cannot update your account at this time.")
            return
        
        await ctx.send(f"Updated {role} elo: {elo}")


    # Command for users to view accounts on our database
    @commands.command(brief=": View a profile", description="View any profile on our database with !view <discord_tag>. Just !view will view your own account.")
    async def view(self, ctx, user: str= commands.parameter(default=None, description=": Discord tag to search")):
        # Handles no parameters auto searching for ctx.author
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
                await ctx.send("You don't have an account. Use !create to make one.")
                return
            
            await ctx.send("We couldn't find an account with that name.")
            return

        await ctx.send(f"{user_to_find}\nTank: {document['tank']} | DPS: {document['dps']} | Support: {document['support']}")

    

# Connect ProfileCommands to the bot (client)
async def setup(client):
    await client.add_cog(ProfileCommands(client))