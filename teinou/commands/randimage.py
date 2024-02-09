from teinou import ImageParser
from teinou.client import deletable_command
import discord

def getColor(r,g,b):
    return discord.Color.from_rgb(r,g,b)

def sendImage(ctx,name,color):
    embed = discord.Embed(title=name, color=color)
    file = ImageParser(name, 30).getRandomItem()
    embed.set_image(url=f"attachment://image.png")
    return ctx.channel.send(file=file, embed=embed)

@deletable_command(name="나즈나")
async def nazuna(ctx):
    return await sendImage(ctx,"nazuna",getColor(163,142,137))

@deletable_command(name="료")
async def ryo(ctx):
    return await ctx.channel.send("미구현 상태입니다.")
    return await sendImage(ctx,"ryo",getColor(70,108,165))