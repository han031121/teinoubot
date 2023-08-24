from teinou import ImageParser
from teinou.client import deletable_command

imageParser = ImageParser('nazuna', 50)

@deletable_command(name="나즈나") #prerandNum index : 1
async def nazuna(ctx):
    return await ctx.channel.send(file = imageParser.getRandomItem())