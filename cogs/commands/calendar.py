from datetime import datetime, date

import discord
from discord.ext import commands
from hijri_converter import convert
from utilities.converting import convert_to_arabic_number

DATE_INVALID = 'You provided an invalid date!'
GREGORIAN_DATE_OUT_OF_RANGE = '**Sorry, this year is out of range**. The year must be between 1924 and 2077.'
HIJRI_DATE_OUT_OF_RANGE = '**Sorry, this year is out of range**. The year must be between 1343 and 1500.'


class HijriCalendar(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def get_current_hijri():
        hijri = convert.Gregorian.today().to_hijri()
        return f'{hijri.day} {hijri.month_name()} {hijri.year} {hijri.notation(language="en")}'

    @staticmethod
    def get_hijri(gregorian_date: date = None):
        hijri = convert.Gregorian.fromdate(gregorian_date).to_hijri()
        return f'{hijri.month_name()} {hijri.day}, {hijri.year} AH'

    @staticmethod
    def get_gregorian(hijri_date):
        gregorian = convert.Hijri(hijri_date.year, hijri_date.month, hijri_date.day).to_gregorian()
        return f'{gregorian.strftime("%d %B %Y")}'

    async def _convert_to_hijri(self, interaction: discord.Interaction, gregorian_date: str):
        response = interaction.response
        try:
            gregorian_date = datetime.strptime(gregorian_date, "%d-%m-%Y").date()
        except:
            return await response.send_message(DATE_INVALID, ephemeral=True)

        try:
            hijri = self.get_hijri(gregorian_date=gregorian_date)
        except OverflowError:
            return await response.send_message(GREGORIAN_DATE_OUT_OF_RANGE, ephemeral=True)
        await response.defer()
        em = discord.Embed(title='To Hijri',description=hijri)
        em.set_author(icon_url=self.bot.user.avatar, name=gregorian_date)
        await interaction.followup.send(embed=em)

    async def _convert_to_gregorian(self, interaction: discord.Interaction, hijri_date: str):
        response = interaction.response
        try:
            hijri_date = datetime.strptime(hijri_date, "%d-%m-%Y").date()
        except:
            return await response.send_message(DATE_INVALID, ephemeral=True)

        try:
            gregorian = self.get_gregorian(hijri_date=hijri_date)
        except OverflowError:
            return await response.send_message(HIJRI_DATE_OUT_OF_RANGE, ephemeral=True)
        await response.defer()
        em = discord.Embed(title="To Gregorian", description=gregorian)
        em.set_author(icon_url=self.bot.user.avatar, name=hijri_date)
        await interaction.followup.send(embed=em)

    async def _hijridate(self, interaction: discord.Interaction):
        hijri = self.get_current_hijri()
        await interaction.response.defer()
        today = datetime.today().strftime("%d %b %Y")
        em = discord.Embed(title='Today\'s Hijri Date', description=hijri)
        em.set_author(icon_url=self.bot.user.avatar, name=today)
        await interaction.followup.send(embed=em)

    group = discord.app_commands.Group(name="calendar", description="Convert between Gregorian and Hijri dates.")

    @group.command(name="to_hijri", description="Convert gregorian date to hijri date.")
    @discord.app_commands.describe(
        day="The day of the Gregorian date to convert, e.g. 1, 31",
        month="The month of the Gregorian date to convert, e.g. 1 for January",
        year="The year of the Gregorian date to convert, e.g. 2023. Must be between 1924 and 2077."
    )
    async def convert_to_hijri(self, interaction: discord.Interaction, day: discord.app_commands.Range[int, 1, 31], month: discord.app_commands.Range[int, 1, 12],
                               year: discord.app_commands.Range[int, 1924, 2077]):
        await self._convert_to_hijri(interaction, f"{day}-{month}-{year}")

    @group.command(name="to_gregorian", description="Convert hijri date to gregorian date.")
    @discord.app_commands.describe(
        day="The day of the Hijri date to convert, e.g. 1, 29",
        month="The month of the Hijri date to convert, e.g. 9 for Ramaḍān",
        year="The year of the Hijri date to convert, e.g. 1444. Must be between 1343 and 1500."
    )
    async def convert_to_gregorian(self, interaction: discord.Interaction, day: discord.app_commands.Range[int, 1, 30], month: discord.app_commands.Range[int, 1, 12],
                                   year: discord.app_commands.Range[int, 1343, 1500]):
        await self._convert_to_gregorian(interaction, f"{day}-{month}-{year}")

    @group.command(name="hijri_date", description="Get today's hijri date")
    async def hijri_date(self, interaction: discord.Interaction):
        await self._hijridate(interaction)

    @hijri_date.error
    @convert_to_hijri.error
    @convert_to_gregorian.error
    async def on_convert_error(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
        await interaction.response.send_message(f"**Error!** `{error}`", ephemeral=True)


async def setup(bot):
    await bot.add_cog(HijriCalendar(bot))