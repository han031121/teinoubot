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


def deletable_command(name= ...):
    '''
    deletable_command
    
    해당 데코레이터를 추가한 함수를 정의하고 그 모듈을 불러올 경우, 함수가 그대로 정의되므로 주의 해야한다.

    @params : name = 커맨드 이름

    해당 함수의 리턴 값은 ctx.channel.send() 함수의 리턴 값이여야한다.
    또한, ctx.channel.send() 는 비동기 함수 이므로, 앞에 await을 붙여야한다.

    e.g. ) return await ctx.channel.send("test")
    '''
    # print(name)
    def decorator(func):
        @client.command(name=name)
        async def wrapper(ctx, *args):
            msg = await func(ctx, *args)
            if msg != None:
                await msgidSave(ctx.channel.id, ctx.message.author.id, msg.id)
            print(msgid_list)
    return decorator


def slash_command(name:str, description:str, params_dsc={}):
    '''슬래시 커맨드를 생성하는 데코레이터

    해당 데코레이터를 사용할 경우, 반드시 첫번째 인자로 interaction: discord.Interaction 을 받을 필요가 없습니다.
    해당 Interaction 에 대한 답장을 보내줄 때에는 await interaction.response.send_message(str) 형태로 메소드를 호출해주면 됩니다.
    데코레이팅되는 함수의 인자는
    @params
        name : 커맨드의 이름입니다. 실제로
        description : 디스코드 봇이 해당 커맨드의 부가 설명을 표시합니다.
        params_dsc : 디스코드 봇이 표시할 해당 슬래시 커맨드의 인자를 담습니다. Dict(...arguments) 형태로 표현됩니다.
        
    '''
    def decorator(func):
        @client.tree.command(name=name, description=description)
        @app_commands.describe(**params_dsc)
        async def wrapper(interaction:Interaction, *args):
            ret = await func(interaction, *args) # 원 함수의 return value.
            return ret
    return decorator


@client.event
async def on_ready():
    await client.change_presence(status=Status.online, activity=game)

@client.tree.command(name="맹꽁")
async def mk(interaction:Interaction):
    await interaction.response.send_message("맹꽁", ephemeral=True)

@client.command(name="sync_slashcommand")
async def sync_slashcommand(ctx):
    synced = await client.tree.sync()
    print(len(synced))