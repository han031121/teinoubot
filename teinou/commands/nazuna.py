
from teinou import client
from teinou.image import ImageParser

imageParser = ImageParser('nazuna', 50)

@client.command(name="나즈나") #prerandNum index : 1
async def nazuna(ctx):
    id = ctx.channel.id

    # if id in prerandNum[1]:
    #     randNum = nodupRand(1, imageCount+1, prerandNum[1][id])
    #     prerandNum[1][id].append(randNum)
    #     if len(prerandNum[1][id])>nodupLimit:
    #         prerandNum[1][id].pop(0)
    # else:
    #     randNum = randrange(1,imageCount+1)
    #     prerandNum[1][id] = [randNum]
    
    # filename = imagehome + '/nazuna/nazuna (' + str(randNum) + ').jpg'
    # await ctx.channel.send(file = discord.File(open(filename,'rb')))
    # print('{}, nazuna //'.format(id), randNum, ', {} images.'.format(imageCount))
    # return None