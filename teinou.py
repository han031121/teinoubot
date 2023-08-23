import discord
from discord.ext import commands
from random import *
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("token_main")
#token = os.getenv("token_test") #test
print(token)


imagehome = './teinoubot_image' #image path

def listDupCheck(list,num):
    for i in range(0,num):
        if list.count(i)>1:
            return True
    return False

def BaseballCount(Ans,Inp,len,mode):
    count=0
    for i in range(0,len):
        for j in range(0,len):
            if Inp[i]==Ans[j]:
                if (mode=='ball' and i!=j) or (mode=='strike' and i==j):
                    count+=1
    return count

def nodupRand(start, end, excluded_value):
    num = randrange(start, end)
    while num in excluded_value:
        num = randrange(start, end)
    return num

presdt={};nzn={}
prerandNum = (presdt,nzn)
baseball_list = {} # id : [[ans1, ans2, ans3], strike, ball]

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=game)

@bot.command(name = "꼬맹")
async def test1(ctx):
    await ctx.channel.send("꼬맹눈")
    return None

@bot.command(name = "꺼져")
async def test2(ctx):
    i = random()
    if i<0.001:
        await ctx.channel.send("느금")
    elif i<0.005:
        await ctx.channel.send("좆까")
    else:
        await ctx.channel.send("힝힝ㅠㅠ")
    return None

@bot.command(name='힝힝ㅠㅠ')
async def test3(ctx):
    await ctx.channel.send("꺼져")
    return None

@bot.command(name = "대통령") #prerandNum index : 0
async def president(ctx,*args):
    id = ctx.channel.id
    president = ('박정희','전두환','노무현','이명박','박근혜','문재인','윤석열')
    imageCount = (5,4,15,6,5,10,6) #president image count

    if len(args)==0:
        await ctx.channel.send('보고싶은 대통령을 함께 입력하세요')
    else:
        try:
            presdtNum = president.index(args[0])

            try:
                randNum = nodupRand(1, imageCount[presdtNum]+1, prerandNum[0][id])
                prerandNum[0][id] = [randNum]
            except KeyError:
                randNum = randrange(1,imageCount[presdtNum]+1)
                prerandNum[0][id] = [randNum]
            
            filename = imagehome + '/president/pre'+str(presdtNum)+' ('+str(randNum)+').jpg'
            file = discord.File(filename, spoiler=True)
            await ctx.channel.send(file = file)
        except ValueError:
            return None

@bot.command(name="나즈나") #prerandNum index : 1
async def nazuna(ctx):
    id = ctx.channel.id
    imageCount = len(os.listdir(imagehome + '/nazuna'))
    nodupLimit = 50

    if id in prerandNum[1]:
        randNum = nodupRand(1, imageCount+1, prerandNum[1][id])
        prerandNum[1][id].append(randNum)
        if len(prerandNum[1][id])>nodupLimit:
            prerandNum[1][id].pop(0)
    else:
        randNum = randrange(1,imageCount+1)
        prerandNum[1][id] = [randNum]
    
    filename = imagehome + '/nazuna/nazuna (' + str(randNum) + ').jpg'
    await ctx.channel.send(file = discord.File(open(filename,'rb')))
    print('{}, nazuna //'.format(id), randNum, ', {} images.'.format(imageCount))
    return None

@bot.command(name = "야구")
async def baseball(ctx,*args):
    if len(args)!=1:
        return None
    id = ctx.channel.id
    baseball_start = True if (id in baseball_list) else False

    if args[0]=='시작':
        ans = sample(range(0,10),3)
        baseball_list[id] = [ans,0,0] #[answer, strike, ball]
        await ctx.channel.send("정답 생성 완료")
        print('{}, baseball //'.format(id),baseball_list[id][0])
        return None
    elif baseball_start==False:
        await ctx.channel.send("게임이 시작되지 않았음")
        return None
    
    if args[0]=='종료':
        ans_string = ''.join(str(element) for element in baseball_list[id][0])
        await ctx.channel.send("정답 : {}. 게임을 종료합니다.".format(ans_string))
        del baseball_list[id]
        return None

    if args[0].isdigit() and len(args[0])==3:
        inp = [int(args[0][0]),int(args[0][1]),int(args[0][2])]
        if listDupCheck(inp,10):
            await ctx.channel.send("중복없이 입력하세요")
            return None
        
        baseball_list[id][1] = BaseballCount(baseball_list[id][0],inp,3,'strike') #count strike
        baseball_list[id][2] = BaseballCount(baseball_list[id][0],inp,3,'ball') #count ball
        if baseball_list[id][1]==3:
            await ctx.channel.send("정답입니다. 게임을 종료합니다.")
            del baseball_list[id]
        else:
            await ctx.channel.send("{} strike, {} ball".format(baseball_list[id][1],baseball_list[id][2]))
        return None
    else:
        await ctx.channel.send("세자리 숫자를 입력하세요")
        return None

