from typing import Optional
from teinou.client import deletable_command
from random import randrange
from teinou.jplibrary import *
import discord

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

def makeKanjiSearch(indexlist_sound,indexlist_mean): #음독,훈독 검색결과 문자열 반환
    if(len(indexlist_sound) + len(indexlist_mean) == 1):
        if len(indexlist_sound) == 1:
            return makeKanjiInfo(indexlist_sound[0])
        else:
            return makeKanjiInfo(indexlist_mean[0])
    elif(len(indexlist_sound) + len(indexlist_mean) == 0):
        return "검색된 한자가 없습니다."

def searchIndexlist(buf,context): #여러개의 index검색, list반환
    indexlist = []
    for i in range(len_jpk-1,-1,-1):
        if buf in jpkList[i][context]:
            indexlist.append(i)
    return indexlist

def searchIndex(buf,context): #하나의 index검색, 반환
    for i in range(len_jpk-1,-1,-1):
        if buf in jpkList[i][context]:
            return i
    return -1

class KanjiSearchList(discord.ui.View):
    soundlist = [2,3,4,5]
    meanlist = [2000,2001,2002,2003]
    def __init__(self, soundlist_, meanlist_, *, timeout: float | None = 180):
        super().__init__(timeout=timeout)
        soundlist = soundlist_
        meanlist = meanlist_
    option_sound = [discord.SelectOption(label = jpkList[i][1], description=jpkList[i][2]+" / "+jpkList[i][3]+" / "+jpkList[i][0]) for i in soundlist]
    option_mean = [discord.SelectOption(label = jpkList[i][1], description=jpkList[i][2]+" / "+jpkList[i][3]+" / "+jpkList[i][0]) for i in meanlist]
    #각각의 options에 SelectOption리스트 대입할 것
    @discord.ui.select(placeholder="음독 검색 결과", min_values = 1, max_values = 1, options=option_sound)
    async def soundlist_callback(self, interaction, select:discord.ui.select):
        await interaction.response.edit_message(content = makeKanjiInfo(searchIndex(select.values[0],1)))
    @discord.ui.select(placeholder="훈독 검색 결과", min_values = 1, max_values = 1, options = option_mean)
    async def meanlist_callback(self, interaction, select:discord.ui.select):
        await interaction.response.edit_message(content = makeKanjiInfo(searchIndex(select.values[0],1)))

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
            index = searchIndex(args[0],1)
            if index==-1:
                return await ctx.channel.send("해당 한자를 찾을 수 없습니다.")
            return await ctx.channel.send(makeKanjiInfo(searchIndex(args[0],1)))
        
        elif ishangeul(args[0]): #한글일 경우
            return await ctx.channel.send("이건 한글입니다.")
        
        else: #히라가나,영어일 경우
            if args[0].encode().isalpha():
                string = engtohira(args[0])
                if string == -1:
                    return await ctx.channel.send("올바르지 않은 입력입니다.")
            elif ishiragana(args[0]):
                string = args[0]
            else:
                return await ctx.channel.send("올바르지 않은 입력입니다.")

            indexlist_sound = searchIndexlist(string,2)
            indexlist_mean = searchIndexlist(string,3)
            if(len(indexlist_sound) + len(indexlist_mean) == 1):
                if len(indexlist_sound) == 1:
                    return await ctx.channel.send(makeKanjiInfo(indexlist_sound[0]))
                else:
                    return await ctx.channel.send(makeKanjiInfo(indexlist_mean[0]))
            elif(len(indexlist_sound) + len(indexlist_mean) == 0):
                return await ctx.channel.send("검색된 한자가 없습니다.")
            else:
                return await ctx.channel.send("한자를 선택해주세요.", view = KanjiSearchList(indexlist_sound,indexlist_mean))
        
@deletable_command(name = "일본어")
async def japankanji(ctx,*args):
    if engtohira(args[0])==-1:
        return await ctx.channel.send("올바르지 않은 입력입니다.")
    return await ctx.channel.send(engtohira(args[0]))