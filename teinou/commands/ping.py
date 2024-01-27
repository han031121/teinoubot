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

class MyView(discord.ui.View):
    @discord.ui.select( # the decorator that lets you specify the properties of the select menu
        placeholder = "Choose a Flavor!", # the placeholder text that will be displayed if nothing is selected
        min_values = 1, # the minimum number of values that must be selected by the users
        max_values = 1, # the maximum number of values that can be selected by the users
        options = [ # the list of options from which users can choose, a required field
            discord.SelectOption(
                label="Vanilla",
                description="Pick this if you like vanilla!"
            ),
            discord.SelectOption(
                label="Chocolate",
                description="Pick this if you like chocolate!"
            ),
            discord.SelectOption(
                label="Strawberry",
                description="Pick this if you like strawberry!"
            )
        ]
    )
    async def select_callback1(self, interaction, select): # the function called when the user is done selecting options
        await interaction.response.send_message(f"Awesome! I like {select.values[0]} too!")
    @discord.ui.select( # the decorator that lets you specify the properties of the select menu
        placeholder = "Choose a Flavor2!", # the placeholder text that will be displayed if nothing is selected
        min_values = 1, # the minimum number of values that must be selected by the users
        max_values = 1, # the maximum number of values that can be selected by the users
        options = [ # the list of options from which users can choose, a required field
            discord.SelectOption(
                label="Vanilla",
                description="Pick this if you like vanilla!"
            ),
            discord.SelectOption(
                label="Chocolate",
                description="Pick this if you like chocolate!"
            ),
            discord.SelectOption(
                label="Strawberry",
                description="Pick this if you like strawberry!"
            )
        ]
    )
    async def select_callback2(self, interaction, select): # the function called when the user is done selecting options
        await interaction.response.send_message(f"Awesome! I like {select.values[0]} too!")

@deletable_command(name="꺼져")
async def reaction(ctx):
        i = random.random()
        if i <= 0.001:
            return await ctx.channel.send("느금")
        elif i <= 0.005:
            return await ctx.channel.send("좆까")
        return await ctx.channel.send("힝힝ㅠㅠ")

@deletable_command(name="꼬맹")
async def reaction(ctx):
    return await ctx.channel.send("꼬맹통",view = Buttons())

@deletable_command(name="힝힝ㅠㅠ")
async def reaction(ctx):
    return await ctx.channel.send("꺼져")
@deletable_command(name = "flavor")
async def reaction(ctx):
    return await ctx.channel.send("select flavor",view = MyView())