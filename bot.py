import discord
from discord.ext import commands
import json
import os
from db import connect_db

# Open keys
with open('KEYS.json', 'r') as f:
    data = json.load(f)
    
# Connect to db (db.py)
connect_db(data)

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