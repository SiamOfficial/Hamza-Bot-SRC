from discord.ext import commands
import os
import discord
from discord import app_commands
import typing
class DevCog(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    print('Group dev loaded!')

  async def action_autocompletion(self, interaction: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
        data = []
        actions = ['Load', 'Reload', 'Unload']
        for action in actions:
            if current.lower() in action.lower():
                data.append(app_commands.Choice(name=action, value=action))
        # slice the data list by 25
        return data[:25]
  async def response_autocompletion(self, interaction: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
        data = []
        responses = ['Accepted', 'Declined']
        for response in responses:
            if current.lower() in response.lower():
                data.append(app_commands.Choice(name=response, value=response))
        # slice the data list by 25
        return data[:25]
  async def content_autocompletion(self, interaction: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
        data = []
        contents = ['Nasheed', 'Adhan']
        for content in contents:
            if current.lower() in content.lower():
                data.append(app_commands.Choice(name=content, value=content))
        # slice the data list by 25
        return data[:25]
  async def files_autocompletion(self, interaction: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
    data = []
    for folder in os.listdir('./cogs'):
        for file in os.listdir(f'./cogs/{folder}'):
            if file.endswith('.py'):
                path = f'cogs.{folder}.{file[:-3]}'
                if current.lower() in path.lower():
                    data.append(app_commands.Choice(name=path, value=path))
    return data[:25]

  developer = app_commands.Group(name='developer', description='Developer only command!')
  @developer.command(name='sync', description='Syncs all commands [for developer]')
  async def sync(self, interaction: discord.Interaction):
    if interaction.user.id == 696623699666665532:
      try:
        await interaction.response.defer(ephemeral=True)
        fmt = await self.bot.tree.sync()
        await interaction.followup.send(f'Synced {len(fmt)} commands')
        print(f'Synced {len(fmt)} commands')
      except Exception as e:
        await interaction.response.send_message(e, ephemeral=True)
    else:
      await interaction.response.send_message('Astaghfirullah, you are not my developer!', ephemeral=True)
  @developer.command(name='extension', description='Does something with an extension [for developer]')
  @app_commands.describe(action='The type of action you want.', extension='Name of the extension')
  @app_commands.autocomplete(action=action_autocompletion, extension=files_autocompletion)
  async def extension(self, interaction: discord.Interaction, action: str, extension: str):
    if interaction.user.id == 696623699666665532:
      if action == 'Reload':
        try:
          await interaction.response.defer(ephemeral=True)
          await self.bot.reload_extension(extension)
          await interaction.followup.send(f'Reloaded {extension}!')
          print(f'Reloaded {extension}!')
        except Exception as e:
          await interaction.followup.send(e, ephemeral=True)
      elif action == 'Unload':
        try:
          await interaction.response.defer(ephemeral=True)
          await self.bot.unload_extension(extension)
          await interaction.followup.send(f'Unloaded {extension}!')
          print(f'Unloaded {extension}!')
        except Exception as e:
          await interaction.followup.send(e, ephemeral=True)
      else:
        try:
          await interaction.response.defer(ephemeral=True)
          await self.bot.load_extension(extension)
          await interaction.followup.send(f'Loaded {extension}!')
          print(f'Loaded {extension}!')
        except Exception as e:
          await interaction.followup.send(e, ephemeral=True)
    else:
      await interaction.response.send_message('Astaghfirullah, you are not my developer!', ephemeral=True)
  @developer.command(name='submit', description='Answers to submission [for developer]')
  @app_commands.autocomplete(response=response_autocompletion, content=content_autocompletion)
  @app_commands.describe(user='ID of the user', content='Nasheed or Adhan', name= 'Name of the content', response='Accepted or Declined', message='Message to the user who submitted.')
  async def sync(self, interaction: discord.Interaction, user: str, content: str, name: str, response: str, message: str):
    if interaction.user.id == 696623699666665532:
      try:
        user1 = await self.bot.fetch_user(int(user))
        if response == 'Accepted':
          await interaction.response.defer(ephemeral=True)
          await user1.send(f'Assalamu Alaikum! Congratulations, your submission of {content} "{name}" has been accepted and added to the bot!\n**Message from the developer:** {message}')
          await interaction.followup.send('Sent!', ephemeral=True)
        elif response == 'Declined':
          await interaction.response.defer(ephemeral=True)
          await user1.send(f'Assalamu Alaikum! Sorry, your submission of {content} "{name}" has been declined and not added to the bot!\n**Message from the developer:** {message}')
          await interaction.followup.send('Sent!', ephemeral=True)
      except Exception as e:
        await interaction.response.send_message(e, ephemeral=True)
    else:
      await interaction.response.send_message('Astaghfirullah, you are not my developer!', ephemeral=True)

async def setup(bot):
  await bot.add_cog(DevCog(bot))