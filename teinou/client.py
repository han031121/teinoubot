'''
discord.py 

디스코드 봇 클라이언트와 저능아 봇의 토큰을 연결해줍니다.
.env 파일은 별도로 찾아야한다.

discord.py 클라이언트 객체는 client 변수에 들어가있다.
'''

import os
from dotenv import load_dotenv
from discord import Intents, Game, Status, app_commands, Interaction
from discord.ext import commands

load_dotenv()

GAME_STATUS = "MapleStory"
CMD_PREFIX = "!"

def get_token(token_mode:str):
    if token_mode == "develop":
        token =  os.getenv("TOKEN_DEV")
        if type(token) == str:
            return token
        raise Exception('토큰 환경변수가 존재하지 않습니다. .env 파일 혹은 환경변수를 확인하세요. ')
        
    elif token_mode == "product":
        token = os.getenv("TOKEN")
        if type(token) == str:
            return token
        raise Exception('토큰 환경변수가 존재하지 않습니다. .env 파일 혹은 환경변수를 확인하세요. ')

    raise Exception('토큰 호출 방식이 잘못 되었습니다. 방식 : "develop", "product" ')

intents = Intents.default()

# 이것도 환경변수로 빼야함.
intents.messages = True
intents.message_content = True

game = Game(GAME_STATUS)

client = commands.Bot(command_prefix=CMD_PREFIX, intents=intents, game=game)

msgid_list = {} # user id : bot's last task(msg)

async def msgidSave(channel_id,author_id,message_id):
    try:
        msgid_list[channel_id][author_id] = message_id
    except KeyError:
        msgid_list[channel_id] = {author_id:message_id}

@client.event
async def on_ready():
    await client.change_presence(status=Status.online, activity=game)

@client.command(name="sync")
async def sync_slashcommand(ctx):
    synced = await client.tree.sync()
    for s in synced:
        print(s)