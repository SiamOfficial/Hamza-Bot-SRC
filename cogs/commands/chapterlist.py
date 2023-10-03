import discord
from discord import app_commands
from discord.ext import commands

class ChapterlistCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='chapterlist', description='Gives you a list of all the chapters of Quran with its number.')
    async def chapterlist(self, interaction: discord.Interaction):
        emb = discord.Embed(title='Chapter List')
        emb.set_image(url='https://go4quiz.com/wp-content/uploads/List-of-114-Surahs-go4quiz.jpg')
        emb.set_footer(text='List is made by go4quiz.com')
        await interaction.response.send_message(embed=emb)

async def setup(bot):
    await bot.add_cog(ChapterlistCog(bot))