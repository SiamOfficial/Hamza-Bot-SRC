import discord
from discord import app_commands
from discord.ext import commands
import requests
import asyncio
import json

class QuoteCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    quote = app_commands.Group(name='quote', description='Quote related commands')
#RQUOTE    
    @quote.command(name='random', description='Get a random islamic quote that might motivate you.')
    async def rquote(self, interaction: discord.Interaction):
        await interaction.response.defer()
        url = 'https://api.islamiq.me/rquote?API_KEY=SheikhNeverHelpsMeAtStudies'
        response = requests.get(url)
        if response.ok:
            data = response.json()
            index = data['index']
            text = data['text']
            author = data['author']
        author = author.replace('— ', '')
        embed = discord.Embed(title=author, description=f'''```{text}```''')
        embed.set_footer(text=f'Quote {str(index)}')
        await interaction.followup.send(embed=embed)

async def setup(bot):
    await  bot.add_cog(QuoteCog(bot))