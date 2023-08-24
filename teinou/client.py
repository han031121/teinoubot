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