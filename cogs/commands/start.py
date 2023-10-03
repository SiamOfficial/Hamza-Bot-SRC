import discord
from discord import app_commands
from discord.ext import commands

class StartCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='start', description='Get all the basic information to get started with Islam if you are interested!')
    async def start(self, interaction: discord.Interaction):
        emb = discord.Embed(title='Get started with Islam', description='Here are the things you need to get started.')
        emb.add_field(name='Information', value='''[What's Islam?](https://en.wikipedia.org/wiki/Islam)
[Why Islam?](https://www.alislam.org/library/books/Why-Islam-My-Choice.pdf)
[How to get started with Islam?](https://www.mymasjid.ca/beginners-guide-understanding-islam)''', inline=False)
        emb.add_field(name='Quran', value='''[Quran Online](https://quran.com/), [Free Quran Copy](https://cpsglobal.org/content/order-free-quran-2)''', inline=False)
        emb.add_field(name='Main Hadith Books', value='''[Sahih Al-Bukhari](https://d1.islamhouse.com/data/en/ih_books/single/en_Sahih_Al-Bukhari.pdf), [Sahih Muslim](https://d1.islamhouse.com/data/en/ih_books/single/en_Sahih_Muslim.pdf), [Sunan Abu Dawood](https://ia802204.us.archive.org/10/items/AllInOne-Hadiths-EngArabicDarusalam_201407/All%20in%20One-Sunan%20Abu%20Dawud-Eng.pdf), [Sunan al-Tirmidhi](https://archive.org/details/sunan-tirmidhi-arabic-english-full/sunan-tirmidhi-english-vol-1/), [Sunan al-Nasa'i](https://archive.org/details/sunan-an-nasa-i-volume-1-6/sunan-an-nasa-i-volume-1/), [Sunan ibn Majah](https://archive.org/details/SunanIbnMajahVol.11802EnglishArabic/Sunan%20Ibn%20Majah%20Vol.%201%20-%201-802%20English%20Arabic/)''', inline=False)
        emb.add_field(name='Popular & Trusted Scholars', value='''[Zakir Naik](https://en.wikipedia.org/wiki/Zakir_Naik), [Mufti Menk](https://en.wikipedia.org/wiki/Ismail_ibn_Musa_Menk), [Assim Al-Hakeem](https://iou.edu.gm/instructors/assim-al-hakeem/#:~:text=Shaykh%20Assim%20al%2DHakeem%20is,Makkah%2C%20Saudi%20Arabia%20in%201998)''', inline=False)
        emb.set_thumbnail(url='https://media.discordapp.net/attachments/997260995883966464/1073289266026774538/Siam_Official_Islam_crescent_moon_4k_2d_art._black_background_784e0b1e-0081-408d-a585-139c8f139511.png?width=401&height=401')
        emb.set_footer(text='Welcome to Islam!')
        await interaction.response.send_message(embed=emb)

async def setup(bot):
    await bot.add_cog(StartCog(bot))