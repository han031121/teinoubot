import random
import os
from teinou.client import client
import discord
from discord import app_commands, Interaction
from discord.app_commands import Choice

dir = os.getcwd() + "/assets/teinoubot_image/kkomaeng/"
class Buttons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Idle",style=discord.ButtonStyle.blurple)
    async def idleButton(self,interaction:Interaction,button:discord.ui.Button):
        await interaction.response.send_message(file = discord.File(open(dir + "idle.png", "rb")), ephemeral=True)
    @discord.ui.button(label="Reverse",style=discord.ButtonStyle.gray)
    async def reverseButton(self,interaction:Interaction,button:discord.ui.Button):
        await interaction.response.send_message(file = discord.File(open(dir + "reverse.png", "rb")), ephemeral=True)
    @discord.ui.button(label="Happy",style=discord.ButtonStyle.green)
    async def happyButton(self,interaction:Interaction,button:discord.ui.Button):
        await interaction.response.send_message(file = discord.File(open(dir + "happy.png", "rb")), ephemeral=True)
    @discord.ui.button(label="Sad",style=discord.ButtonStyle.red)
    async def sadButton(self,interaction:Interaction,button:discord.ui.Button):
        await interaction.response.send_message(file = discord.File(open(dir + "sad.png", "rb")), ephemeral=True)

@client.tree.command(name="말걸기", description="저능아봇에게 말을 겁니다")
@app_commands.describe(input="저능아봇에게 할 말을 골라주세요")
@app_commands.rename(input="내용")
@app_commands.choices(input=[
    Choice(name="안녕",value=0),
    Choice(name="꼬맹",value=1),
    Choice(name="꺼져",value=2),
    Choice(name="힝힝ㅠㅠ",value=3)
])
async def reaction(interaction:Interaction, input:Choice[int]):
    if (input.value==0):
        await interaction.response.send_message(embed=discord.Embed(title="저능아봇의 대답",
                                                              description=f"안녕하세요 {interaction.user.name}님"),
                                                              ephemeral=True)
    elif (input.value==1):
        await interaction.response.send_message(view = Buttons())
    elif (input.value==2):
        if random.random() <= 0.03:
            await interaction.response.send_message(embed=discord.Embed(title="저능아봇의 대답",
                                                                               description="좆까"),
                                                                               ephemeral=True)
        await interaction.response.send_message(embed=discord.Embed(title="저능아봇의 대답",
                                                                           description="힝힝ㅠㅠ"),
                                                                           ephemeral=True)
    elif (input.value==3):
        await interaction.response.send_message(embed=discord.Embed(title="저능아봇의 대답",
                                                                           description="꺼져"),
                                                                           ephemeral=True)