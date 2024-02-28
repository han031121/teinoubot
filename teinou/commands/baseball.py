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
    Button_3 = ui.Button(label="시작(3개)",style=ButtonStyle.green)
    Button_4 = ui.Button(label="시작(4개)",style=ButtonStyle.green)
    async def callback_3(interaction:Interaction):
        await interaction.response.send_message(embed=Embed(title="숫자야구 - 시작",
                                                    description=f"**{interaction.user}**님이 숫자야구를 시작하였습니다.\n**세 자리**의 정답이 생성되었습니다."))
        answerDict[interaction.channel_id] = sample(range(0, 10), 3) #answer generate
    async def callback_4(interaction:Interaction):
        await interaction.response.send_message(embed=Embed(title="숫자야구 - 시작",
                                                    description=f"**{interaction.user}**님이 숫자야구를 시작하였습니다.\n**네 자리**의 정답이 생성되었습니다."))
        answerDict[interaction.channel_id] = sample(range(0, 10), 4) #answer generate
    Button_3.callback=callback_3
    Button_4.callback=callback_4
    view.add_item(Button_3)
    view.add_item(Button_4)
    return view

def endButton():
    view = ui.View()
    Button = ui.Button(label="종료",style=ButtonStyle.red)
    async def callback(interaction:Interaction):
        answer = "".join(str(num) for num in answerDict[interaction.channel_id])
        await interaction.response.send_message(embed=Embed(title="숫자야구 - 종료",
                                                    description=f"**{interaction.user}**님이 숫자야구를 종료하였습니다.\n정답은 **{answer}**입니다."))
        del answerDict[interaction.channel_id]
    Button.callback=callback
    view.add_item(Button)
    return view

@client.tree.command(name="숫자야구", description="숫자야구를 실행합니다")
@app_commands.describe(input="세 자리 혹은 네 자리 숫자를 입력해주세요. 이 값을 제공하지 않으면 숫자야구를 시작하거나 종료합니다.")
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
    if not (interaction.channel_id in answerDict):
        return await interaction.response.send_message(embed=Embed(title="숫자야구 - 오류", 
                                                                   description="아직 시작되지 않았습니다.\n명령어 실행 시 입력값을 제공하지 않으면 시작 또는 종료합니다."),
                                                        ephemeral=True)
    answer = answerDict[interaction.channel_id]
    if (input.isdigit==False or len(input)!=len(answer)):
        if(len(answer)==3):
            return await interaction.response.send_message(embed=Embed(title="숫자야구 - 오류", 
                                                                       description="세 자리 숫자를 입력해주세요."),ephemeral=True)
        elif(len(answer)==4):
            return await interaction.response.send_message(embed=Embed(title="숫자야구 - 오류", 
                                                                       description="네 자리 숫자를 입력해주세요."),ephemeral=True)
    if (len(answer)==3):
        inputAns=[int(int(input)/100), int(int(input)%100/10), int(input)%10]
    elif (len(answer)==4):
        inputAns=[int(int(input)/1000), int(int(input)%1000/100), int(int(input)%100/10), int(input)%10]

    if (len(set(inputAns))!=len(inputAns)):
        return await interaction.response.send_message(embed=Embed(title="숫자야구 - 오류", 
                                                                    description="숫자를 중복없이 입력해주세요."),ephemeral=True)

    baseballList = baseballCount(answer, inputAns) #[ball,strike]
    inputAns_str = "".join(str(num) for num in inputAns)

    if (answer == inputAns):
        del answerDict[interaction.channel_id]
        return await interaction.response.send_message(embed=Embed(title=f"숫자야구 - {inputAns_str}",
                                                                   description=f"**{interaction.user}**님이 정답을 맞췄습니다.\n숫자야구를 종료합니다."))
    else:
        return await interaction.response.send_message(embed=Embed(title=f"숫자야구 - {inputAns_str}",
                                                               description=f"{baseballList[0]} ball, {baseballList[1]} strike"))