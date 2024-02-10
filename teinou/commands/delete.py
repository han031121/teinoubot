from teinou import client
from teinou.client import msgid_list
from discord import Embed

@client.command(name = "삭제")
async def delete_botmsg(ctx):
    channel_id = ctx.channel.id
    author_id = ctx.message.author.id
    if (not channel_id in msgid_list) or (not author_id in msgid_list[channel_id]):
        await ctx.channel.send(embed=Embed(description=f"{ctx.message.author}의 삭제 명령을 수행할 수 없습니다."))
        return None
    if msgid_list[channel_id][author_id] == None:
        await ctx.channel.send(embed=Embed(description=f"{ctx.message.author}의 삭제 명령을 수행할 수 없습니다."))
    else:
        message = await ctx.channel.fetch_message(msgid_list[channel_id][author_id])
        await message.delete()
        msgid_list[channel_id][author_id] = None
        await ctx.channel.send(embed=Embed(description=f'{ctx.message.author}의 최근 명령을 삭제했습니다.'))
        return None