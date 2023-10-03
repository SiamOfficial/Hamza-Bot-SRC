import discord
from discord import app_commands
from discord.ext import commands
import typing
import requests
import json
from utilities.functions import get_chapter_info
import random
class ChapterinfoCog(commands.Cog):
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
    
    chapterinfo = app_commands.Group(name='chapterinfo', description='Chapterlist related commands')
#SEARCH CHAPTERINFO 
    @chapterinfo.command(name='search', description='Gives you the information of the specific chapter.')
    @app_commands.describe(chapter='Name or number of the chapter')
    @app_commands.autocomplete(chapter=chapter_autocompletion)
    async def search(self, interaction: discord.Interaction, chapter: str):
        try:
            index = int(chapter)
        except ValueError:
            index = chapter.split(')')[0][1:]

        chapter_data = await get_chapter_info(index)
        if chapter_data is None:
            await interaction.response.send_message('Chapter not found', ephemeral=True)
            return
        await interaction.response.defer()
        embed = discord.Embed(title=f"({chapter_data['chapter']}) {chapter_data['name']}")
        embed.add_field(name='Arabic', value=chapter_data['arabicname'])
        embed.add_field(name='Meaning', value=chapter_data['englishname'])
        embed.add_field(name='Revelation Place', value=chapter_data['revelation'])
        embed.add_field(name='Number of Verses', value=len(chapter_data['verses']))
        await interaction.followup.send(embed=embed)

#RCHAPTER
    @chapterinfo.command(name='random', description='Get information about a random chapter.')
    async def rchapterinfo(self, interaction: discord.Interaction):
        index = random.randint(1, 114)
        chapter_data = await get_chapter_info(index=index)
        if chapter_data is None:
            await interaction.response.send_message('Chapter not found', ephemeral=True)
            return
        await interaction.response.defer()
        embed = discord.Embed(title=f"({chapter_data['chapter']}) {chapter_data['name']}")
        embed.add_field(name='Arabic', value=chapter_data['arabicname'])
        embed.add_field(name='Meaning', value=chapter_data['englishname'])
        embed.add_field(name='Revelation Place', value=chapter_data['revelation'])
        embed.add_field(name='Number of Verses', value=len(chapter_data['verses']))
        await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(ChapterinfoCog(bot))