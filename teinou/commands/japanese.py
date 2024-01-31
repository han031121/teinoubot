from typing import Optional
from teinou.client import deletable_command
from random import randrange
from teinou.jplibrary import *
from math import ceil
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

def emptySearchResult():
    return discord.ui.Select(
        placeholder = "검색 결과가 없음",
        min_values = 1,
        max_values = 1,
        options = [discord.SelectOption(label = ".")],
        disabled=True)
def makeSelect(placeholder, options):
    return discord.ui.Select(
        placeholder = placeholder,
        min_values = 1,
        max_values = 1,
        options = options)

def KanjiSelectmenu(indexlist_sound, indexlist_mean, page_sound, page_mean):
    page_sound = page_sound
    page_mean = page_mean
    totalpage_sound = ceil(len(indexlist_sound)/25)
    totalpage_mean = ceil(len(indexlist_mean)/25)

    if page_sound>totalpage_sound: page_sound = totalpage_sound
    if page_mean>totalpage_mean: page_mean = totalpage_mean
    if page_sound<1: page_sound = 1
    if page_mean<1: page_mean = 1

    option_sound = [discord.SelectOption(label = jpkList[i][1],
            description=jpkList[i][2]+" / "+jpkList[i][3]+" / "+jpkList[i][0]) 
            for i in indexlist_sound[ slice((page_sound-1)*25,min([page_sound*25,len(indexlist_sound)])) ]]
    option_mean = [discord.SelectOption(label = jpkList[i][1],
            description=jpkList[i][2]+" / "+jpkList[i][3]+" / "+jpkList[i][0]) 
            for i in indexlist_mean[ slice((page_mean-1)*25,min([page_mean*25,len(indexlist_mean)])) ]]

    if len(option_sound)>0:
        select_sound = makeSelect("음독 검색 결과 ("+str(page_sound)+"/"+str(totalpage_sound)+")", option_sound)
    else:
        select_sound = emptySearchResult()
    if len(option_mean)>0:
        select_mean = makeSelect("훈독 검색 결과 ("+str(page_mean)+"/"+str(totalpage_mean)+")", option_mean)
    else:
        select_mean = emptySearchResult()
    prev_sound = discord.ui.Button(label="음독 이전",style=discord.ButtonStyle.blurple)
    next_sound = discord.ui.Button(label="음독 다음",style=discord.ButtonStyle.blurple)
    prev_mean = discord.ui.Button(label="훈독 이전",style=discord.ButtonStyle.green)
    next_mean = discord.ui.Button(label="훈독 다음",style=discord.ButtonStyle.green)
    reset = discord.ui.Button(label="다시 선택",style=discord.ButtonStyle.gray)

    view = discord.ui.View()
    result_view = discord.ui.View()
    view.add_item(select_sound)
    view.add_item(select_mean)
    view.add_item(prev_sound)
    view.add_item(next_sound)
    view.add_item(prev_mean)
    view.add_item(next_mean)
    result_view.add_item(reset)

    async def callback_reset(interaction):
        await interaction.response.edit_message(content = "한자를 선택해주세요.", view = KanjiSelectmenu(indexlist_sound,indexlist_mean,1,1))
    async def callback_sound(interaction,select=select_sound):
        if (len(select.values)>0):
            await interaction.response.edit_message(content = makeKanjiInfo(searchIndex(select.values[-1],1)), view = result_view)
    async def callback_mean(interaction,select=select_mean):
        if (len(select.values)>0):
            await interaction.response.edit_message(content = makeKanjiInfo(searchIndex(select.values[-1],1)), view = result_view)
    async def callback_next_sound(interaction):
        await interaction.response.edit_message(view = KanjiSelectmenu(indexlist_sound,indexlist_mean,page_sound+1,page_mean))
    async def callback_next_mean(interaction):
        await interaction.response.edit_message(view = KanjiSelectmenu(indexlist_sound,indexlist_mean,page_sound,page_mean+1))
    async def callback_prev_sound(interaction):
        await interaction.response.edit_message(view = KanjiSelectmenu(indexlist_sound,indexlist_mean,page_sound-1,page_mean))
    async def callback_prev_mean(interaction):
        await interaction.response.edit_message(view = KanjiSelectmenu(indexlist_sound,indexlist_mean,page_sound,page_mean-1))

    select_sound.callback = callback_sound
    select_mean.callback = callback_mean
    next_sound.callback = callback_next_sound
    next_mean.callback = callback_next_mean
    prev_sound.callback = callback_prev_sound
    prev_mean.callback = callback_prev_mean
    reset.callback = callback_reset
    
    return view

def KanjiRegen(diff):
    view = discord.ui.View()
    regenButton = discord.ui.Button(label="다시 생성", style=discord.ButtonStyle.gray)

    async def regenButton_callback(interaction):
        if diff!=0:
            index = randrange(jpkDiffindex[diff],jpkDiffindex[diff-1])
        else:
            index = randrange(0,len_jpk)
        await interaction.response.edit_message(content = makeKanjiInfo(index))
    regenButton.callback = regenButton_callback

    view.add_item(regenButton)
    return view

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
        return await ctx.channel.send(makeKanjiInfo(index), view = KanjiRegen(0))
    else:
        if args[0].isdecimal(): #숫자일 경우
            try:
                index = randrange(jpkDiffindex[int(args[0])],jpkDiffindex[int(args[0])-1])
                return await ctx.channel.send(makeKanjiInfo(index), view = KanjiRegen(int(args[0])))
            except IndexError:
                return await ctx.channel.send("올바른 난이도값을 입력해주세요. (1~5)")
            
        elif iskanji(args[0]): #한자일 경우
            index = searchIndex(args[0],1)
            if index==-1:
                return await ctx.channel.send("해당 한자를 찾을 수 없습니다.")
            return await ctx.channel.send(makeKanjiInfo(searchIndex(args[0],1)))
        
        elif ishangeul(args[0]): #한글일 경우
            return await ctx.channel.send("이건 한글입니다.")
        
        else: #히라가나,영어, 기타 올바르지 않은 입력일 경우
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
                return await ctx.channel.send("한자를 선택해주세요.", view = KanjiSelectmenu(indexlist_sound,indexlist_mean,1,1))
        
@deletable_command(name = "일본어")
async def japankanji(ctx,*args):
    if engtohira(args[0])==-1:
        return await ctx.channel.send("올바르지 않은 입력입니다.")
    return await ctx.channel.send(engtohira(args[0]))