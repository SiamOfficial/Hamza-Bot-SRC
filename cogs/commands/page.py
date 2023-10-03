import discord
from discord import app_commands
from discord.ext import commands
import random
from utilities.converting import convert_to_arabic_number
from utilities.pagination import PagePaginator
class PageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    page = app_commands.Group(name='page', description='Page related commands')
#SEARCH PAGE
    @page.command(name='search', description='Search for a page of the Quran')
    @app_commands.describe(page='Number of the page (must be between 1 - 604)')
    async def search(self, interaction: discord.Interaction, page: app_commands.Range[int, 1, 604]):
        try:
            await interaction.response.defer()
            embed = discord.Embed(title=f'Page {str(page)} | صفحة {convert_to_arabic_number(str(page))}')
            embed.set_author(icon_url=self.bot.user.avatar, name='Pages by zeyadetman')
            embed.set_image(url=f'https://hamzabot.me/zeyadetman/{str(page)}.jpg')
            embed.set_footer(text=f'Page {str(page)} of 604 pages')
            await interaction.followup.send(embed=embed)

        except:
            await interaction.followup.send('You provided an invalid reference!')

#ALL PAGES
    @page.command(name='all', description='Get the whole Quran')
    async def all(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer()
            paginator = PagePaginator(self.bot, interaction.user)
            await paginator.start(interaction)
        except Exception as e:
            await interaction.followup.send(e)


#RANDOM PAGE
    @page.command(name='random', description='Get a random page of the Quran')
    async def search(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer()
            page = random.randint(1, 604)
            embed = discord.Embed(title=f'Page {str(page)} | صفحة {convert_to_arabic_number(str(page))}')
            embed.set_author(icon_url=self.bot.user.avatar, name='Pages by zeyadetman')
            embed.set_image(url=f'https://hamzabot.me/zeyadetman/{str(page)}.jpg')
            embed.set_footer(text=f'Page {str(page)} of 604 pages')
            await interaction.followup.send(embed=embed)

        except:
            await interaction.followup.send('You provided an invalid reference!')

async def setup(bot):
    await bot.add_cog(PageCog(bot))