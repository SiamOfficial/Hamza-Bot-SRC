import discord
from discord import app_commands
from discord.ext import commands
import json
import aiohttp
from utilities.functions import get_dua
import random
import typing
class DuaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    with open('duas.json', 'r', encoding='utf-8') as f:
        duas = json.load(f)
            
    async def dua_autocompletion(self, interaction: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
        data = []
        for dua in self.duas:
                name = dua['name']
                index = dua['index']
                duaname = f'({str(index)}) {name}'
                if current.lower() in duaname.lower():
                    data.append(app_commands.Choice(name=duaname, value=str(index)))
        return data[:25]

    dua = app_commands.Group(name='dua', description='Dua related commands')
#DUA    
    @dua.command(name='search', description='Gives you a specific dua from a specific topic/action.')
    @app_commands.describe(topic='Name of the topic/action')
    @app_commands.autocomplete(topic=dua_autocompletion)
    async def search(self, interaction: discord.Interaction, topic: str):
        await interaction.response.defer()
        index = int(topic)
        dua_data = await get_dua(index=index)
        embed = discord.Embed(title=f'({dua_data["index"]}) {dua_data["name"]}', description=f'''```{dua_data["arabic"]}```
```{dua_data["english"]}```''')
        await interaction.followup.send(embed=embed)
#RDUA
    @dua.command(name='random', description='Get a random dua for an action/topic.')
    async def rdua(self, interaction: discord.Interaction):
        await interaction.response.defer()
        index = random.randint(1, len(self.duas))
        dua_data = await get_dua(index=index)
        embed = discord.Embed(title=f'({dua_data["index"]}) {dua_data["name"]}', description=f'''```{dua_data["arabic"]}"```
```{dua_data["english"]}```''')
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(DuaCog(bot))