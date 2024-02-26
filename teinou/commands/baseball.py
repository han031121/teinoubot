'''
숫자 야구 기능
'''

from random import sample
from teinou import client
from discord import app_commands, Embed, Interaction, ui, ButtonStyle

answerDict = {}

def baseballCount(ans, input):
    ball=0
    strike=0
    for i in range(len(ans)):
        for j in range(len(ans)):
            if(input[i]==ans[j]):
                if(i!=j):
                    ball+=1
                if(i==j):
                    strike+=1
                break
    return [ball,strike]

def startButton():
    view = ui.View()
    Button = ui.Button(label="시작",style=ButtonStyle.green)
    async def callback(interaction:Interaction):
        await interaction.response.send_message(embed=Embed(title="숫자야구 - 시작",
                                                    description=f"{interaction.user}님이 숫자야구를 시작하였습니다.\n정답이 생성되었습니다."))
        answerDict[interaction.channel_id] = sample(range(0, 10), 3) #answer generate
    Button.callback=callback
    view.add_item(Button)
    return view

def endButton():
    view = ui.View()
    Button = ui.Button(label="종료",style=ButtonStyle.red)
    async def callback(interaction:Interaction):
        await interaction.response.send_message(embed=Embed(title="숫자야구 - 종료",
                                                    description=f"{interaction.user}님이 숫자야구를 종료하였습니다.\n정답은 {answerDict[interaction.channel_id]}입니다."))
        del answerDict[interaction.channel_id]
    Button.callback=callback
    view.add_item(Button)
    return view

@client.tree.command(name="숫자야구", description="숫자야구를 실행합니다")
@app_commands.describe(input="세 자리 숫자를 입력해주세요. 이 값을 제공하지 않으면 숫자야구를 시작하거나 종료합니다.")
@app_commands.rename(input="입력")
async def baseball(interaction:Interaction, input:str|None):
    if (input==None):
        if (interaction.channel_id in answerDict):
            return await interaction.response.send_message(embed=Embed(title="숫자야구 - 종료",
                                                                       description="숫자야구가 진행중입니다. 종료하시겠습니까?"),
                                                            view=endButton(), ephemeral=True)
        else:
            return await interaction.response.send_message(embed=Embed(title="숫자야구 - 시작",
                                                                       description="숫자야구를 시작하시겠습니까?"),
                                                            view=startButton(), ephemeral=True)
    if (interaction.channel_id in answerDict == False):
        return await interaction.response.send_message(embed=Embed(title="숫자야구 - 오류", 
                                                                   description="아직 시작되지 않았습니다.\n명령어 실행 시 입력값을 제공하지 않으면 시작 또는 종료합니다."),
                                                        ephemeral=True)
    elif (input.isdigit==False or len(input)!=3):
        return await interaction.response.send_message(embed=Embed(title="숫자야구 - 오류", 
                                                                   description="세 자리 숫자를 입력해주세요."),
                                                        ephemeral=True)
    answer = answerDict[interaction.channel_id]
    inputAns=[int(int(input)/100), int(int(input)%100/10), int(input)%10]
    baseballList = baseballCount(answer, inputAns) #[ball,strike]
    inputAns_str = "".join(str(num) for num in inputAns)

    if (answer == inputAns):
        del answerDict[interaction.channel_id]
        return await interaction.response.send_message(embed=Embed(title=f"숫자야구 - {inputAns_str}",
                                                                   description=f"{interaction.user}님이 정답을 맞췄습니다.\n숫자야구를 종료합니다."))
    else:
        return await interaction.response.send_message(embed=Embed(title=f"숫자야구 - {inputAns_str}",
                                                               description=f"{baseballList[0]} ball, {baseballList[1]} strike"))