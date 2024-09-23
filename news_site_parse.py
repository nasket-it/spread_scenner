import aiohttp
import requests
from bs4 import BeautifulSoup
from lxml import html
from rss_parser import rebrentext_send_discord_telegram
import time
import datetime
import asyncio


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


async def fetch(session, url):
    async with session.get(url,headers=headers) as response:
        return await response.text()


dividend_data = {}
async def parse_rbk(list_last_news: list, bot, func_link):
    url_rbk = 'https://www.rbc.ru/economics/'
    async with aiohttp.ClientSession() as session:
        list_sravnrniya = []
        html_rbk = await fetch(session, url_rbk)
        rbk = html.fromstring(html_rbk)
        # 1. Получение текста внутри тега <p>
        news_title_rbk = rbk.xpath('//span[@class="normal-wrap"]/text()')
        if news_title_rbk != list_sravnrniya:
            list_sravnrniya = news_title_rbk
            for i in list_sravnrniya:
                if i in list_last_news:
                    pass
                else:
                    list_last_news.append(i)
                    await rebrentext_send_discord_telegram(i, bot=bot, func_link_text=func_link)



async def parse_komersant(list_last_news: list, bot, func_link):
    url_komersant = 'https://www.kommersant.ru/rubric/3'
    async with aiohttp.ClientSession() as session:
        list_sravnrniya = []
        html_kom = await fetch(session, url_komersant)
        komersant = html.fromstring(html_kom)
        news_title_komersant = komersant.xpath('//article//@data-article-title')
        if news_title_komersant != list_sravnrniya:
            list_sravnrniya = news_title_komersant
            for i in list_sravnrniya:
                if i in list_last_news:
                    pass
                else:
                    list_last_news.append(i)
                    await rebrentext_send_discord_telegram(i, bot=bot, func_link_text=func_link)


        # print(news_title_komersant)

# url_rbk = 'https://www.rbc.ru/economics/'
url_komersant = 'https://www.kommersant.ru/rubric/3'
#
html_kom = requests.get(url_komersant, headers=headers).text
# html_rbk= requests.get(url_rbk, headers=headers).text
# # soup = BeautifulSoup(html1, 'html.parser')
# # print(soup.get_text())
# # Поиск элемента по атрибуту data-tes
#
# rbk = html.fromstring(html_rbk)
komersant = html.fromstring(html_kom)
#
# # 1. Получение текста внутри тега <p>
news_title_komersant = komersant.xpath('//article[@data-article-title]')#//@data-article-title'
for i in news_title_komersant:
    title = i.get('data-article-title', None)
    description = i.get('data-article-description', None)
    url_all_post = i.get('data-article-url', None)

    print(f"{title}\n{description}\n{url_all_post}")
# news_title_rbk = rbk.xpath('//span[@class="normal-wrap"]/text()')
#
print(news_title_komersant)



import traceback
import sys

def capture_error():
    try:
        # Ваш код, который может вызвать ошибку
        result = 1 / 0  # Пример ошибки
    except Exception:

        time_apgrade = datetime.datetime.now()
        # Получение информации об ошибке
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback_details = traceback.format_exception(exc_type, exc_value, exc_traceback)
        title_errors = traceback_details[0]
        file_str_errors = ''.join(traceback_details[1:-1])
        name_errors = traceback_details[-1]
        messageErrorTelegram = f"Время и дата: {time_apgrade}\nСтек вызова: {title_errors}\nГде произошла ошибка: {file_str_errors}\nНазвание ошибки: {name_errors}"
        print(messageErrorTelegram)
        # print("Полная информация о стеке вызовов:")
        # print(traceback_details[-2])
        # for line in traceback_details:
        #     print(11, line.strip())

