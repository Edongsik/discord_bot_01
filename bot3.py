
import discord
from discord.ext import commands

TOKEN = 'YOUR_DISCORD_BOT_TOKEN'

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

bot.run(TOKEN)
