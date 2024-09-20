# import requests
# from bs4 import BeautifulSoup
# import time
# import datetime
# import asyncio
#
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
# }
# html = requests.get('https://www.kommersant.ru/rubric/3', headers=headers).text
# soup = BeautifulSoup(html, 'html.parser')
# # print(soup.get_text())
# # Поиск элемента по атрибуту data-tes
# title_news = soup.find_all('article')
# for i in title_news:
#     print(i.contents)


