import discord
from discord import app_commands
from discord.ext import commands
import json
import typing
from utilities.functions import get_adhan
import asyncio

voice_clients = {}
ffmpeg_options = {'options': '-vn'}
class AdhanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    with open('adhan.json', 'r', encoding='utf-8') as f:
        adhans = json.load(f)
            
    async def adhan_autocompletion(self, interaction: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
        data = []
        for adhan in self.adhans:
            name = adhan['name']
            index = adhan['index']
            adhanname = f'({str(index)}) {name}'
            if current.lower() in adhanname.lower():
                data.append(app_commands.Choice(name=adhanname, value=str(index)))
        return data[:25]
    adhan = app_commands.Group(name='adhan', description='Adhan related commands.')

#PLAY ADHAN
    @adhan.command(name='play', description='Plays an adhan from a number of different adhans.')
    @app_commands.autocomplete(type=adhan_autocompletion)
    @app_commands.describe(type='Type of adhan you want to play')
    async def play(self, interaction: discord.Interaction, type: int):
        await interaction.response.defer()
        adhan = await get_adhan(index=type)
        if interaction.user.voice:
            try:
                voice_client = await interaction.user.voice.channel.connect()
                voice_clients[voice_client.guild.id] = voice_client
            except discord.ClientException as e:
                await interaction.followup.send(f'Error connecting to voice channel: {e}')
                return
            try:
                source = discord.FFmpegPCMAudio(adhan['link'], **ffmpeg_options)
                voice_client.play(source)
                embed = discord.Embed(title=adhan["name"], description=f'Started playing adhan in {interaction.user.voice.channel.mention}!')
                embed.set_author(icon_url=self.bot.user.avatar, name=adhan['author'])
                embed.set_footer(text=f'Adhan {str(adhan["index"])} of {len(self.adhans)}')
                await interaction.followup.send(embed=embed)
                while True:
                    if not voice_client.is_playing():
                        await asyncio.sleep(1)
                        await voice_client.disconnect()
                        await interaction.channel.send(f'{interaction.user.mention}, adhan is over!')
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
    await bot.add_cog(AdhanCog(bot))