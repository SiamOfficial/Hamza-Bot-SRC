import asyncio
import discord
from discord import app_commands
from discord.ext import commands
import praw
import random
reddit = praw.Reddit(client_id="m65mVfreEWHjPSSE2wGYaw",
                       client_secret="KGtkUTTJ73dETW9RzztjY36nklr6dg",
                       user_agent="Script:halalpostfetching:1.0.0 (by u/SiamOfficial)")

class MemeCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    
  @app_commands.command(name="meme", description="Get a random islamic meme from Reddit")
  async def meme(self, interaction: discord.Interaction):
    await interaction.response.defer()
    loop = asyncio.get_event_loop()
    redditlist = ['Muslim_Memes', 'halalmemes', 'izlanimemes', 'izlam']
    type = random.choice(redditlist)
    if not hasattr(self.bot, 'nextMeme'): # check if the bot has the nextMeme attribute
        self.bot.nextMeme = await loop.run_in_executor(None, reddit.subreddit(type).random) # if not, get the first meme
    submission = self.bot.nextMeme # get the next meme from the bot attribute
    if submission:
        if not submission.is_self:
            if len(submission.title) > 256:
              title = submission.title[:253] + '...'
            else:
              title = submission.title
            emb = discord.Embed(title=f'[{type}] {title}', url=f'https://reddit.com{submission.permalink}')
            emb.set_image(url=submission.url)
            emb.set_footer(text=f'Score: {submission.score} | Upvote Ratio: {submission.upvote_ratio}')
        else:
            emb = discord.Embed(description='I couldn\'t find an image in that subreddit!')
        await interaction.followup.send(embed=emb)
        self.bot.nextMeme = await loop.run_in_executor(None, reddit.subreddit(type).random) # update the next meme after sending it

async def setup(bot):
  await bot.add_cog(MemeCog(bot))
