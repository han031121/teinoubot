from teinou import ImageParser
from teinou.client import deletable_command

imageParser_nazuna = ImageParser('nazuna', 50)
#imageParser_ryo = ImageParser('ryo', 30)

@deletable_command(name="나즈나")
async def nazuna(ctx):
    return await ctx.channel.send(file = imageParser_nazuna.getRandomItem())

@deletable_command(name="료")
async def ryo(ctx):
    return await ctx.channel.send("미구현 상태입니다.")
    return await ctx.channel.send(file = imageParser_ryo.getRandomItem())