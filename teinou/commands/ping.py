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
        await interaction.channel.send(file = discord.File(open(dir + "idle.png", "rb")))
        await interaction.message.delete()
    @discord.ui.button(label="Reverse",style=discord.ButtonStyle.gray)
    async def reverseButton(self,interaction:discord.Interaction,buttons:discord.ui.Button):
        await interaction.channel.send(file = discord.File(open(dir + "reverse.png", "rb")))
        await interaction.message.delete()
    @discord.ui.button(label="Happy",style=discord.ButtonStyle.green)
    async def happyButton(self,interaction:discord.Interaction,buttons:discord.ui.Button):
        await interaction.channel.send(file = discord.File(open(dir + "happy.png", "rb")))
        await interaction.message.delete()
    @discord.ui.button(label="Sad",style=discord.ButtonStyle.red)
    async def sadButton(self,interaction:discord.Interaction,buttons:discord.ui.Button):
        await interaction.channel.send(file = discord.File(open(dir + "sad.png", "rb")))
        await interaction.message.delete()

@deletable_command(name="꺼져")
async def reaction(ctx):
        i = random.random()
        if i <= 0.005:
            return await ctx.channel.send(embed=discord.Embed(description="좆까"))
        return await ctx.channel.send(embed=discord.Embed(description="힝힝ㅠㅠ"))

@deletable_command(name="꼬맹")
async def reaction(ctx):
    return await ctx.channel.send(embed=discord.Embed(description="꼬맹통"),view = Buttons())

@deletable_command(name="힝힝ㅠㅠ")
async def reaction(ctx):
    return await ctx.channel.send(embed=discord.Embed(description="꺼져"))