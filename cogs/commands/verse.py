import discord
from discord import app_commands
from discord.ext import commands
import typing
import aiohttp
import requests
import random
from utilities.functions import get_verse, get_chapter_info, get_author_info, get_verse_recitation, get_recitor_info
import json
import asyncio
from utilities.converting import convert_to_arabic_number
voice_clients = {}
ffmpeg_options = {'options': '-vn'}
class VerseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def recitor_autocompletion(self, interaction: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
        data = []
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.quran.com/api/v4/resources/recitations?language=en') as response:
                if response.ok:
                    deta = await response.json()
                    for i in range(len(deta["recitations"])):
                        name = deta["recitations"][i]['reciter_name']
                        style = deta["recitations"][i]['style']
                        id = deta["recitations"][i]['id']
                        comname = f'{name} ({style})'
                        if current.lower() in comname.lower():
                            data.append(app_commands.Choice(name=comname, value=str(id)))
        return data[:25]
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
    async def translation_autocompletion(self, interaction: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
        data = []
        url = 'https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions.json'
        response = requests.get(url)
        if response.ok:
            authors = response.json()
            for author in authors.values():
                name = author['author']
                lang = author['language']
                authorname = author['name']
                if 'la' in authorname:
                    completename = f'{name} ({lang}) (Roman)'
                else:
                    completename = f'{name} ({lang})'
                if current.lower() in completename.lower():
                        data.append(app_commands.Choice(name=completename, value=authorname))
        return data[:25]

    verse = app_commands.Group(name='verse', description='Verse related commands.')  
#GET RVERSE
    @verse.command(name='random', description='Get a random verse from a random chapter.')
    @app_commands.autocomplete(translation=translation_autocompletion)
    @app_commands.describe(translation='Choose one of the 90+ languages with 400+ editions (Showing 25 at once)')
    async def rverse(self, interaction: discord.Interaction, translation: str):
        try:
            chapter = random.randint(1, 114)
            chapterdata = await get_chapter_info(index=int(chapter))
            verse = random.randint(1, len(chapterdata["verses"]))
            await interaction.response.defer()
            versedata = await get_verse(chapter=int(chapter), verse=verse, author=translation)
            versearabicdata = await get_verse(chapter=int(chapter), verse=verse, author='ara-quranacademy')
            authordata = await get_author_info(name=translation)
            arabic = convert_to_arabic_number(f'{chapter}:{verse}')
            embed = discord.Embed(title=f'{chapter}:{verse} ({chapterdata["name"]}) | {arabic} ({chapterdata["arabicname"]})', description=f'''```{versearabicdata["text"]}```
```{versedata["text"]}```''')
            embed.add_field(name='Information', value=f'''**Translation:** {authordata['language']}
**Revelation Place:** {chapterdata['revelation']}''')
            embed.set_author(icon_url=self.bot.user.avatar, name=authordata['author'])
            embed.set_footer(text=f"Verse {verse} of {len(chapterdata['verses'])}")
            embed.set_image(url=f'https://hamzabot.me/everyayah.com/{chapter}_{verse}.png')
            await interaction.followup.send(embed=embed)
        except:
            await interaction.followup.send('You provided an invalid reference!', ephemeral=True)

#SEARCH VERSE
    @verse.command(name='search', description='Gives you a specific verse from a specific chapter.')
    @app_commands.autocomplete(chapter=chapter_autocompletion, translation=translation_autocompletion)
    @app_commands.describe(chapter='Number/name of the chapter', verse='Number of the verse', translation='Choose one of the 90+ languages with 400+ editions (Showing 25 at once)')
    async def search(self, interaction: discord.Interaction, chapter: str, verse: int, translation: str):
        try:
            await interaction.response.defer()
            versedata = await get_verse(chapter=int(chapter), verse=verse, author=translation)
            versearabicdata = await get_verse(chapter=int(chapter), verse=verse, author='ara-quranacademy')
            chapterdata = await get_chapter_info(index=int(chapter))
            authordata = await get_author_info(name=translation)
            arabic = convert_to_arabic_number(f'{chapter}:{verse}')
            embed = discord.Embed(title=f'{chapter}:{verse} ({chapterdata["name"]}) | {arabic} ({chapterdata["arabicname"]})', description=f'''```{versearabicdata["text"]}```
```{versedata["text"]}```''')
            embed.add_field(name='Information', value=f'''**Translation:** {authordata['language']}
**Revelation Place:** {chapterdata['revelation']}''')
            embed.set_author(icon_url=self.bot.user.avatar, name=authordata['author'])
            embed.set_footer(text=f"Verse {verse} of {len(chapterdata['verses'])}")
            embed.set_image(url=f'https://hamzabot.me/everyayah.com/{chapter}_{verse}.png')
            await interaction.followup.send(embed=embed)
        except:
            await interaction.followup.send('You provided an invalid reference!', ephemeral=True)

#RECITE VERSE
    @verse.command(name='recite', description='Recites a verse from a chapter with your preferred recitor.')
    @app_commands.autocomplete(chapter=chapter_autocompletion, reciter=recitor_autocompletion)
    @app_commands.describe(chapter='Name/number of the chapter', verse="Number of the verse.", reciter='Reciter with their style.')
    async def recite(self, interaction: discord.Interaction, chapter: int, verse: int, reciter: int):
        await interaction.response.defer()
        verse_recite = await get_verse_recitation(chapter=chapter, verse=verse, recitor=reciter)
        reciter_info = await get_recitor_info(id=reciter)
        chapterdata = await get_chapter_info(index=chapter)
        if interaction.user.voice:
            try:
                voice_client = await interaction.user.voice.channel.connect()
                voice_clients[voice_client.guild.id] = voice_client
            except discord.ClientException as e:
                await interaction.followup.send(f'Error connecting to voice channel: {e}')
                return
            try:
                source = discord.FFmpegPCMAudio(f'https://audio.qurancdn.com/{verse_recite["url"]}', **ffmpeg_options)
                voice_client.play(source)
                arabic = convert_to_arabic_number(f'{chapter}:{verse}')
                embed = discord.Embed(title=f'{chapter}:{verse} ({chapterdata["name"]}) | {arabic} ({chapterdata["arabicname"]})', description=f'Started reciting verse {str(verse)} of {chapterdata["name"]} in {interaction.user.voice.channel.mention}!')
                embed.set_author(icon_url=self.bot.user.avatar, name=reciter_info['reciter_name'])
                embed.add_field(name='Information', value=f'''**Revelation Place:** {chapterdata['revelation']}''')
                embed.set_footer(text=f'Verse {verse} of {len(chapterdata["verses"])}')
                embed.set_image(url=f'https://hamzabot.me/everyayah.com/{chapter}_{verse}.png')
                await interaction.followup.send(embed=embed)
                while True:
                    if not voice_client.is_playing():
                        await asyncio.sleep(1)
                        await voice_client.disconnect()
                        await interaction.channel.send(f'{interaction.user.mention}, reciting is over!')
                        break
                    elif len(voice_client.channel.members) == 1:
                        await asyncio.sleep(1)
                        await voice_client.disconnect()
                        await interaction.channel.send(f'Left {voice_client.channel.mention}, as there are no members in it!')
                        break
                    await asyncio.sleep(1)
            except Exception as e:
                print(e)
                await interaction.followup.send(f'Error playing audio: {e}')
        else:
            await interaction.followup.send('You need to be in a voice channel to use this command.') 

async def setup(bot):
    await bot.add_cog(VerseCog(bot))