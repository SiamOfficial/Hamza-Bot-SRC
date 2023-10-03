from typing import Optional
import discord
from discord import app_commands
from discord.ext import commands

class MyView(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(discord.ui.Button(label='Invite', style=discord.ButtonStyle.url, url='http://invite.hamzabot.me/'))
        self.add_item(discord.ui.Button(label='Website', style=discord.ButtonStyle.url, url='http://hamzabot.me/'))
        self.add_item(discord.ui.Button(label='Support', style=discord.ButtonStyle.url, url='http://support.hamzabot.me/'))
        self.add_item(discord.ui.Button(label='Vote (top.gg)', style=discord.ButtonStyle.url, url='http://votetopgg.hamzabot.me/'))
        self.add_item(discord.ui.Button(label='Vote (discordbotlist.com)', style=discord.ButtonStyle.url, url='http://votedbl.hamzabot.me/'))
class InfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='info', description='Get information of Hamza Bot.')
    async def info(self, interaction: discord.Interaction):
        await interaction.response.defer()
        members = 0
        channels = 0
        latency = self.bot.latency * 1000
        ready_time = str(self.bot.ready_time).split('.')
        for guild in self.bot.guilds:
            members += guild.member_count
            channels += len(guild.channels)
        emb = discord.Embed(title=f'Hamza Bot ({self.bot.user})', description='Assalamu Alaikum. Hamza Bot is an islamic halal bot made for muslims to do/discover islamic things. Such as Quran verses, hadiths, charity [coming soon™️], etc. This bot is free-to-use. This bot has no premium versions. But if you want to support the development, please make dua for the developer. May Allah bless you!')
        emb.add_field(name='Developer', value=f'[{await self.bot.fetch_user(696623699666665532)}](https://discord.com/users/696623699666665532)')
        emb.add_field(name='APIs', value='[Hamza Bot API](https://hamzabot.me/api), [IslamiQ API](https://api.islamiq.me/), [Quran API](https://github.com/fawazahmed0/quran-api), [Hadith API](https://github.com/fawazahmed0/hadith-api)')
        emb.add_field(name='Servers', value=f'```{str(len(self.bot.guilds))}```')
        emb.add_field(name='Members', value=f'```{str(members)}```')
        emb.add_field(name='Channels', value=f'```{str(channels)}```')
        emb.add_field(name='Ping', value=f'```{latency:.2f} ms```')
        emb.add_field(name='Uptime', value=f'<t:{ready_time[0]}:R>')
        emb.set_thumbnail(url=self.bot.user.avatar.url)
        emb.set_footer(text='Hamza Bot')
        await interaction.followup.send(embed=emb, view=MyView())

async def setup(bot):
    await bot.add_cog(InfoCog(bot))