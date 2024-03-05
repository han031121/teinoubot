from teinou.client import client
from random import randrange
from teinou.kanjilibrary import *
from discord import Interaction, ui, Embed, app_commands, File, SelectOption, ButtonStyle, Color
TEXT_PATH = "assets/teinoubot_texts/"
cncharList = []
len_cnch = 0

with open(TEXT_PATH + "chinese_character_1.txt","r",encoding='UTF8') as f_chinachar:
    tmpList = f_chinachar.readlines()
    for i in range(len(tmpList)):
        cncharList.append(tmpList[i].split("\t")) #{한자}\t{한어병음}
    len_cnch = len(cncharList)

def file_cncharImage(index):
    return File(cncharImage(cncharList[index][0]), filename = "image.png")
def embed_cncharInfo(index): #한자 하나에 대한 설명 embed 반환
    embed = Embed(
        title="중국한자 - " + cncharList[index][0],
        color=Color.red()
    )
    embed.set_thumbnail(url=f"attachment://image.png")
    embed.add_field(name="한어병음",value=cncharList[index][1],inline=True)
    #embed.add_field(name="뜻",value=cncharList[index][1],inline=True)
    return embed

def searchIndexlist(buf): #여러개의 index검색, list반환 (병음 검색 시)
    indexlist = []
    for i in range(0,len_cnch):
        if buf in cncharList[i][1]:
            bufIndex = cncharList[i][1].find(buf)
            if (bufIndex == 0) and (bufIndex+len(buf) == len(cncharList[i][1])): #완벽히 일치
                indexlist.append(i)
            elif (bufIndex == 0): #시작지점에 위치
                if (cncharList[i][1][bufIndex+len(buf)] == ','):
                    indexlist.append(i)
            elif (bufIndex+len(buf) == len(cncharList[i][1])): #끝지점에 위치
                if(cncharList[i][1][bufIndex-1] == ' '):
                    indexlist.append(i)
            elif (cncharList[i][1][bufIndex-1] == ' ' and cncharList[i][1][bufIndex+len(buf)] == ','): #중간에 위치
                indexlist.append(i)
    return indexlist
def searchIndex(buf): #하나의 index검색, 반환 (한자 검색 시)
    for i in range(0,len_cnch):
        if buf in cncharList[i][0]:
            return i
    return -1

def pinyinConvert(string, num):
    engList = ['a','o','e','i','u','ü']
    pinyinList = {'a' : ['ā','á','ǎ','à','a'],
                  'e' : ['ē','é','ě','è','e'],
                  'i' : ['ī','í','ǐ','ì','i'],
                  'o' : ['ō','ó','ǒ','ò','o'],
                  'u' : ['ū','ú','ǔ','ù','u'],
                  'ü' : ['ǖ','ǘ','ǚ','ǜ','ü']}
    targetIndex = -1
    i_index = string.find('i')
    u_index = string.find('u')

    if (i_index>=0 and u_index>=0):
        if (i_index<u_index):
            targetIndex = i_index+1
        else:
            targetIndex = u_index+1
    else:
        for e in engList:
                index = string.find(e)
                if index!=-1:
                    targetIndex = index
                    break

    if(targetIndex==-1):
        return ''
    return string[:targetIndex] + pinyinList[string[targetIndex]][num] + string[targetIndex+1:]

def view_cncharSelectmenu(resultList):
    view = ui.View()
    header = list(resultList.keys())
    select=[]
    options = [[],[],[],[],[]]
    
    for i in range(5):
        options[i] = [SelectOption(label = cncharList[j][0],
            description = cncharList[j][1]) 
            for j in resultList[header[i]]]
    for i in range(5):
        if(len(options[i])==0):
            select.append(select_list(f"{header[i]} : 검색 결과 없음", [SelectOption(label = ".")], True))
        else:
            select.append(select_list(f"{header[i]} : {len(options[i])}개", options[i]))

    async def callback_1(interaction:Interaction):
            await interaction.response.send_message(content='',file=file_cncharImage(searchIndex(select[0].values[-1])),
                                                    embed=embed_cncharInfo(searchIndex(select[0].values[-1])))
    async def callback_2(interaction:Interaction):
            await interaction.response.send_message(content='',file=file_cncharImage(searchIndex(select[1].values[-1])),
                                                    embed=embed_cncharInfo(searchIndex(select[1].values[-1])))
    async def callback_3(interaction:Interaction):
            await interaction.response.send_message(content='',file=file_cncharImage(searchIndex(select[2].values[-1])),
                                                    embed=embed_cncharInfo(searchIndex(select[2].values[-1])))
    async def callback_4(interaction:Interaction):
            await interaction.response.send_message(content='',file=file_cncharImage(searchIndex(select[3].values[-1])),
                                                    embed=embed_cncharInfo(searchIndex(select[3].values[-1])))
    async def callback_none(interaction:Interaction):
            await interaction.response.send_message(content='',file=file_cncharImage(searchIndex(select[4].values[-1])),
                                                    embed=embed_cncharInfo(searchIndex(select[4].values[-1])))
    select[0].callback = callback_1
    select[1].callback = callback_2
    select[2].callback = callback_3
    select[3].callback = callback_4
    select[4].callback = callback_none
    
    for i in range(5):
        view.add_item(select[i])
    return view

@client.command(name="중국한자")
async def chinachar(ctx, args):
    resultList = {}
    for i in range(5):
        pron = pinyinConvert(args,i)
        resultList[pron] = []
        for j in searchIndexlist(pron):
            resultList[pron].append(j)
    await ctx.channel.send(view = view_cncharSelectmenu(resultList))

@client.tree.command(name="중국한자", description="검색을 통해 중국 한자 정보를 출력합니다")
@app_commands.describe(input="알고자 하는 한자를 직접 입력 / 한어병음을 영어로 입력 (j,p,x 뒤에 오지 않는 ü는 yu로 입력)")
@app_commands.rename(input="키워드")
async def chinachar(interaction:Interaction, input:str):
    if input.encode().isalpha(): #알파벳일 경우
        return None
        #한어병음 색인, 모든 성조 결과 표시
    elif iskanji(input): #한자일 경우
        return None
        #한자 색인, 해당 한자 정보 표시
    elif ishangeul(input): #한글일 경우
        return await interaction.response.send_message(embed=Embed(description="이건 한글입니다."),
                                                        ephemeral=True)
    else: #나머지 잘못된 입력
        return await interaction.response.send_message(embed=Embed(description="올바르지 않은 입력입니다."),
                                                            ephemeral=True)