import discord
from discord.ext import commands
import os

TOKEN = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command(name='인사')
async def hello(ctx):
    await ctx.send('Hello!')

bot.run(TOKEN)
