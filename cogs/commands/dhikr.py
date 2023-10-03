from typing import Optional
import discord
from discord.ext import commands
from discord import app_commands
import asqlite
from utilities.dhikrcount import DhikrCount
import typing
import datetime
dhikrs = ["La ilaha illallah", "SubhanAllah", "Alhamdulillah", "Allahu Akbar", "Astaghfirullah",
          "SubhanAllahi wa bihamdihi SubhanAllahil Adheem", "La hawla wala quwwata illa billah",
          "Allahumma salli ala Muhammad", "Allahumma barik ala Muhammad", "Radhiallahu anhu anha anhum"]

class Sure(discord.ui.View):
    def __init__(self, original_response, dhikr_count):
        super().__init__()
        self.original_response = original_response
        self.dhikr_count = dhikr_count
    async def get_embed(self, interaction: discord.Interaction):
        dhikr_counts = []
        for dhikr in dhikrs:
            dhikr_counts.append(f"**{dhikr}:** 0")
        counts_string = "\n".join(dhikr_counts)
        embed = discord.Embed(title=f"Dhikr Counts", description=f"Here are your dhikr counts:\n\n{counts_string}")
        embed.set_author(icon_url=interaction.user.avatar, name=interaction.user)
        return embed
    @discord.ui.button(label='Yes', style=discord.ButtonStyle.danger)
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        async with asqlite.connect('dhikr.db') as conn:
            async with conn.cursor() as cursor:
                for dhikr in dhikrs:
                    await cursor.execute(f"DELETE FROM {dhikr.replace(' ', '_')} WHERE user_id = ?", (interaction.user.id))
                await conn.commit()
                await self.original_response.edit(embed=await self.get_embed(interaction))
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(content='The reset was a success!', view=self)
    @discord.ui.button(label='No', style=discord.ButtonStyle.green)
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(content='The reset was cancelled!', view=self)

class MyView(discord.ui.View):
    def __init__(self, author):
        super().__init__()
        self.author = author
    @discord.ui.button(label='Reset', style=discord.ButtonStyle.danger)
    async def reset(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = Sure(interaction.message, self)
        await interaction.response.send_message('Are you sure you want to reset your dhikr counts? **This action cannot be undone!**', view=view, ephemeral=True)
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.author.id:
            try:
                await interaction.response.send_message('This command is not for you!', ephemeral=True)
            except discord.errors.NotFound:
                pass
            return False
        return True

class DhikrCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def dhikr_autocompletion(self, interaction: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
        data = []
        for dhikr in dhikrs:
            if current.lower() in dhikr.lower():
                data.append(app_commands.Choice(name=dhikr, value=dhikr))
        return data[:25]

    dhikr = app_commands.Group(name='dhikr', description='Dhikr related commands.')

#START DHIKR
    @dhikr.command(name='start', description='Allows you to start your dhikr count')
    @app_commands.autocomplete(dhikr=dhikr_autocompletion)
    @app_commands.describe(dhikr='Name of the dhikr.')
    async def start(self, interaction: discord.Interaction, dhikr: str):
        await interaction.response.defer()
        view = DhikrCount(interaction.user, self.bot, dhikr.replace(' ', '_'))
        await view.load_click_count()
        await interaction.followup.send(embed=await view.get_embed(interaction), view=view)

#DHIKR COUNT
    @dhikr.command(name='counts', description='View all of your dhikr counts!')
    async def count(self, interaction: discord.Interaction):
        await interaction.response.defer()

        dhikr_counts = []
        for dhikr in dhikrs:
            user_id = interaction.user
            view = DhikrCount(user_id, self.bot, dhikr.replace(' ', '_'))
            count = await view.load_click_count()
            dhikr_counts.append(f"**{dhikr}:** {count}")

        counts_string = "\n".join(dhikr_counts)
        reset = MyView(interaction.user)
        embed = discord.Embed(title=f"Dhikr Counts", description=f"Here are your dhikr counts:\n\n{counts_string}")
        embed.set_footer(text='Dhikr counts will reset during 12 am to 1 am (EDT) everyday.')
        embed.set_author(icon_url=interaction.user.avatar, name=interaction.user)

        await interaction.followup.send(embed=embed, view=reset)



async def setup(bot):
    await bot.add_cog(DhikrCog(bot))