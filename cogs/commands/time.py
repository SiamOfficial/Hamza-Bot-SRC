import discord
from discord import app_commands
from discord.ext import commands
from utilities.functions import get_prayer_times
import json
import typing

class TimeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    time = app_commands.Group(name='time', description='Time related commands.')
    @time.command(name='prayers', description='Get timings of different prayers of a city.')
    @app_commands.describe(city='Name of the city.')
    async def prayers(self, interaction: discord.Interaction, city: str):
        try:
            await interaction.response.defer()
            times = await get_prayer_times(city=city)
            embed = discord.Embed(title=f'{city.title()} prayer times', description=f'Here are the prayer times of {city.title()}.')
            embed.add_field(name='Fajr', value=times['timings']['Fajr'])
            embed.add_field(name='Dhuhr', value=times['timings']['Dhuhr'])
            embed.add_field(name='Asr', value=times['timings']['Asr'])
            embed.add_field(name='Maghrib', value=times['timings']['Maghrib'])
            embed.add_field(name='Isha', value=times['timings']['Isha'])
            embed.set_author(icon_url=self.bot.user.avatar, name=times['date']['readable'])
            await interaction.followup.send(embed=embed)
        except Exception as e:
            print(e)
            await interaction.followup.send('You have input a wrong reference!')

async def setup(bot):
    await bot.add_cog(TimeCog(bot))
