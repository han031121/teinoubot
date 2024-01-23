from teinou.client import deletable_command
from random import randrange
from teinou.jplibrary import *

TEXT_PATH = "assets/teinoubot_texts/"
jpList = []; jpkList = []
len_jp = 0; len_jpk = 0; 
jpkDiffindex = [2135,1895,1493,1109,512,0] #난이도가 구분되는 index
jpkDiff = {
    "20\n":"中学 (2급)",
    "25\n":"中学 (준2급)",
    "30\n":"中学 (3급)",
    "40\n":"中学 (4급)",
    "50\n":"小6 (5급)",
    "60\n":"小5 (6급)",
    "70\n":"小4 (7급)",
    "80\n":"小3 (8급)",
    "90\n":"小2 (9급)",
    "100\n":"小1 (10급)",
}

with open(TEXT_PATH + "japanese_list.txt","r",encoding='UTF8') as f_japanese:
    tmpList = f_japanese.readlines()
    for i in range(len(tmpList)):
        jpList.append(tmpList[i].split("*")) #{일본단어}*{발음}*{한글뜻}
    len_jp = len(jpList)
with open(TEXT_PATH + "japankanji_list.txt","r",encoding='UTF8') as f_japankanji:
    tmpList = f_japankanji.readlines()
    for i in range(len(tmpList)):
        jpkList.append(tmpList[i].split(",")) #{한글훈음},{일본한자},{음독},{훈독},{난이도}
    len_jpk = len(jpkList)

def makeKanjiInfo(index): #한자 하나에 대한 설명 문자열 반환
    return "`" + jpkDiff[jpkList[index][4]] + "`" + "\n# " + jpkList[index][1] + "\n음 : " + jpkList[index][2] + "\n훈 : " + jpkList[index][3] + "\n韓 : " + jpkList[index][0]

def makeKanjiSearch(list_sound,list_mean): #음독,훈독 검색결과 문자열 반환
    string = ""
    if(len(list_sound) + len(list_mean) == 1):
        if len(list_sound) == 1:
            return makeKanjiInfo(list_sound[0])
        else:
            return makeKanjiInfo(list_mean[0])
    elif(len(list_sound) + len(list_mean) == 0):
        return "검색된 한자가 없습니다."
    else:
        string += "음독 검색결과 : "
        for i in list_sound:
            string += jpkList[i][1] + " "
        string += "\n훈독 검색결과 : "
        for i in list_mean:
            string += jpkList[i][1] + " "
        return string

def searchIndexlist(buf,context): #여러개의 index검색, list반환
    indexlist = []
    for i in range(len_jpk-1,-1,-1):
        if buf in jpkList[i][context]:
            indexlist.append(i)
    return indexlist

@deletable_command(name = "일본단어")
async def japanese(ctx,*args):
    return await ctx.channel.send("미구현 상태입니다.")
    index = randrange(0,len_jp)
    if len(jpList[index][1])>0:
        string = "# " + jpList[index][0] + " [" + jpList[index][1] + "]" + "\n뜻 : ||" + jpList[index][2] + "||"
    else:
        string = "# " + jpList[index][0] + "\n뜻 : ||" + jpList[index][2] + "||"
    return await ctx.channel.send(string)

@deletable_command(name = "일본한자")
async def japankanji(ctx,*args):
    if len(args) == 0:
        index = randrange(0,len_jpk)
        return await ctx.channel.send(makeKanjiInfo(index))
    else:
        if args[0].isdecimal(): #숫자일 경우
            try:
                index = randrange(jpkDiffindex[int(args[0])],jpkDiffindex[int(args[0])-1])
                return await ctx.channel.send(makeKanjiInfo(index))
            except IndexError:
                return await ctx.channel.send("올바른 난이도값을 입력해주세요. (1~5)")
        elif iskanji(args[0]): #한자일 경우
            for index in range(len_jpk-1,-1,-1):
                if jpkList[index][1] == args[0]:
                    return await ctx.channel.send(makeKanjiInfo(index))
            return await ctx.channel.send("해당 한자를 찾을 수 없습니다.")
        elif ishiragana(args[0]): #히라가나일 경우
            indexlist_sound = searchIndexlist(args[0],2)
            indexlist_mean = searchIndexlist(args[0],3)
            return await ctx.channel.send(makeKanjiSearch(indexlist_sound,indexlist_mean))
        elif args[0].encode().isalpha(): #알파벳일 경우
            string = engtohira(args[0])
            if string == -1:
                return await ctx.channel.send("올바르지 않은 입력입니다.")
            indexlist_sound = searchIndexlist(string,2)
            indexlist_mean = searchIndexlist(string,3)
            return await ctx.channel.send(makeKanjiSearch(indexlist_sound,indexlist_mean))
        else:
            return await ctx.channel.send("올바르지 않은 입력입니다.")
        
@deletable_command(name = "일본어")
async def japankanji(ctx,*args):
    string = engtohira(args[0])
    if string==-1:
        return await ctx.channel.send("올바르지 않은 입력입니다.")
    return await ctx.channel.send(engtohira(args[0]))