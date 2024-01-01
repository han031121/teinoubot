from teinou.client import deletable_command
from random import randrange

TEXT_PATH = "assets/teinoubot_texts/"
jpList = []
jpkList = []
len_jp = 0; len_jpk = 0; 
jpkDiff = [2135,1895,1493,1109,512,0] #난이도가 구분되는 index
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
        try:
            if len(args) == 1:
                index = randrange(jpkDiff[int(args[0])],jpkDiff[int(args[0])-1])
        except ValueError:
            return await ctx.channel.send("올바른 난이도값을 입력해주세요. (1~5)")
        except IndexError:
            return await ctx.channel.send("올바른 난이도값을 입력해주세요. (1~5)")

    string = "# " + jpkList[index][1] + "\n音 : " + jpkList[index][2] + "\n訓 : " + jpkList[index][3] + "\n韓 : " + jpkList[index][0]
    return await ctx.channel.send(string)