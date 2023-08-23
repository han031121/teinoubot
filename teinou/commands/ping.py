import random
from teinou.client import client

@client.command(name="꺼져")
async def reaction(ctx):
        i = random.random()
        if i <= 0.001:
            await ctx.channel.send("느금")
        elif i <= 0.005:
            await ctx.channel.send("좆까")
        else:
            await ctx.channel.send("힝힝ㅠㅠ")
        return None

@client.command(name="꼬맹")
async def reaction(ctx):
    await ctx.channel.send("꼬맹통")

@client.command(name="힝힝ㅜㅜ")
async def reaction(ctx):
    await ctx.channel.send("꺼져")