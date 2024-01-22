from teinou.client import deletable_command
from teinou import ImageParser
import discord

imageParser = ImageParser('nazuna', 50)

class Buttons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Nazuna",style=discord.ButtonStyle.green)
    async def regenButton(self,interaction:discord.Interaction,buttons:discord.ui.Button):
        await interaction.response.send_message(file = imageParser.getRandomItem())

@deletable_command(name = "버튼")
async def button(ctx):
    return await ctx.send("나즈나버튼",view=Buttons())