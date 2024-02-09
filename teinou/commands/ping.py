import random
import os
from teinou import client
from teinou.client import deletable_command
import discord

dir = os.getcwd() + "/assets/teinoubot_image/kkomaeng/"
class Buttons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Idle",style=discord.ButtonStyle.blurple)
    async def idleButton(self,interaction:discord.Interaction,buttons:discord.ui.Button):
        await interaction.response.send_message(file = discord.File(open(dir + "idle.png", "rb")))
    @discord.ui.button(label="Reverse",style=discord.ButtonStyle.gray)
    async def reverseButton(self,interaction:discord.Interaction,buttons:discord.ui.Button):
        await interaction.response.send_message(file = discord.File(open(dir + "reverse.png", "rb")))
    @discord.ui.button(label="Happy",style=discord.ButtonStyle.green)
    async def happyButton(self,interaction:discord.Interaction,buttons:discord.ui.Button):
        await interaction.response.send_message(file = discord.File(open(dir + "happy.png", "rb")))
    @discord.ui.button(label="Sad",style=discord.ButtonStyle.red)
    async def sadButton(self,interaction:discord.Interaction,buttons:discord.ui.Button):
        await interaction.response.send_message(file = discord.File(open(dir + "sad.png", "rb")))

@deletable_command(name="꺼져")
async def reaction(ctx):
        i = random.random()
        if i <= 0.005:
            return await ctx.channel.send("좆까")
        return await ctx.channel.send("힝힝ㅠㅠ")

@deletable_command(name="꼬맹")
async def reaction(ctx):
    return await ctx.channel.send("꼬맹통",view = Buttons())

@deletable_command(name="힝힝ㅠㅠ")
async def reaction(ctx):
    return await ctx.channel.send("꺼져")