
from teinou import client, ImageParser

imageParser = ImageParser('nazuna', 50)

@client.command(name="나즈나") #prerandNum index : 1
async def nazuna(ctx):
    id = ctx.channel.id
    await ctx.channel.send(file = imageParser.getRandomItem())