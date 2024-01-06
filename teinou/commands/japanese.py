from teinou.client import deletable_command
from random import randrange
import re

def iskanji(string):
    kanji = r'[㐀-䶵一-鿋豈-頻]'
    if re.fullmatch(kanji,string):
        return True
    return False
def ishiragana(string):
    hiragana = r'[ぁ-ゟ]'
    strlist = re.findall(hiragana,string)
    if len(string)!=len(strlist):
            return False
    for i in range(len(strlist)):
        if string[i]!=strlist[i]:
            return False
    return True

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
    else:
        if args[0].isdecimal():
            try:
                index = randrange(jpkDiffindex[int(args[0])],jpkDiffindex[int(args[0])-1])
                return await ctx.channel.send(makeKanjiInfo(index))
            except IndexError:
                return await ctx.channel.send("올바른 난이도값을 입력해주세요. (1~5)")
        elif iskanji(args[0]):
            for index in range(len_jpk-1,-1,-1):
                if jpkList[index][1] == args[0]:
                    return await ctx.channel.send(makeKanjiInfo(index))
            return await ctx.channel.send("해당 한자를 찾을 수 없습니다.")
        elif ishiragana(args[0]):
            indexlist_sound = searchIndexlist(args[0],2)
            indexlist_mean = searchIndexlist(args[0],3)
            return await ctx.channel.send(makeKanjiSearch(indexlist_sound,indexlist_mean))