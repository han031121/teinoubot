'''
숫자 야구 기능
'''

from random import sample
from teinou import client
from discord import Embed

baseball_list = {} # id : [[ans1, ans2, ans3], strike, ball]

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

@client.command(name = "야구")
async def baseball(ctx,*args):
    if len(args)!=1:
        return None
    id = ctx.channel.id
    baseball_start = True if (id in baseball_list) else False

    if args[0]=='시작':
        ans = sample(range(0,10),3)
        baseball_list[id] = [ans,0,0] #[answer, strike, ball]
        await ctx.channel.send(embed=Embed(title="숫자야구",
                                           description="정답 생성 완료\n세 자리 숫자를 입력해주세요."))
        return None
    elif baseball_start==False:
        await ctx.channel.send(embed=Embed(title="숫자야구",
                                           description="게임이 시작되지 않았음"))
        return None
    
    if args[0]=='종료':
        ans_string = ''.join(str(element) for element in baseball_list[id][0])
        await ctx.channel.send(embed=Embed(title="숫자야구",
                                           description=f"정답 : {ans_string}. \n게임을 종료합니다."))
        del baseball_list[id]
        return None

    if args[0].isdigit() and len(args[0])==3:
        inp = [int(args[0][0]),int(args[0][1]),int(args[0][2])]
        if listDupCheck(inp,10):
            await ctx.channel.send(embed=Embed(title="숫자야구",
                                               description="중복없이 입력하세요"))
            return None
        
        baseball_list[id][1] = BaseballCount(baseball_list[id][0],inp,3,'strike') #count strike
        baseball_list[id][2] = BaseballCount(baseball_list[id][0],inp,3,'ball') #count ball
        if baseball_list[id][1]==3:
            await ctx.channel.send(embed=Embed(title="숫자야구",
                                               description="정답입니다. 게임을 종료합니다."))
            del baseball_list[id]
        else:
            await ctx.channel.send(embed=Embed(title=f"숫자야구 - {args[0][0]}{args[0][1]}{args[0][2]}",
                                               description=f"{baseball_list[id][1]} strike, {baseball_list[id][2]} ball"))
        return None
    else:
        await ctx.channel.send(embed=Embed(title="숫자야구",
                                           description="세자리 숫자를 입력하세요"))
        return None