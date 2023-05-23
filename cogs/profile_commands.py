import discord
from discord.ext import commands

#Profile commands 
class Profile(commands.Cog):

    def __init__(self, client):
        self.client = client

        
    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello")


async def setup(client):
    await client.add_cog(Profile(client))