import discord
from discord import app_commands
from discord.ext import commands

class SelectMenu(discord.ui.Select):
    def __init__(self):

        options = [
            discord.SelectOption(label='Islam', description='Commands related to Islam.'),
            discord.SelectOption(label='Quran', description='Commands related to Quran.'),
            discord.SelectOption(label='Hadith', description='Commands related to Hadith.'),
            discord.SelectOption(label='Bot', description='Commands related to Bot.'),
            discord.SelectOption(label='AI', description='Commands related to AI.'),
            discord.SelectOption(label='Voice', description='Commands related to Voice.')
        ]

        super().__init__(placeholder='Choose a category!', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == 'Islam':
            embed = discord.Embed(title=f'Help: {self.values[0]}', description='</start:1104303826829332571> </dua search:1109030558111109150> </dua random:1109030558111109150> </calendar hijri_date:1094629224020725804> </calendar to_hijri:1094629224020725804> </calendar to_gregorian:1094629224020725804> </quote random:1109030557951737883> </meme:1104303826829332569> </time prayers:1109030557951737877> </dhikr start:1114121856681783308> </dhikr counts:1114121856681783308>')
            embed.set_footer(text='For options and description of each command, click the Commands button below.')
            await interaction.response.edit_message(embed=embed)
        elif self.values[0] == 'Quran':
            embed = discord.Embed(title=f'Help: {self.values[0]}', description='</verse search:1109030557951737885> </chapter search:1109030557951737878> </verse random:1109030557951737885> </chapter random:1109030557951737878> </tafsir search:1109030557951737880> </chapterinfo search:1109030557951737884> </chapterinfo random:1109030557951737884> </chapterlist:1104303826829332564> </page search:1109030557951737882> </page random:1109030557951737882> </page all:1109030557951737882>')
            embed.set_footer(text='For options and description of each command, click the Commands button below.')
            await interaction.response.edit_message(embed=embed)
        elif self.values[0] == 'Hadith':
            embed = discord.Embed(title=f'Help: {self.values[0]}', description='</hadith search:1109030557951737876> </hadith random:1109030557951737876>')
            embed.set_footer(text='For options and description of each command, click the Commands button below.')
            await interaction.response.edit_message(embed=embed)
        elif self.values[0] == 'Bot':
            embed = discord.Embed(title=f'Help: {self.values[0]}', description='</help:1104303826829332567> </update:1104303827030642698> </info:1104303826829332568> </achievements:1121749404618076211> </submit adhan:1156835315349192785> </submit nasheed:1156835315349192785>')
            embed.set_footer(text='For options and description of each command, click the Commands button below.')
            await interaction.response.edit_message(embed=embed)
        elif self.values[0] == 'AI':
            embed = discord.Embed(title=f'Help: {self.values[0]}', description='</askai:1104303826829332563>')
            embed.set_footer(text='For options and description of each command, click the Commands button below.')
            await interaction.response.edit_message(embed=embed)
        elif self.values[0] == 'Voice':
            embed = discord.Embed(title=f'Help: {self.values[0]}', description='</chapter recite:1109030557951737878> </verse recite:1109030557951737885> </adhan play:1109030557951737881> </nasheed play:1109030557951737879>')
            embed.set_footer(text='For options and description of each command, click the Commands button below.')
            await interaction.response.edit_message(embed=embed)

class MyView(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_item(SelectMenu())
        self.add_item(discord.ui.Button(label='Commands', style=discord.ButtonStyle.url, url='https://hamzabot.me/commands'))
class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='help', description='Get all the commands of Hamza (Stop it, get some help).')
    async def help(self, interaction: discord.Interaction):
        view = MyView()
        embed = discord.Embed(title='Help', description='Choose a category of commands below.')
        embed.set_footer(text='For options and description of each command, click the Commands button below.')
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(HelpCog(bot))
