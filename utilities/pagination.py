import discord
import asyncio
import html
import re
from utilities.converting import convert_to_arabic_number
from utilities.functions import get_author_info, get_chapter, get_chapter_info, get_tafsir
import json
# Pagination for chapter
class ChapterPaginator(discord.ui.View):
    def __init__(self, bot, chapter, translation, author):
        super().__init__()
        self.pages = []
        self.current = 0
        self.message = None
        self.chapter = chapter
        self.bot = bot
        self.translation = translation
        self.author = author

    async def start(self, interaction):
        chapterdata = await get_chapter_info(index=int(self.chapter))
        getchapter = await get_chapter(index=int(self.chapter), author=self.translation)
        getarabicchapter = await get_chapter(index=int(self.chapter), author='ara-quranacademy')
        authordata = await get_author_info(name=self.translation)
        verses_list = []
        verses_arabic_list = []
        for verse in getchapter['chapter']:
            verses_list.append(verse['text'])
        for verse in getarabicchapter['chapter']:
            verses_arabic_list.append(verse['text'])
        pages = []
        arabic = convert_to_arabic_number(f'{self.chapter}')
        for i in range(0, len(verses_list)):
            embed = discord.Embed(
                title=f'{self.chapter} ({chapterdata["name"]}) | {arabic} ({chapterdata["arabicname"]})',
                description=f'```{"".join(verses_arabic_list[i:i+1])}```\n```{"".join(verses_list[i:i+1])}```'
            )
            embed.add_field(name='Information', value=f'**Translation:** {authordata["language"]}\n**Revelation Place:** {chapterdata["revelation"]}')
            embed.set_author(icon_url=self.bot.user.avatar, name=authordata['author'])
            embed.set_footer(text=f'Verse {i+1} of {len(verses_list)}')
            embed.set_image(url=f'https://hamzabot.me/everyayah.com/{str(self.chapter)}_{i+1}.png')
            pages.append(embed)
        self.pages = pages

        embed = self.pages[self.current]
        self.message = await interaction.followup.send(embed=embed, view=self)
        if len(self.pages) > 1:
            await self.message.edit(view=self)
        if len(self.pages) == 1:
            self.next_page.disabled = True
            await self.message.edit(view=self)

    @discord.ui.button(label='Previous', style=discord.ButtonStyle.green, disabled=True)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.next_page.disabled = False
        if self.current == 1:
            self.previous_page.disabled = True
        self.current -= 1
        embed = self.pages[self.current]
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label='Next', style=discord.ButtonStyle.green)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.previous_page.disabled = False
        if self.current == len(self.pages) - 2:
            self.next_page.disabled = True
        self.current += 1
        embed = self.pages[self.current]
        await interaction.response.edit_message(embed=embed, view=self)

        asyncio.create_task(self.update_footer())
        asyncio.create_task(self.update_image())
    async def update_footer(self):
        try:
            embed = self.pages[self.current]
            embed.set_footer(text=f'Verse {self.current + 1} of {len(self.pages)}')
            await self.message.edit(embed=embed, view=self)

        except discord.errors.NotFound:
            pass

    async def update_image(self):
        try:
            embed = self.pages[self.current]
            image_url = f'https://hamzabot.me/everyayah.com/{self.chapter}_{self.current + 1}.png'
            embed.set_image(url=image_url)
            await self.message.edit(embed=embed, view=self)

        except discord.errors.NotFound:
            pass
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.author.id:
            try:
                await interaction.response.send_message('This command is not for you!', ephemeral=True)
            except discord.errors.NotFound:
                pass
            return False
        return True

#Pagination for tafsir
class TafsirPaginator(discord.ui.View):
    def __init__(self, bot, chapter, verse, mufassir, author):
        super().__init__()
        self.pages = []
        self.bot = bot
        self.chapter = chapter
        self.verse = verse
        self.mufassir = mufassir
        self.current = 0
        self.author = author
        self.message = None
    async def start(self, interaction):
        gettafsir = await get_tafsir(chapter=self.chapter, verse=self.verse, mufassir=self.mufassir)
        chapterdata = await get_chapter_info(index=int(self.chapter))
        text = gettafsir['tafsir']['text']
        text = html.unescape(text)
        text = re.sub('<.*?>', '', text)
        numpages = len(text) / 1000 + 1
        numpages = str(numpages).split('.')
        pages = []
        arabic = convert_to_arabic_number(f'{self.chapter}:{self.verse}')
        for i in range(0, len(text), 1000):
            embed = discord.Embed(title=f'{self.chapter}:{self.verse} ({chapterdata["name"]}) | {arabic} ({chapterdata["arabicname"]})',
                                  description=f'''```{text[i:i+1000]}```''')
            embed.add_field(name='Information', value=f'''**Language:** {gettafsir['tafsir']['language_name'].title()}
**Revelation Place:** {chapterdata['revelation']}''')
            embed.set_author(icon_url=self.bot.user.avatar, name=gettafsir['tafsir']['resource_name'])
            embed.set_footer(text=f'Page {i // 1000 + 1} of {numpages[0]}')
            embed.set_image(url=f'https://hamzabot.me/everyayah.com/{self.chapter}_{self.verse}.png')
            pages.append(embed)
        self.pages = pages
        embed = self.pages[self.current]
        self.message = await interaction.followup.send(embed=embed, view=self)
        if len(self.pages) > 1:
            await self.message.edit(view=self)
        if len(self.pages) == 1:
            self.next_page.disabled = True
            await self.message.edit(view=self)

    @discord.ui.button(label='Previous', style=discord.ButtonStyle.green, disabled=True)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.next_page.disabled = False
        if self.current == 1:
            self.previous_page.disabled = True
        self.current -= 1
        embed = self.pages[self.current]
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label='Next', style=discord.ButtonStyle.green)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.previous_page.disabled = False
        if self.current == len(self.pages) - 2:
            self.next_page.disabled = True
        self.current += 1
        embed = self.pages[self.current]
        await interaction.response.edit_message(embed=embed, view=self)

        asyncio.create_task(self.update_footer())
    async def update_footer(self):
        try:
            embed = self.pages[self.current]
            embed.set_footer(text=f'Page {self.current + 1} of {len(self.pages)}')
            await self.message.edit(embed=embed, view=self)

        except discord.errors.NotFound:
            pass
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.author.id:
            try:
                await interaction.response.send_message('This command is not for you!', ephemeral=True)
            except discord.errors.NotFound:
                pass
            return False
        return True

#Pagination for pages of the quran
class PagePaginator(discord.ui.View):
    def __init__(self, bot, author):
        super().__init__()
        self.pages = []
        self.bot = bot
        self.current = 0
        self.message = None
        self.author = author
    async def start(self, interaction):
        pages = []
        page_num = []
        pages_list = list(range(1, 605))
        for page in pages_list:
            page_num.append(str(page))
        for i in range(len(page_num)):
            embed = discord.Embed(title=f'Page {i+1} | صفحة {convert_to_arabic_number(f"{i+1}")}')
            embed.set_author(icon_url=self.bot.user.avatar, name='Pages by zeyadetman')
            embed.set_image(url=f'https://hamzabot.me/zeyadetman/{i+1}.jpg')
            embed.set_footer(text=f'Page {i+1} of 604 pages')
            pages.append(embed)
        self.pages = pages
        embed = self.pages[self.current]
        self.message = await interaction.followup.send(embed=embed, view=self)
        if len(self.pages) > 1:
            await self.message.edit(view=self)
        if len(self.pages) == 1:
            self.next_page.disabled = True
            await self.message.edit(view=self)

    @discord.ui.button(label='Previous', style=discord.ButtonStyle.green, disabled=True)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.next_page.disabled = False
        if self.current == 1:
            self.previous_page.disabled = True
        self.current -= 1
        embed = self.pages[self.current]
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label='Next', style=discord.ButtonStyle.green)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.previous_page.disabled = False
        if self.current == len(self.pages) - 2:
            self.next_page.disabled = True
        self.current += 1
        embed = self.pages[self.current]
        await interaction.response.edit_message(embed=embed, view=self)

        asyncio.create_task(self.update_footer())
        asyncio.create_task(self.update_image())
        asyncio.create_task(self.update_title())
    async def update_footer(self):
        try:
            embed = self.pages[self.current]
            embed.set_footer(text=f'Page {self.current + 1} of 604 pages')
            await self.message.edit(embed=embed, view=self)

        except discord.errors.NotFound:
            pass

    async def update_image(self):
        try:
            embed = self.pages[self.current]
            image_url = f'https://hamzabot.me/zeyadetman/{self.current + 1}.jpg'
            embed.set_image(url=image_url)
            await self.message.edit(embed=embed, view=self)

        except discord.errors.NotFound:
            pass
    async def update_title(self):
        try:
            embed = self.pages[self.current]
            page_number_str = str(self.current + 1)
            embed_title = f'Page {page_number_str} | صفحة {convert_to_arabic_number(page_number_str)}'
            embed.title = embed_title
            await self.message.edit(embed=embed, view=self)


        except discord.errors.NotFound:
            pass

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.author.id:
            try:
                await interaction.response.send_message('This command is not for you!', ephemeral=True)
            except discord.errors.NotFound:
                pass
            return False
        return True
    
#ACHIEVEMENTS 
class AchievementsPaginator(discord.ui.View):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.pages = []
        self.current = 0
        self.message = None

    async def start(self, interaction):
        pages = []
        with open('achievements.json', 'r', encoding='utf-8') as f:
            achievements = json.load(f)
            name_list = []
            description_list = []
            progress_list = []
            date_list = []
            for item in achievements:
                name_list.append(item['name'])
                description_list.append(item['description'])
                progress_list.append(item['progress'])
                date_list.append(item['date'])

            numpages = ((len(name_list) - 1) // 4) + 1

            for i in range(0, len(name_list), 4):
                embed = discord.Embed(title='Achievements', description='Achievements of Hamza Bot.')
                for j in range(i, min(i + 4, len(name_list))):
                    embed.add_field(
                        name=name_list[j],
                        value=f"**Description**: {description_list[j]}\n"
                              f"**Progress**: {progress_list[j]}\n"
                              f"**Date**: {date_list[j]}\n"
                    )
                embed.set_footer(text=f"Page {i // 4 + 1} of {numpages}")
                pages.append(embed)
            self.pages = pages

        embed = self.pages[self.current]
        self.message = await interaction.followup.send(embed=embed, view=self)
        if len(self.pages) > 1:
            await self.message.edit(view=self)
        if len(self.pages) == 1:
            self.next_page.disabled = True
            await self.message.edit(view=self)

    @discord.ui.button(label='Previous', style=discord.ButtonStyle.green, disabled=True)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.next_page.disabled = False
        self.current -= 1
        if self.current == 0:
            self.previous_page.disabled = True
        embed = self.pages[self.current]
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label='Next', style=discord.ButtonStyle.green)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.previous_page.disabled = False
        self.current += 1
        if self.current >= len(self.pages) - 1:
            self.next_page.disabled = True
        embed = self.pages[self.current]
        await interaction.response.edit_message(embed=embed, view=self)

    async def update_footer(self):
        try:
            embed = self.pages[self.current]
            embed.set_footer(text=f"Page {self.current // 4 + 1} of {len(self.pages) // 4}")
            await self.message.edit(embed=embed, view=self)
        except discord.errors.NotFound:
            pass