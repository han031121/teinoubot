import random
from teinou import client
from teinou.client import deletable_command

@deletable_command(name="꺼져")
async def reaction(ctx):
    i = random.random()
    if i <= 0.001:
        return await ctx.channel.send("느금")
    elif i <= 0.005:
        return await ctx.channel.send("좆까")
    return await ctx.channel.send("힝힝ㅠㅠ")

@deletable_command(name="꼬맹")
async def reaction(ctx):
    return await ctx.channel.send("꼬맹통")

@deletable_command(name="힝힝ㅠㅠ")
async def reaction(ctx):
    return await ctx.channel.send("꺼져")