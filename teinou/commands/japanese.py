from teinou.client import deletable_command
from random import randrange

TEXT_PATH = "assets/teinoubot_texts/"
jpList = []
jpkList = []
len_jp = 0
len_jpk = 0
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

@deletable_command(name = "일본어")
async def japanese(ctx,*args):
    index = randrange(0,len_jp)
    if len(jpList[index][1])>0:
        string = "# " + jpList[index][0] + " [" + jpList[index][1] + "]" + "\n뜻 : ||" + jpList[index][2] + "||"
    else:
        string = "# " + jpList[index][0] + "\n뜻 : ||" + jpList[index][2] + "||"
    return await ctx.channel.send(string)

@deletable_command(name = "일본한자")
async def japankanji(ctx,*args):
    index = randrange(0,len_jpk)
    string = "# " + jpkList[index][1] + "\n音 : " + jpkList[index][2] + "\n訓 : " + jpkList[index][3] + "\n韓 : " + jpkList[index][0]
    return await ctx.channel.send(string)