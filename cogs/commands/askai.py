import discord
from discord import app_commands
from discord.ext import commands
import openai
from typing import Literal
from datetime import datetime
from Ai.Completion import generate_completion_response
from Ai.AiBase import Message


class AskAICog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @app_commands.command(name="askai", description='Ask Hamza AI about any Islamic question.')
  @app_commands.describe(question='Question you want to ask. (Must be related to Islam)')
  async def askai(self, interaction: discord.Interaction, question: str):
    #await interaction.response.send_message('Assalamu Alaikum, the AI is currently unavailable at this moment right now. Please stick to the updates in the support server. (Use /info command to join the support server.)')
    try:
        await interaction.response.defer()
        response = await generate_completion_response(
            messages=[Message(user=interaction.user.name, text=question)], user=interaction.user.name
        )
        if len(question) > 256:
          questionshorted = f'{question[:253]}...'
        else:
          questionshorted = question
        embed = discord.Embed(title=questionshorted, description=f'''```{response.reply_text}```''')
        embed.set_footer(text=f'Hamza AI helped by {await self.bot.fetch_user(821789676255969301)}')
        await interaction.followup.send(embed=embed)
        guild = self.bot.get_guild(1076185219700363264)
        channel = guild.get_channel(1108727272749408316)
        embed = discord.Embed(title=f'{interaction.user} asked', description=question)
        embed2 = discord.Embed(title=f'I answered', description=response.reply_text)
        embeds = [embed, embed2]
        await channel.send(embeds=embeds)
    except:
        await interaction.response.send_message(f'Something went wrong! Try again later!', ephemeral=True)

async def setup(bot):
  await bot.add_cog(AskAICog(bot))