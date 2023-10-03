from discord.ext import commands
from discord import app_commands
import discord
from utilities.functions import get_hadith, get_hadith_number, get_hadith_author
from utilities.converting import convert_to_arabic_number
import typing
import random
dic = {
        'Sunan Abu Dawud': "سنن أبي داود",
        'Sahih al Bukhari': "صحيح البخاري",
        'Sunan Ibn Majah': "سُنن ابن ماجه",
        'Muwatta Malik': "موطأ مالك",
        'Sahih Muslim': "صحيح مسلم",
        'Sunan an Nasai': "سنن النسائي",
        'Jami At Tirmidhi': "جامع الترمذي",
        "Section": "القسم"
    }
class HadithCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    hadith = app_commands.Group(name='hadith', description='Hadith related commands')
    async def hadith_book_autocompletion(self, interaction: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
        data = []
        books = ['Sunan Abu Dawud', 'Sahih al Bukhari', 'Sunan Ibn Majah', 'Muwatta Malik', 'Sahih Muslim', 'Sunan an Nasai', 'Jami At Tirmidhi']
        books_short = ['abudawud', 'bukhari', 'ibnmajah', 'malik', 'muslim', 'nasai', 'tirmidhi']
        for book in books:
            if current.lower() in book.lower():
                index = books.index(book)
                data.append(app_commands.Choice(name=book, value=books_short[index]))
        return data[:25]
    async def hadith_translation_autocompletion(self, interaction: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
        data = []
        langs = ['English', 'Bengali', 'Turkish', 'Indonesian', 'Urdu']
        for lang in langs:
            if current.lower() in lang.lower():
                data.append(app_commands.Choice(name=lang, value=lang))
        return data[:25]
    
#search hadith
    @hadith.command(name='search', description='Gives you a specific hadith from a specific book.')
    @app_commands.describe(book='Name of the book', hadith='Number of the hadith', translation='Translation you want')
    @app_commands.autocomplete(book=hadith_book_autocompletion, translation=hadith_translation_autocompletion)
    async def search(self, interaction: discord.Interaction, book: str, hadith: int, translation: str):
        try:
            await interaction.response.defer()
            langs_short = {'English': 'eng', 'Bengali': 'ben', 'Turkish': 'tur', 'Indonesian': 'ind', 'Urdu': 'urd'}
            arabichadith = await get_hadith(book=f'ara-{book}', hadith=hadith)
            translatedhadith = await get_hadith(book=f'{langs_short[translation]}-{book}', hadith=hadith)
            author = await get_hadith_author(book=book)
            arabicnumber = convert_to_arabic_number(str(hadith))
            secarabic = convert_to_arabic_number(str(translatedhadith["hadiths"][0]["reference"]["book"]))
            grades_str = '\n'.join([f'{grade["name"]}: {grade["grade"]}' for grade in translatedhadith["hadiths"][0]["grades"]])
            embed = discord.Embed(title=f'{translatedhadith["hadiths"][0]["hadithnumber"]} ({translatedhadith["metadata"]["name"]}, Section {str(translatedhadith["hadiths"][0]["reference"]["book"])}) | {arabicnumber} ({dic[translatedhadith["metadata"]["name"]]}, {dic["Section"]} {secarabic})',
                                  description=f'''```{arabichadith["hadiths"][0]["text"]}```
```{translatedhadith["hadiths"][0]["text"]}```''')
            embed.add_field(name='Information', value=f'''**Translation:** {translation}
**Grades:**
{grades_str}''')
            embed.set_author(icon_url=self.bot.user.avatar, name=author['author_name'])
            await interaction.followup.send(embed=embed)
        except:
            await interaction.followup.send('You provided an invalid reference!', ephemeral=True)

#get rhadith
    @hadith.command(name='random', description='Gives you a random hadith from a random book.')
    @app_commands.describe(translation='Translation you want')
    @app_commands.autocomplete(translation=hadith_translation_autocompletion)
    async def random(self, interaction: discord.Interaction, translation: str):
        try:
            await interaction.response.defer()
            books  = ['abudawud', 'bukhari', 'ibnmajah', 'malik', 'muslim', 'nasai', 'tirmidhi']
            book = random.choice(books)
            langs_short = {'English': 'eng', 'Bengali': 'ben', 'Turkish': 'tur', 'Indonesian': 'ind', 'Urdu': 'urd'}
            hadith = await get_hadith_number(book=book)
            arabichadith = await get_hadith(book=f'ara-{book}', hadith=hadith)
            translatedhadith = await get_hadith(book=f'{langs_short[translation]}-{book}', hadith=hadith)
            author = await get_hadith_author(book=book)
            arabicnumber = convert_to_arabic_number(str(hadith))
            secarabic = convert_to_arabic_number(str(translatedhadith["hadiths"][0]["reference"]["book"]))
            grades_str = '\n'.join([f'{grade["name"]}: {grade["grade"]}' for grade in translatedhadith["hadiths"][0]["grades"]])
            embed = discord.Embed(title=f'{translatedhadith["hadiths"][0]["hadithnumber"]} ({translatedhadith["metadata"]["name"]}, Section {str(translatedhadith["hadiths"][0]["reference"]["book"])}) | {arabicnumber} ({dic[translatedhadith["metadata"]["name"]]}, {dic["Section"]} {secarabic})',
                                  description=f'''```{arabichadith["hadiths"][0]["text"]}```
```{translatedhadith["hadiths"][0]["text"]}```''')
            embed.add_field(name='Information', value=f'''**Translation:** {translation}
**Grades:**
{grades_str}''')
            embed.set_author(icon_url=self.bot.user.avatar, name=author['author_name'])
            await interaction.followup.send(embed=embed)
        except Exception as e:
            await interaction.followup.send('You provided an invalid reference!', ephemeral=True)

async def setup(bot):
    await bot.add_cog(HadithCog(bot))