from teinou.client import client
from random import randrange
from teinou.kanjilibrary import *
from math import ceil
from discord import Interaction, ui, Embed, app_commands, File, SelectOption, ButtonStyle, Color
from discord.app_commands import Choice
import re

TEXT_PATH = "assets/teinoubot_texts/"
jpList = []; jpkList = []
len_jp = 0; len_jpk = 0; 
jpkDiffindex = [2135,2055,1895,1695,1493,1300,1109,796,512,184,0] #난이도가 구분되는 index
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

def file_kanjiImage(index):
    return File(kanjiImage(jpkList[index][1]), filename = "image.png")
def embed_kanjiInfo(index): #한자 하나에 대한 설명 embed 반환
    embed = Embed(
        title="일본한자 - " + jpkList[index][1],
        color=Color.fuchsia()
    )
    embed.set_thumbnail(url=f"attachment://image.png")
    embed.add_field(name="음독",value=jpkList[index][2],inline=True)
    embed.add_field(name="훈독",value=jpkList[index][3],inline=False)
    embed.add_field(name="한국훈음",value=jpkList[index][0],inline=True)
    embed.add_field(name="난이도",value=jpkDiff[jpkList[index][4]],inline=True)
    return embed

def searchIndexlist(pat,context): #여러개의 index검색, list반환
    indexlist = []
    for i in range(len_jpk-1,-1,-1):
        if re.fullmatch(pat,jpkList[i][context]):
            indexlist.append(i)
    return indexlist
def searchIndex(buf,context): #하나의 index검색, 반환
    for i in range(len_jpk-1,-1,-1):
        if buf in jpkList[i][context]:
            return i
    return -1

def view_kanjiSelectmenu(indexlist_sound, indexlist_mean, page_sound, page_mean):
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

    option_sound = [SelectOption(label = jpkList[i][1],
            description=jpkList[i][2]+" / "+jpkList[i][3]+" / "+jpkList[i][0]) 
            for i in indexlist_sound[slicer_sound]]
    option_mean = [SelectOption(label = jpkList[i][1],
            description=jpkList[i][2]+" / "+jpkList[i][3]+" / "+jpkList[i][0]) 
            for i in indexlist_mean[slicer_mean]]

    if len(option_sound)>0:
        select_sound = select_list("음독 검색 결과 ("+str(page_sound)+"/"+str(totalpage_sound)+")", option_sound)
    else:
        select_sound = select_list("음독 검색 결과 없음", [SelectOption(label = ".")], True)
    if len(option_mean)>0:
        select_mean = select_list("훈독 검색 결과 ("+str(page_mean)+"/"+str(totalpage_mean)+")", option_mean)
    else:
        select_mean = select_list("훈독 검색 결과 없음", [SelectOption(label = ".")], True)
    prev_sound = ui.Button(label="이전(음)",style=ButtonStyle.blurple)
    next_sound = ui.Button(label="다음(음)",style=ButtonStyle.blurple)
    prev_mean = ui.Button(label="이전(훈)",style=ButtonStyle.green)
    next_mean = ui.Button(label="다음(훈)",style=ButtonStyle.green)

    view = ui.View()
    view.add_item(select_sound)
    view.add_item(select_mean)
    view.add_item(prev_sound)
    view.add_item(next_sound)
    view.add_item(prev_mean)
    view.add_item(next_mean)

    async def callback_sound(interaction,select=select_sound):
        if (len(select.values)>0):
            await interaction.response.send_message(content = '', file = file_kanjiImage(searchIndex(select.values[-1],1)),
                                                    embed = embed_kanjiInfo(searchIndex(select.values[-1],1)))
    async def callback_mean(interaction,select=select_mean):
        if (len(select.values)>0):
            await interaction.response.send_message(content = '', file = file_kanjiImage(searchIndex(select.values[-1],1)),
                                                    embed = embed_kanjiInfo(searchIndex(select.values[-1],1)))
    async def callback_next_sound(interaction):
        await interaction.response.edit_message(view = view_kanjiSelectmenu(indexlist_sound,indexlist_mean,page_sound+1,page_mean))
    async def callback_next_mean(interaction):
        await interaction.response.edit_message(view = view_kanjiSelectmenu(indexlist_sound,indexlist_mean,page_sound,page_mean+1))
    async def callback_prev_sound(interaction):
        await interaction.response.edit_message(view = view_kanjiSelectmenu(indexlist_sound,indexlist_mean,page_sound-1,page_mean))
    async def callback_prev_mean(interaction):
        await interaction.response.edit_message(view = view_kanjiSelectmenu(indexlist_sound,indexlist_mean,page_sound,page_mean-1))

    select_sound.callback = callback_sound
    select_mean.callback = callback_mean
    next_sound.callback = callback_next_sound
    next_mean.callback = callback_next_mean
    prev_sound.callback = callback_prev_sound
    prev_mean.callback = callback_prev_mean
    return view

def view_regenButton(diff):
    view = ui.View()
    button = ui.Button(label="다시 생성",style=ButtonStyle.blurple)
    if(diff==-1):
        index = randrange(0,len_jpk)
    else:
        index = randrange(jpkDiffindex[diff+1], jpkDiffindex[diff]+1)

    async def callback(interaction):
        await interaction.channel.send(file = file_kanjiImage(index),
                                        embed = embed_kanjiInfo(index),
                                        view = view_regenButton(diff))
        await interaction.message.delete()
    button.callback = callback
    view.add_item(button)
    return view

'''
@client.command(name = "일본단어")
async def japanese(ctx,*args):
    index = randrange(0,len_jp)
    if len(jpList[index][1])>0:
        string = "# " + jpList[index][0] + " [" + jpList[index][1] + "]" + "\n뜻 : ||" + jpList[index][2] + "||"
    else:
        string = "# " + jpList[index][0] + "\n뜻 : ||" + jpList[index][2] + "||"
    return await ctx.channel.send(string)
'''

@client.tree.command(name="일본한자", description="검색을 통해 일본 한자 정보를 출력합니다")
@app_commands.describe(input="알고자 하는 한자를 직접 입력 / 발음을 영어 혹은 히라가나로 입력")
@app_commands.rename(input="키워드")
async def japankanji(interaction:Interaction, input:str):
    if iskanji(input): #한자일 경우
        index = searchIndex(input,1)
        if index==-1:
            return await interaction.response.send_message(embed=Embed(description="해당 한자를 찾을 수 없습니다."),
                                                            ephemeral=True)
        return await interaction.response.send_message(file = file_kanjiImage(index), 
                                                        embed = embed_kanjiInfo(searchIndex(input,1)))
    elif ishangeul(input): #한글일 경우
        return await interaction.response.send_message(embed=Embed(description="이건 한글입니다."),
                                                        ephemeral=True)
    else: #히라가나,영어, 기타 입력일 경우
        if input.encode().isalpha():
            string = engtohira(input)
            if string == -1:
                return await interaction.response.send_message(embed=Embed(description="올바르지 않은 입력입니다."),
                                                                ephemeral=True)
        elif ishiragana(input):
            string = input
        else:
            return await interaction.response.send_message(embed=Embed(description="올바르지 않은 입력입니다."),
                                                            ephemeral=True)
        indexlist_sound = searchIndexlist(string,2)
        indexlist_mean = searchIndexlist(string,3)
        if(len(indexlist_sound) + len(indexlist_mean) == 1):
            if len(indexlist_sound) == 1:
                return await interaction.response.send_message(file = file_kanjiImage(indexlist_sound[0]), 
                                                embed = embed_kanjiInfo(indexlist_sound[0]))
            else:
                return await interaction.response.send_message(file = file_kanjiImage(indexlist_mean[0]), 
                                                embed = embed_kanjiInfo(indexlist_mean[0]))
        elif(len(indexlist_sound) + len(indexlist_mean) == 0):
            return await interaction.response.send_message(embed=Embed(description="검색된 한자가 없습니다."),
                                                            ephemeral=True)
        else:
            return await interaction.response.send_message(embed=Embed(title=f"검색 결과 - {input}",
                                                                                description="한자를 선택해주세요."),
                                                        view=view_kanjiSelectmenu(indexlist_sound,indexlist_mean,1,1),
                                                        ephemeral=True)

@client.tree.command(name = "일본한자_랜덤", description="무작위의 일본 한자 정보를 출력합니다. 난이도를 설정할 수 있습니다")
@app_commands.describe(select="난이도를 선택해주세요")
@app_commands.rename(select="난이도")
@app_commands.choices(select=[
    Choice(name="모두", value=-1),
    Choice(name="小1 (10급)", value=0),
    Choice(name="小2 (9급)", value=1),
    Choice(name="小3 (8급)", value=2),
    Choice(name="小4 (7급)", value=3),
    Choice(name="小5 (6급)", value=4),
    Choice(name="小6 (5급)", value=5),
    Choice(name="中学 (4급)", value=6),
    Choice(name="中学 (3급)", value=7),
    Choice(name="中学 (준2급)", value=8),
    Choice(name="中学 (2급)", value=9)
])
async def japankanji_rand(interaction:Interaction, select:Choice[int]):
    if (select==-1):
        index = randrange(0,len_jpk)
    else:
        index = randrange(jpkDiffindex[select.value+1], jpkDiffindex[select.value]+1)
    return await interaction.response.send_message(file = file_kanjiImage(index), 
                                                    embed = embed_kanjiInfo(index),
                                                    view = view_regenButton(select.value))

@client.tree.command(name = "일본어", description="영어로 입력된 일본어 발음을 일본어로 출력합니다")
@app_commands.describe(input="일본어 발음을 영어로 입력")
@app_commands.rename(input="입력")
async def japanese(interaction:Interaction, input:str):
    result = engtohira(input)
    if result==-1:
        return await interaction.response.send_message(embed=Embed(description="올바르지 않은 입력입니다."),
                                                       ephemeral=True)
    return await interaction.response.send_message(embed=Embed(title=f"일본어 - {input}",
                                                                description=result))