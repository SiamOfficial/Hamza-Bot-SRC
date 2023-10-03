import discord
from discord import app_commands
from discord.ext import commands
import asqlite
import random

class MyView(discord.ui.View):
    def __init__(self):
        super().__init__()
class LogsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

#COMMANDS LOG
    @commands.Cog.listener()
    async def on_app_command_completion(self, interaction: discord.Interaction, command: discord.app_commands.Command):

        guild = self.bot.get_guild(1076185219700363264)
        channel = guild.get_channel(1092117950313533482)
        if command.parent:
            msg = command.parent.name
        else:
            msg = "-"
        if interaction.guild:
            server = f'{interaction.guild} ({interaction.guild.id})'
            icon = interaction.guild.icon
        else:
            server = '-'
            icon = None
        embed = discord.Embed(title='Command Logs')
        embed.add_field(name='User ID', value=interaction.user.id)
        embed.add_field(name='Parent Command', value=msg)
        embed.add_field(name='Command', value=interaction.command.name)
        embed.add_field(name='Guild', value=server)
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar, url=f'https://discord.com/users/{interaction.user.id}')
        embed.set_thumbnail(url=icon)
        await channel.send(embed=embed)

        async with asqlite.connect('database.db') as conn:
            async with conn.cursor() as cursor:
                await cursor.execute('''CREATE TABLE IF NOT EXISTS users
       (id INTEGER PRIMARY KEY, user_id TEXT UNIQUE)''')
                await cursor.execute('SELECT user_id FROM users WHERE user_id = ?',
        (str(interaction.user.id),))
                data = await cursor.fetchone()
                if data is None:
                    await interaction.followup.send('New update is available! Type </update:1104303827030642698> to check!', ephemeral=True)
                else:
                    pass
        chance = random.randint(1, 100)
        if chance <= 10:
            await interaction.followup.send(f'Seems like you are enjoying **{self.bot.user.name}**! Please also consider trying out other cool commands of this Bot!', ephemeral=True)

    #JOIN LOGS
    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        channel = random.choice(guild.text_channels)
        embed = discord.Embed(title=f'Jazakallahu Khairan for adding {self.bot.user}', description='Assalamu Alaikum! Hamza bot is a discord bot for your islamic server. To get started, run the command /help.')
        embed.set_thumbnail(url=self.bot.user.avatar)
        embed.set_footer(text=f'Made by {await self.bot.fetch_user(696623699666665532)}')
        view = MyView()
        view.add_item(discord.ui.Button(label='Invite', style=discord.ButtonStyle.url, url='http://invite.hamzabot.me'))
        view.add_item(discord.ui.Button(label='Support Server', style=discord.ButtonStyle.url, url='http://support.hamzabot.me'))
        view.add_item(discord.ui.Button(label='Website', style=discord.ButtonStyle.url, url='https://hamzabot.me'))
        await channel.send(embed=embed, view=view)
        guild1 = self.bot.get_guild(1076185219700363264)
        channel = guild1.get_channel(1092117965933125673)
        owner = await self.bot.fetch_user(guild.owner_id)
        embed = discord.Embed(title='Join Logs')
        embed.add_field(name='Guild Name', value=guild.name)
        embed.add_field(name='Guild ID', value=guild.id)
        embed.add_field(name='Owner ID', value=owner.id)
        embed.add_field(name='Members', value=guild.member_count)
        embed.set_thumbnail(url=guild.icon)
        embed.set_author(icon_url=owner.avatar, name=owner, url=f'https://discord.com/users/{guild.owner_id}')
        await channel.send(embed=embed)
    #REMOVE LOGS
    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        guild1 = self.bot.get_guild(1076185219700363264)
        channel = guild1.get_channel(1092117982261563462)
        owner = await self.bot.fetch_user(guild.owner_id)
        embed = discord.Embed(title='Leave Logs')
        embed.add_field(name='Guild Name', value=guild.name)
        embed.add_field(name='Guild ID', value=guild.id)
        embed.add_field(name='Owner ID', value=owner.id)
        embed.add_field(name='Members', value=guild.member_count)
        embed.set_thumbnail(url=guild.icon)
        embed.set_author(icon_url=owner.avatar, name=owner, url=f'https://discord.com/users/{guild.owner_id}')
        await channel.send(embed=embed)
async def setup(bot):
    await bot.add_cog(LogsCog(bot))