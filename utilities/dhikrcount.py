import discord
from discord.ext import commands
import asqlite
import datetime
import os
import asyncio

class MyView(discord.ui.View):
    def __init__(self, name, original_response, dhikr_count):
        super().__init__()
        self.name = name
        self.original_response = original_response
        self.dhikr_count = dhikr_count

    @discord.ui.button(label='Yes', style=discord.ButtonStyle.danger)
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        async with asqlite.connect('dhikr.db') as conn:
            async with conn.cursor() as cursor:
            # Get today's count
                await cursor.execute(f"SELECT click_count FROM {self.name} WHERE user_id = ?",
                                 (interaction.user.id))
                today_count = await cursor.fetchone()

                if today_count is not None:
                # Reset today's count
                    await cursor.execute(f"DELETE FROM {self.name} WHERE user_id = ?",
                                     (interaction.user.id))

                    await conn.commit()

                # Update the count in the dhikr_count object
                    self.dhikr_count.click_count = 0

                # Update the count in the original response
                    self.original_response.embeds[0].set_field_at(
                    index=0,
                    name=f"{self.name.replace('_', ' ')} Count",
                    value=str(self.dhikr_count.click_count)
                )

                # Edit the original response
                    await self.original_response.edit(embed=self.original_response.embeds[0])
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(content='The reset was a success!', view=self)

    @discord.ui.button(label='No', style=discord.ButtonStyle.green)
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        for child in self.children:
            child.disabled = True
        await interaction.response.edit_message(content='The reset was cancelled!', view=self)

class DhikrCount(discord.ui.View):
    def __init__(self, author, bot, name):
        super().__init__()
        self.bot = bot
        self.author = author
        self.click_count = 0
        self.name = name
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.reset_counts_daily())

    async def load_click_count(self):
        # Connect to the database
        async with asqlite.connect("dhikr.db") as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    f"CREATE TABLE IF NOT EXISTS {self.name} (id INTEGER PRIMARY KEY, user_id TEXT UNIQUE, click_count INTEGER)"
                )
                # Retrieve the user's click count from the database based on the specified date

                await cursor.execute(f"SELECT click_count FROM {self.name} WHERE user_id = ?",
                                         (self.author.id,))
                result = await cursor.fetchone()

                if result:
                    # If the user's click count exists, set it as the initial count
                    self.click_count = result[0]
        return self.click_count

    @discord.ui.button(label='Dhikr', style=discord.ButtonStyle.primary)
    async def click(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Increment the click count
        self.click_count = await self.load_click_count()
        self.click_count += 1
        await self.store_click(interaction.user.id, self.click_count)

        # Retrieve and update the click count from the database
        self.click_count = await self.load_click_count()

        await interaction.response.edit_message(embed=await self.get_embed(interaction))

    @discord.ui.button(label='Reset', style=discord.ButtonStyle.danger)
    async def reset(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = MyView(self.name, interaction.message, self)
        await interaction.response.send_message(
            'Are you sure you want to reset your dhikr counts? **This action cannot be undone!**',
            view=view,
            ephemeral=True
        )

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.author.id:
            try:
                await interaction.response.send_message('This command is not for you!', ephemeral=True)
            except discord.errors.NotFound:
                pass
            return False
        return True
    async def reset_counts_daily(self):
        while True:
            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            tomorrow_str = tomorrow.strftime("%Y-%m-%d")
            if datetime.date.today() == tomorrow:
                await self.reset_counts()
            await asyncio.sleep(86400)  # 24 hours
    
    async def store_click(self, user_id, click_count):
        # Connect to the database
        async with asqlite.connect("dhikr.db") as conn:
            async with conn.cursor() as cursor:
                # Create a table if it doesn't exist
                await cursor.execute(
                    f"CREATE TABLE IF NOT EXISTS {self.name} (id INTEGER PRIMARY KEY, user_id TEXT UNIQUE, click_count INTEGER)"
                )
                await cursor.execute(f"INSERT OR REPLACE INTO {self.name} (user_id, click_count) "
                                         f"VALUES (?, ?)", (user_id, click_count))
                await conn.commit()

    async def get_embed(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Dhikr Counter",
                              description='Click the button below to increase your dhikr count!')
        embed.set_author(icon_url=interaction.user.avatar, name=interaction.user)
        name = self.name.replace('_', ' ')
        embed.add_field(name=f"{name} Count", value=str(self.click_count))
        return embed