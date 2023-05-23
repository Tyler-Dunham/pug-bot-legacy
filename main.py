import discord
from discord.ext import commands
import json
import os
from pymongo import MongoClient
import asyncio

# Keys
with open('KEYS.json', 'r') as f:
    data = json.load(f)
    

CONNECTION_STRING = data['DB_CONN_STRING']
# Create an instance of the mongo client
client = MongoClient(CONNECTION_STRING)
# Get the database
db = client.get_database("pugs")
# Get players collection
players_collection = db["players"]


# Bot Login Reqs
token = data['BOT_TOKEN']
intents = discord.Intents.all()
client = commands.Bot(command_prefix = "!", intents=intents)

# Load cogs on_ready
@client.event
async def on_ready():
	for filename in os.listdir('./cogs'):
		if filename.endswith('.py'):
			await client.load_extension(f'cogs.{filename[:-3]}')

client.run(token)