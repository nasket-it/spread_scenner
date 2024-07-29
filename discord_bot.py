from main import bot_discord
import diskord
import aiohttp
import asyncio
import json
from diskord.ext import commands

# bot = commands.Bot(command_prefix='/')

@bot_discord.command()
async def ping(ctx):
    await ctx.send('pong')

@bot_discord.event
async def on_message(message):
    user = message.author
    name_channel = message.channel.name
    id_channl = message.channel.id
    id_user = message.author.id

    print(user, name_channel, id_channl )


