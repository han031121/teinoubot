from teinou import ImageParser
from teinou.client import client
from discord import app_commands, Embed, Color, Interaction
from discord.app_commands import Choice

embedColors = {
    "nazuna":Color.from_rgb(163,142,137),
    "ryo":Color.from_rgb(70,108,165)
}

@client.tree.command(name="이미지", description="어떤 그림을 출력합니다")
@app_commands.describe(select="출력하고자 하는 것을 선택하세요")
@app_commands.rename(select="캐릭터")
@app_commands.choices(select=[
    Choice(name="나즈나", value="nazuna"),
    Choice(name="료",value="ryo")
])
async def randimage(interaction:Interaction, select:Choice[str]):
    try:
        file = ImageParser(select.value, 30).getRandomItem()
    except:
        return await interaction.response.send_message(embed=Embed(title=select.name, description="미구현 상태입니다."))
    embed = Embed(title=select.name, color=embedColors[select.value])
    embed.set_image(url=f"attachment://image.png")
    return await interaction.response.send_message(file=file, embed=embed)