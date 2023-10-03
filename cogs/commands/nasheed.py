import discord
from discord import app_commands
from discord.ext import commands
import json
import typing
from utilities.functions import get_nasheed
import asyncio

voice_clients = {}
ffmpeg_options = {'options': '-vn'}
class NasheedCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    with open('nasheeds.json', 'r', encoding='utf-8') as f:
        nasheeds = json.load(f)
            
    async def nasheed_autocompletion(self, interaction: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
        data = []
        for nasheed in self.nasheeds:
            name = nasheed['name']
            index = nasheed['index']
            nasheedname = f'({str(index)}) {name}'
            if current.lower() in nasheedname.lower():
                data.append(app_commands.Choice(name=nasheedname, value=str(index)))
        return data[:25]
    nasheed = app_commands.Group(name='nasheed', description='Nasheed related commands.')

#PLAY ADHAN
    @nasheed.command(name='play', description='Plays a nasheed from a number of different nasheeds.')
    @app_commands.autocomplete(name=nasheed_autocompletion)
    @app_commands.describe(name='Nasheed you want to play')
    async def play(self, interaction: discord.Interaction, name: int):
        await interaction.response.defer()
        nasheed = await get_nasheed(index=name)
        if interaction.user.voice:
            try:
                voice_client = await interaction.user.voice.channel.connect()
                voice_clients[voice_client.guild.id] = voice_client
            except discord.ClientException as e:
                await interaction.followup.send(f'Error connecting to voice channel: {e}')
                return
            try:
                source = discord.FFmpegPCMAudio(nasheed['link'], **ffmpeg_options)
                voice_client.play(source)
                embed = discord.Embed(title=nasheed["name"], description=f'Started playing nasheed in {interaction.user.voice.channel.mention}!')
                embed.set_author(icon_url=self.bot.user.avatar, name=nasheed['author'])
                embed.set_footer(text=f'Nasheed {str(nasheed["index"])} of {len(self.nasheeds)}')
                await interaction.followup.send(embed=embed)
                while True:
                    if not voice_client.is_playing():
                        await asyncio.sleep(1)
                        await voice_client.disconnect()
                        await interaction.channel.send(f'{interaction.user.mention}, nasheed is over!')
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
    await bot.add_cog(NasheedCog(bot))