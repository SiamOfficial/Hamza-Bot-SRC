import json
import aiohttp
import random
import datetime

today = datetime.date.today()
formatted_date = today.strftime("%d-%m-%Y")

#function for getting dua
with open('duas.json', 'r', encoding='utf-8') as f:
    duas = json.load(f)
async def get_dua(index: int) -> dict:
    for dua in duas:
        if dua['index'] == index:
            return dua
    return None

#for getting chapter info
async def get_chapter_info(index: int) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get('https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/info.json') as response:
            data = await response.json()
            chapter_info = next((chapter for chapter in data['chapters'] if chapter['chapter'] == index), None)
            if chapter_info:
                return chapter_info
            else:
                return {}

# For getting chapter
async def get_chapter(index: int, author: str) -> dict:
    url = f'https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/{author}/{index}.json'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.ok:
                data = await response.json()
                return data
            else:
                return {}
    
# For getting verse
async def get_verse(chapter: int, verse: int, author: str) -> dict:
    url = f'https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions/{author}/{chapter}/{verse}.json'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.ok:
                data = await response.json()
                return data
            else:
                return {}
    
#translator's info
async def get_author_info(name: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get('https://cdn.jsdelivr.net/gh/fawazahmed0/quran-api@1/editions.json') as response:
            data = await response.json()
            author_info = next((author for author in data.values() if author['name'] == name), None)
            if author_info:
                return author_info
            else:
                return {}

# For getting hadith
async def get_hadith(book: str, hadith: int):
    url = f'https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1/editions/{book}/{hadith}.json'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.ok:
                data = await response.json()
                return data
            else:
                return None

#getting hadith number for random hadith cmd
async def get_hadith_number(book: str):
    url = f'https://cdn.jsdelivr.net/gh/fawazahmed0/hadith-api@1/editions/ara-{book}.json'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.ok:
                data = await response.json()
                hadiths = data['hadiths']
                hadith = random.randint(1, len(hadiths))
                return hadith
            
# For getting tafsir
async def get_tafsir(chapter: int, verse: int, mufassir: str):
    url = f'http://api.quran.com/api/v3/chapters/{chapter}/verses/{verse}/tafsirs/{mufassir}'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.ok:
                data = await response.json()
                return data
            else:
                return None
    
async def get_recitor_info(id: int) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.quran.com/api/v4/resources/recitations?language=en') as response:
            if response.ok:
                data = await response.json()
                for i in range(len(data['recitations'])):
                    if data['recitations'][i]['id'] == id:
                        return data['recitations'][i]
                return {}
            else:
                return {}

            
async def get_chapter_recitation(recitor: int, chapter: int) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.quran.com/api/v4/chapter_recitations/{recitor}/{chapter}') as response:
            if response.ok:
                data = await response.json()
                return data['audio_file']
            
async def get_verse_recitation(recitor: int, chapter: int, verse: int) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.quran.com/api/v4/recitations/{recitor}/by_ayah/{chapter}:{verse}') as response:
            if response.ok:
                data = await response.json()
                return data['audio_files'][0]
            
async def get_adhan(index: int) -> dict:
    with open('adhan.json', 'r', encoding='utf-8') as f:
        adhans = json.load(f)

    for adhan in adhans:
        if adhan['index'] == index:
            return adhan
        
async def get_nasheed(index: int) -> dict:
    with open('nasheeds.json', 'r', encoding='utf-8') as f:
        nasheeds = json.load(f)

    for nasheed in nasheeds:
        if nasheed['index'] == index:
            return nasheed

async def get_hadith_author(book: str) -> dict:
    with open('hadith.json', 'r', encoding='utf-8') as f:
        hadiths = json.load(f)

    for hadith in hadiths:
        if hadith["name"] == book:
            return hadith
        
async def get_prayer_times(city: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.aladhan.com/v1/timingsByCity/{formatted_date}?city={city}&country=&method=2') as response:
            if response.ok:
                data = await response.json()
                return data['data']