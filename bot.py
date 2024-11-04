import discord
import asyncio
#import nest_asyncio
import random
from discord.ext import commands
import os

#nest_asyncio.apply()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Intents 설정
intents = discord.Intents.default()
intents.messages = True  # 메시지 이벤트를 활성화합니다.
intents.message_content = True  # 메시지 내용을 읽기 위해 필요합니다.

bot = commands.Bot(command_prefix='/', intents=intents)

# Sample quiz questions
quiz = {
    "What is the capital of France?": "Paris",
    "What is 2 + 2?": "4",
    "What is the color of the sky?": "Blue"
}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command(name='퀴즈')
async def quiz_game(ctx):
    question, answer = random.choice(list(quiz.items()))
    await ctx.send(f"퀴즈: {question}")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for('message', timeout=15.0, check=check)
        if msg.content.lower() == answer.lower():
            await ctx.send("정답입니다!")
        else:
            await ctx.send(f"틀렸습니다. 정답은 '{answer}'입니다.")
    except asyncio.TimeoutError:
        await ctx.send(f"시간이 초과되었습니다! 정답은 '{answer}'입니다.")

bot.run(TOKEN)
