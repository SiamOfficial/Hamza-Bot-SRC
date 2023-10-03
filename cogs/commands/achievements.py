import discord
from discord.ext import commands
from discord import app_commands
from utilities.pagination import AchievementsPaginator

class AchievementsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='achievements', description='See all of the Hamza\'s achievements.')
    async def achievements(self, interaction: discord.Interaction):
        await interaction.response.defer()
        paginator = AchievementsPaginator(self.bot)
        await paginator.start(interaction)

async def setup(bot):
    await bot.add_cog(AchievementsCog(bot))