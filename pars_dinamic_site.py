import aiohttp
import asyncio
from bs4 import BeautifulSoup


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def fetch_dividend_data(url):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        soup = BeautifulSoup(html, 'html.parser')
        print(soup)

        # Найти таблицу "Предстоящие закрытия реестра"
        table_section = soup.find('div', {'class': 'dividends-calendar'})
        if not table_section:
            print("Table section not found")
            return []

        tables = table_section.find_all('table')
        if not tables:
            print("Tables not found")
            return []

        # Попробуем найти таблицу с заголовком "Предстоящие закрытия реестра"
        data = []
        for table in tables:
            header = table.find_previous_sibling('h2')
            if header and "Предстоящие закрытия реестра" in header.text:
                headers = [header.text.strip() for header in table.find_all('th')]
                data.append(headers)

                for row in table.find_all('tr'):
                    cols = row.find_all('td')
                    if cols:
                        data.append([col.text.strip() for col in cols])
                break

        # return data
        print(data)


async def main():
    url = 'https://bcs-express.ru/dividednyj-kalendar'
    data = await fetch_dividend_data(url)
    return data


# # Запуск асинхронного выполнения
# data = asyncio.get_event_loop().run_until_complete(main())
# for row in data:
#     print(row)
