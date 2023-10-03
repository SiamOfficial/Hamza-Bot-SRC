import discord
from discord.ext import commands, tasks
from cogs.commands.calendar import HijriCalendar
import time
import os
import datetime
class BotStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(hours=1)
    async def update_presence(self):
        status = discord.Activity(type=discord.ActivityType.listening, name=f"v3.3.0 | {len(self.bot.guilds)} guilds")
        await self.bot.change_presence(status=discord.Status.idle, activity=status)
    
    @tasks.loop(hours=1)
    async def dhikr_reset(self):
        if datetime.datetime.now().hour == 0:
            if os.path.exists("dhikr.db"):
                os.remove("dhikr.db")
                print("Removed dhikr.db file!")
            else:
                pass   
        else:
            pass   

    @update_presence.before_loop
    async def before_presence_update(self):
        await self.bot.wait_until_ready()
    @dhikr_reset.before_loop
    async def before_dhikr_reset(self):
        await self.bot.wait_until_ready()
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Status loaded!')
        self.bot.ready_time = time.time()
        self.update_presence.start()
async def setup(bot):
    await bot.add_cog(BotStatus(bot))