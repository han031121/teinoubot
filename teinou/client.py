'''
discord.py 

디스코드 봇 클라이언트와 저능아 봇의 토큰을 연결해줍니다.
.env 파일은 별도로 찾아야한다.

discord.py 클라이언트 객체는 client 변수에 들어가있다.
'''

import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()

TOKEN_ATTR = os.getenv('TOKEN_ATTR')
GAME_STATUS = os.getenv('GAME_STATUS')
CMD_PREFIX = os.getenv('CMD_PREFIX')

token = os.getenv(TOKEN_ATTR)
intents = discord.Intents.default()

# 이것도 환경변수로 빼야함.
intents.messages = True
intents.message_content = True

game = discord.Game(GAME_STATUS)

client = commands.Bot(command_prefix=CMD_PREFIX, intents=intents, game=game)

msgid_list = {} # user id : bot's last task(msg)

async def msgidSave(channel_id,author_id,message_id):
    try:
        msgid_list[channel_id][author_id] = message_id
    except KeyError:
        msgid_list[channel_id] = {author_id:message_id}

'''
deletable_command

@params : name = 커맨드 이름

해당 함수의 리턴 값은 ctx.channel.send() 함수의 리턴 값이여야한다.
또한, ctx.channel.send() 는 비동기 함수 이므로, 앞에 await을 붙여야한다.

e.g. ) return await ctx.channel.send("test")
'''
def deletable_command(name= ...):
    print(name)
    def decorator(func):
        @client.command(name=name)
        async def wrapper(ctx, *args):
            msg = await func(ctx, *args)
            if msg != None:
                await msgidSave(ctx.channel.id, ctx.message.author.id, msg.id)
            print(msgid_list)
    return decorator


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=game)