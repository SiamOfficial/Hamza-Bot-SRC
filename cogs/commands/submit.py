import discord
from discord import app_commands
from discord.ext import commands
from utilities.submission import Nasheed_Submission, Adhan_Submission

class SubmitCog(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot

    submit = app_commands.Group(name='submit', description='Submit related commands.')

#SUBMIT NASHEED
    @submit.command(name='nasheed', description='Submit a copyright-free nasheed in the Bot.')
    async def nasheed(self, interaction: discord.Interaction):
        await interaction.response.send_modal(Nasheed_Submission(self.bot))

#SUBMIT ADHAN
    @submit.command(name='adhan', description='Submit a copyright-free adhan in the Bot.')
    async def nasheed(self, interaction: discord.Interaction):
        await interaction.response.send_modal(Adhan_Submission(self.bot))

async def setup(bot):
    await bot.add_cog(SubmitCog(bot))