import discord
from discord.ext import commands
import json
import os
from pymongo import MongoClient

CONNECTION_STRING = "mongodb+srv://albion:tJAmID8vqeM8YzrZ@pugs.0ra0ugs.mongodb.net/?retryWrites=true&w=majority"
# Create an instance of the mongo client
client = MongoClient(CONNECTION_STRING)
# Get the database
db = client.get_database("pugs")
# Get players collection
players_collection = db["players"]

#Bot Login
with open('BOT_KEYS.json', 'r') as f:
    discordToken = json.load(f)

token = discordToken['TOKEN']
intents = discord.Intents.default()
client = commands.Bot(command_prefix="!", intents=intents)

@client.command()
async def load(ctx, extension):
	client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
	client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f'cogs.{filename[:-3]}')

client.run(token)