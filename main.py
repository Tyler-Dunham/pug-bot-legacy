import discord
from discord.ext import commands
import json
import os
from pymongo import MongoClient

# Connection string
with open('KEYS.json', 'r') as f:
    data = json.load(f)

CONNECTION_STRING = data['DB_CONN_STRING']
# Create an instance of the mongo client
client = MongoClient(CONNECTION_STRING)
# Get the database
db = client.get_database("pugs")
# Get players collection
players_collection = db["players"]

#Bot Login
with open('KEYS.json', 'r') as f:
    discordToken = json.load(f)

token = discordToken['BOT_TOKEN']
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