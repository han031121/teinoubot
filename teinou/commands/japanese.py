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

def makeKanjifile(index):
    return discord.File(kanjiImage(jpkList[index][1]), filename = "image.png")
def makeKanjiInfo(index): #한자 하나에 대한 설명 embed 반환
    embed = discord.Embed(
        title="일본한자 - " + jpkList[index][1],
        color=discord.Color.fuchsia()
    )
    embed.set_thumbnail(url=f"attachment://image.png")
    embed.add_field(name="음독",value=jpkList[index][2],inline=True)
    embed.add_field(name="훈독",value=jpkList[index][3],inline=False)
    embed.add_field(name="한국훈음",value=jpkList[index][0],inline=True)
    embed.add_field(name="난이도",value=jpkDiff[jpkList[index][4]],inline=True)
    return embed

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
    slicer_sound = slice((page_sound-1)*25,min([page_sound*25,len(indexlist_sound)]))
    slicer_mean = slice((page_mean-1)*25,min([page_mean*25,len(indexlist_mean)]))

    option_sound = [discord.SelectOption(label = jpkList[i][1],
            description=jpkList[i][2]+" / "+jpkList[i][3]+" / "+jpkList[i][0]) 
            for i in indexlist_sound[slicer_sound]]
    option_mean = [discord.SelectOption(label = jpkList[i][1],
            description=jpkList[i][2]+" / "+jpkList[i][3]+" / "+jpkList[i][0]) 
            for i in indexlist_mean[slicer_mean]]

    if len(option_sound)>0:
        select_sound = makeSelect("음독 검색 결과 ("+str(page_sound)+"/"+str(totalpage_sound)+")", option_sound)
    else:
        select_sound = emptySearchResult()
    if len(option_mean)>0:
        select_mean = makeSelect("훈독 검색 결과 ("+str(page_mean)+"/"+str(totalpage_mean)+")", option_mean)
    else:
        select_mean = emptySearchResult()
    prev_sound = discord.ui.Button(label="이전(음)",style=discord.ButtonStyle.blurple)
    next_sound = discord.ui.Button(label="다음(음)",style=discord.ButtonStyle.blurple)
    prev_mean = discord.ui.Button(label="이전(훈)",style=discord.ButtonStyle.green)
    next_mean = discord.ui.Button(label="다음(훈)",style=discord.ButtonStyle.green)
    again = discord.ui.Button(label="다시 선택", style=discord.ButtonStyle.blurple)

    view = discord.ui.View()
    view.add_item(select_sound)
    view.add_item(select_mean)
    view.add_item(prev_sound)
    view.add_item(next_sound)
    view.add_item(prev_mean)
    view.add_item(next_mean)
    view_select = discord.ui.View()
    view_select.add_item(again)

    async def callback_sound(interaction,select=select_sound):
        if (len(select.values)>0):
            await interaction.message.delete()
            await interaction.channel.send(content = '', file = makeKanjifile(searchIndex(select.values[-1],1)),
                                                    embed = makeKanjiInfo(searchIndex(select.values[-1],1)), view = view_select)
    async def callback_mean(interaction,select=select_mean):
        if (len(select.values)>0):
            await interaction.message.delete()
            await interaction.channel.send(content = '', file = makeKanjifile(searchIndex(select.values[-1],1)),
                                                    embed = makeKanjiInfo(searchIndex(select.values[-1],1)), view = view_select)
    async def callback_next_sound(interaction):
        await interaction.response.edit_message(view = KanjiSelectmenu(indexlist_sound,indexlist_mean,page_sound+1,page_mean))
    async def callback_next_mean(interaction):
        await interaction.response.edit_message(view = KanjiSelectmenu(indexlist_sound,indexlist_mean,page_sound,page_mean+1))
    async def callback_prev_sound(interaction):
        await interaction.response.edit_message(view = KanjiSelectmenu(indexlist_sound,indexlist_mean,page_sound-1,page_mean))
    async def callback_prev_mean(interaction):
        await interaction.response.edit_message(view = KanjiSelectmenu(indexlist_sound,indexlist_mean,page_sound,page_mean-1))
    async def callback_again(interaction):
        await interaction.message.delete()
        await interaction.channel.send(view = KanjiSelectmenu(indexlist_sound,indexlist_mean,page_sound,page_mean),
                                       embed=discord.Embed(description="한자를 선택해주세요."))

    select_sound.callback = callback_sound
    select_mean.callback = callback_mean
    next_sound.callback = callback_next_sound
    next_mean.callback = callback_next_mean
    prev_sound.callback = callback_prev_sound
    prev_mean.callback = callback_prev_mean
    again.callback = callback_again
    return view

def regenButton(diff):
    view = discord.ui.View()
    button = discord.ui.Button(label="다시 생성",style=discord.ButtonStyle.blurple)
    index = randrange(diff,len_jpk)

    async def callback(interaction):
        await interaction.message.delete()
        await interaction.channel.send(file = makeKanjifile(index),
                                                embed = makeKanjiInfo(index),
                                                view = regenButton(diff))
    button.callback = callback
    view.add_item(button)
    return view

@deletable_command(name = "일본단어")
async def japanese(ctx,*args):
    return await ctx.channel.send(embed=discord.Embed(description="미구현 상태입니다."))
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
        return await ctx.channel.send(file = makeKanjifile(index), 
                                      embed = makeKanjiInfo(index),
                                      view = regenButton(0))
    else:
        if args[0].isdecimal(): #숫자일 경우
            try:
                index = randrange(jpkDiffindex[int(args[0])],jpkDiffindex[int(args[0])-1])
                return await ctx.channel.send(file = makeKanjifile(index), 
                                              embed = makeKanjiInfo(index),
                                              view = regenButton(int(args[0])))
            except:
                return await ctx.channel.send(embed=discord.Embed(description="올바른 난이도값을 입력해주세요. (1~5)"))
            
        elif iskanji(args[0]): #한자일 경우
            index = searchIndex(args[0],1)
            if index==-1:
                return await ctx.channel.send(embed=discord.Embed(description="해당 한자를 찾을 수 없습니다."))
            return await ctx.channel.send(file = makeKanjifile(index), 
                                          embed = makeKanjiInfo(searchIndex(args[0],1)))
        
        elif ishangeul(args[0]): #한글일 경우
            return await ctx.channel.send(embed=discord.Embed(description="이건 한글입니다."))
        
        else: #히라가나,영어, 기타 올바르지 않은 입력일 경우
            if args[0].encode().isalpha():
                string = engtohira(args[0])
                if string == -1:
                    return await ctx.channel.send(embed=discord.Embed(description="올바르지 않은 입력입니다."))
            elif ishiragana(args[0]):
                string = args[0]
            else:
                return await ctx.channel.send(embed=discord.Embed(description="올바르지 않은 입력입니다."))

            indexlist_sound = searchIndexlist(string,2)
            indexlist_mean = searchIndexlist(string,3)
            if(len(indexlist_sound) + len(indexlist_mean) == 1):
                if len(indexlist_sound) == 1:
                    return await ctx.channel.send(file = makeKanjifile(indexlist_sound[0]), 
                                                  embed = makeKanjiInfo(indexlist_sound[0]))
                else:
                    return await ctx.channel.send(file = makeKanjifile(indexlist_mean[0]), 
                                                  embed = makeKanjiInfo(indexlist_mean[0]))
            elif(len(indexlist_sound) + len(indexlist_mean) == 0):
                return await ctx.channel.send(embed=discord.Embed(description="검색된 한자가 없습니다."))
            else:
                return await ctx.channel.send(embed=discord.Embed(description="한자를 선택해주세요."),
                                              view=KanjiSelectmenu(indexlist_sound,indexlist_mean,1,1))
            
@deletable_command(name = "일본어")
async def japankanji(ctx,*args):
    if engtohira(args[0])==-1:
        return await ctx.channel.send(embed=discord.Embed(description="올바르지 않은 입력입니다."))
    return await ctx.channel.send(engtohira(args[0]))