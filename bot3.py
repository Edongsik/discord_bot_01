import discord
import random
import csv
import time
import difflib
from discord.ext import commands
import os

TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# CSV 파일 경로
csv_file_path = "/home/ec2-user/typing_sentences.csv"

# 연습용 문장 리스트 가져오기
def load_sentences_from_csv(file_path):
    sentences = []
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            sentences.append(row[0])  # 첫 번째 열에서 문장을 가져옴
    return sentences


# 연습용 문장 리스트
sentences = load_sentences_from_csv(csv_file_path)

leaderboard = {}

# discord.py 1.7.3 버전에서는 message_content 지원 X
intents = discord.Intents.default()
intents.messages = True  # 메시지 이벤트 활성화

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

def highlight_differences(expected, actual):
    matcher = difflib.SequenceMatcher(None, expected, actual)
    result = []
    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == 'equal':
            result.append(expected[i1:i2])
        elif op in ('replace', 'delete'):
            result.append(f"**{expected[i1:i2]}**")
        elif op == 'insert':
            result.append(f"**{actual[j1:j2]}**")
    return ''.join(result)

async def ask_for_retry(ctx):
    """사용자에게 다시 시도할 것인지 묻고, 응답에 따라 새로운 문제를 제공."""
    await ctx.send("한 번 더 하시겠습니까? (yes/no)")
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for('message', timeout=30.0, check=check)
        if msg.content.lower() in ['yes', 'y']:
            await typing_practice(ctx)
        elif msg.content.lower() in ['no', 'n']:
            await ctx.send("타자 연습을 종료합니다. 수고하셨습니다!")
        else:
            await ctx.send("잘못된 응답입니다. (yes/no)로 답변해주세요.")
            await ask_for_retry(ctx)
    except asyncio.TimeoutError:
        await ctx.send("시간 초과! 다시 시도하려면 `!타자연습`을 입력해주세요.")

@bot.command(name='타자연습')
async def typing_practice(ctx):
    sentence = random.choice(sentences)
    await ctx.send(f"다음 문장을 입력하세요:\n`{sentence}`")

    start_time = time.time()

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for('message', timeout=30.0, check=check)
        end_time = time.time()
        elapsed_time = end_time - start_time

        if msg.content.strip() == sentence:
            await ctx.send(f"정확합니다! 걸린 시간: {elapsed_time:.2f}초")
            user_id = str(ctx.author.id)
            if user_id not in leaderboard or elapsed_time < leaderboard[user_id]:
                leaderboard[user_id] = elapsed_time
                await ctx.send(f"{ctx.author.name}님의 최고 기록이 갱신되었습니다!")
        else:
            differences = highlight_differences(sentence, msg.content.strip())
            await ctx.send(f"틀렸습니다. 정답은:\n`{sentence}`\n\n입력한 내용:\n`{msg.content}`\n\n차이점:\n{differences}")

        await ask_for_retry(ctx)  # 연습을 다시 시도할지 묻기

    except asyncio.TimeoutError:
        await ctx.send("시간 초과! 다시 시도하려면 `!타자연습`을 입력해주세요.")

@bot.command(name='리더보드')
async def show_leaderboard(ctx):
    if not leaderboard:
        await ctx.send("리더보드에 등록된 기록이 없습니다.")
        return

    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1])
    message = "**리더보드**:\n"
    for idx, (user_id, time_record) in enumerate(sorted_leaderboard[:10], start=1):
        user = bot.get_user(int(user_id))  # bot.fetch_user 대신 bot.get_user 사용
        if user:
            message += f"{idx}. {user.name} - {time_record:.2f}초\n"
        else:
            message += f"{idx}. Unknown User - {time_record:.2f}초\n"
    await ctx.send(message)

bot.run(TOKEN)
