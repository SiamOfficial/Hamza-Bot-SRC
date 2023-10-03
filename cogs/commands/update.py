import discord
from discord import app_commands
from discord.ext import commands
import asqlite

class MyView(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(discord.ui.Button(label='Check Update', style=discord.ButtonStyle.url, url='https://hamzabot.me/updates#3.3.0'))
class UpdateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='update', description='Get information about the latest update of Hamza.')
    async def update(self, interaction: discord.Interaction):
        async with asqlite.connect('database.db') as conn:
            async with conn.cursor() as cursor:
                await cursor.execute('''CREATE TABLE IF NOT EXISTS users
            (id INTEGER PRIMARY KEY, user_id TEXT UNIQUE)''')
                await cursor.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)',
            (str(interaction.user.id), ))
                await conn.commit()

        embed = discord.Embed(title='Update v3.3.0', description='Latest update of Hamza Bot is here! Added, fixed a few things! AI is back, too!')
        await interaction.response.send_message(embed=embed, view=MyView())

async def setup(bot):
    await bot.add_cog(UpdateCog(bot))