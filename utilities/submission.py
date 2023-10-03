import discord
from discord.ext import commands

class Nasheed_Submission(discord.ui.Modal, title='Nasheed Submission'):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
        self.custom_id = 'nasheed_submission'

    name = discord.ui.TextInput(label=f'Nasheed Name', required=True, placeholder='Name of the nasheed you want to submit.')
    link = discord.ui.TextInput(label='Nasheed Link (Streaming Link/File Link)', required=True, placeholder='Link to the nasheed or its file.')
    author = discord.ui.TextInput(label='Nasheed Author', required=True, placeholder="Name of the author who made this nasheed.")
    copyright_free = discord.ui.TextInput(label='Is the nasheed copyright-free?', required=True, placeholder='Yes or No', max_length=3)
    message = discord.ui.TextInput(label='Your Message', placeholder='Your message to the developer.', required=False, max_length=300, style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message('Thank you for submitting the nasheed!', ephemeral=True)
        try:
            embed = discord.Embed(title='Nasheed Submission')
            embed.add_field(name='Nasheed Name', value=self.name, inline=False)
            embed.add_field(name='Nasheed Link', value=self.link, inline=False)
            embed.add_field(name='Nasheed Author', value=self.author, inline=False)
            embed.add_field(name='Copyright-Free', value=self.copyright_free, inline=False)
            embed.add_field(name='Message', value=self.message or None, inline=False)
            embed.set_author(icon_url=interaction.user.avatar, name=interaction.user, url=f'https://discord.com/users/{interaction.user.id}')
            guild = self.bot.get_guild(1076185219700363264)
            channel = guild.get_channel(1154395630177898507)
            await channel.send(embed=embed)
        except:
            pass

class Adhan_Submission(discord.ui.Modal, title='Adhan Submission'):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
        self.custom_id = 'adhan_submission'

    name = discord.ui.TextInput(label=f'Adhan Name', required=True, placeholder='Name of the adhan you want to submit.')
    link = discord.ui.TextInput(label='Adhan Link (Streaming Link/File Link)', required=True, placeholder='Link to the adhan or its file.')
    author = discord.ui.TextInput(label='Adhan Author', required=True, placeholder="Name of the author who made this adhan.")
    copyright_free = discord.ui.TextInput(label='Is the adhan copyright-free?', required=True, placeholder='Yes or No', max_length=3)
    message = discord.ui.TextInput(label='Your Message', placeholder='Your message to the developer.', required=False, max_length=300, style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message('Thank you for submitting the adhan!', ephemeral=True)
        try:
            embed = discord.Embed(title='Adhan Submission')
            embed.add_field(name='Adhan Name', value=self.name, inline=False)
            embed.add_field(name='Adhan Link', value=self.link, inline=False)
            embed.add_field(name='Adhan Author', value=self.author, inline=False)
            embed.add_field(name='Copyright-Free', value=self.copyright_free, inline=False)
            embed.add_field(name='Message', value=self.message or None, inline=False)
            embed.set_author(icon_url=interaction.user.avatar, name=interaction.user, url=f'https://discord.com/users/{interaction.user.id}')
            guild = self.bot.get_guild(1076185219700363264)
            channel = guild.get_channel(1154395644216217740)
            await channel.send(embed=embed)
        except:
            pass
      