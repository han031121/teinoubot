from teinou.client import deletable_command
import discord

class Buttons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Button",style=discord.ButtonStyle.green)
    async def regenButton(self,buttons:discord.ui.Button,interaction:discord.Interaction):
        await interaction.response.edit_message(content=f"This is an edited button response!")

@deletable_command(name = "버튼")
async def button(ctx):
    return await ctx.send("This message has buttons!",view=Buttons())