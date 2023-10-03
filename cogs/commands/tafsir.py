import discord
from discord import app_commands
from discord.ext import commands
from utilities.pagination import TafsirPaginator
from utilities.functions import get_tafsir, get_chapter_info
import random
from utilities.converting import convert_to_arabic_number
import typing
import requests
import re
import html
import json
class TafsirCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    async def chapter_autocompletion(self, interaction: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
        data = []
        with open('chapters.json', 'r', encoding='utf-8') as f:
            chapters = json.load(f)
            for chapter in chapters:
                name = chapter['name']
                index = chapter['index']
                chapname = f'({str(index)}) {name}'
                if current.lower() in chapname.lower():
                    data.append(app_commands.Choice(name=chapname, value=str(index)))
        return data[:25]
    async def tafsir_autocompletion(self, interaction: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
        data = []
        url = "https://api.quran.com/api/v3/options/tafsirs"
        response = requests.get(url)
        if response.ok:
            data = response.json()
            tafsirs = data['tafsirs']
        data = []
        for tafsir in tafsirs:
            lang = tafsir['language_name']
            mufassir = tafsir['name']
            name = f'{mufassir} ({lang.title()})'
            if current.lower() in mufassir.lower() or current.lower() in lang.lower():
                data.append(app_commands.Choice(name=name, value=tafsir['slug']))
        # slice the data list by 25
        return data[:25]
    
    tafsir = app_commands.Group(name='tafsir', description='Tafsir related commands.')
#TAFSIR
    @tafsir.command(name='search', description='Search tafsir for a specific verse of a chapter.')
    @app_commands.autocomplete(chapter=chapter_autocompletion, mufassir=tafsir_autocompletion)
    @app_commands.describe(chapter='Name/number of the chapter', verse='Number of the verse', mufassir='Select a mufassir for tafsir')
    async def search(self, interaction: discord.Interaction, chapter: int, verse: int, mufassir: str):
      try:
        await interaction.response.defer()
        paginator = TafsirPaginator(self.bot, chapter, verse, mufassir, interaction.user)
        await paginator.start(interaction)
      except:
          await interaction.followup.send('You have input a wrong reference!')

async def setup(bot):
    await bot.add_cog(TafsirCog(bot))