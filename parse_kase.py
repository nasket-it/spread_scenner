import datetime
import time
import pytz
# from datetime import datetime
import asyncio
from secrete import LoginPasword, Flag
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import pandas as pd
moscow_tz = pytz.timezone('Europe/Moscow')

kase_curen_dict = {}


async def is_valid_float(string):
    # Убираем возможный знак минуса и десятичный разделитель
    string = string.replace('.', '').lstrip('-')
    # Проверяем, состоит ли строка только из цифр
    return string.isdigit()



async def new_text_kase_current(data_dict):
    # data_dict = kase_curen_dict
    def valyta_smail( percent):
        if percent < 0:
            return '📕'
        if percent > 0:
            return '📗'
        if percent == 0:
            return "📘"

    def link_text(text, link="https://t.me/cricket_scan"):
        return f'<a href="{link}">{text}</a>'

    def _podcher_text(text):
        return f'<u>{text}</u>'

    def _zirniy_text(text):
        return f'<b>{text}</b>'

    time_apgrade = datetime.datetime.now(moscow_tz)
    time_new = time_apgrade.strftime("%H:%M:%S")
    if data_dict:
        cnykzt_bid = data_dict["CNYKZT_TOM"]["bid"] if await is_valid_float(data_dict["CNYKZT_TOM"]["bid"])  else False
        eurkzt_bid = data_dict["EURKZT_TOM"]["bid"] if await is_valid_float(data_dict["EURKZT_TOM"]["bid"])  else False
        usdkzt_bid = data_dict["USDKZT_TOM"]["bid"] if await is_valid_float(data_dict["USDKZT_TOM"]["bid"])  else False
        rubkzt_bid = data_dict["RUBKZT_TOM"]["bid"] if await is_valid_float(data_dict["RUBKZT_TOM"]["bid"])  else False
        if rubkzt_bid:
            cross_cnyrub = float(cnykzt_bid) / float(rubkzt_bid) if cnykzt_bid  else 0
            cross_eurrub = float(eurkzt_bid) / float(rubkzt_bid) if eurkzt_bid else 0
            cross_usdrub = float(usdkzt_bid) / float(rubkzt_bid) if usdkzt_bid else 0
        else:
            cross_cnyrub = 0
            cross_eurrub = 0
            cross_usdrub = 0

        link = "https://t.me/cricket_scan"
        stroka1 = f'🧭 Время последнего обновления:\n{time_apgrade.date()}  время: {time_new}'
        stroka2 = f'Просмотр торгов КАЗАХСТАН'
        stroka3 = f'🇨🇳 🇰🇿 CNYKZT_TOM :'
        stroka4 = f'Bid : {cnykzt_bid}    |    {data_dict["CNYKZT_TOM"]["ask"]} : Ask'
        stroka5 = f'🇪🇺 🇰🇿 EURKZT_TOM :'
        stroka6 = f'Bid : {eurkzt_bid}    |    {data_dict["EURKZT_TOM"]["ask"]} : Ask'
        stroka7 = f'🇷🇺 🇰🇿 RUBKZT_TOM :'
        stroka8 = f'Bid : {rubkzt_bid}    |    {data_dict["RUBKZT_TOM"]["ask"]} : Ask'
        stroka9 = f'🇺🇸 🇰🇿 USDKZT_TOM :'
        stroka10 = f'Bid : {usdkzt_bid}    |    {data_dict["USDKZT_TOM"]["ask"]} : Ask'
        stroka11 = f'Кросс курсы KZT(KASE):  '
        stroka12 = f'🇨🇳CNYRUB : {cross_cnyrub}'
        stroka13 = f'🇪🇺EURRUB : {cross_eurrub}'
        stroka14 = f'🇺🇸USDRUB : {cross_usdrub}'
        message = f"{stroka1}\n\n" \
                  f"{stroka2}\n" \
                  f"{stroka3}\n" \
                  f"{stroka4}\n\n" \
                  f"{stroka5}\n" \
                  f"{stroka6}\n\n" \
                  f"{stroka7}\n" \
                  f"{stroka8}\n\n" \
                  f"{stroka9}\n" \
                  f"{stroka10}\n\n" \
                  f"{stroka11}\n" \
                  f"{stroka12}\n" \
                  f"{stroka13}\n" \
                  f"{stroka14}\n" \

        return message




async def login_to_kase(page):
    await page.goto("https://kase.kz/ru/currency/")
    await page.click("text='Войти'")
    await asyncio.sleep(5)
    await page.fill("#id_username", LoginPasword.kase_login)
    await page.fill("#id_password", LoginPasword.kase_pasword)
    await page.click("button[type='submit'] span:has-text('Войти')")
    await asyncio.sleep(3)

async def parse_price_curent_kase(kase_curen_dict: dict):
    if Flag.vikl_parse_kase:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()
            # Логинимся один раз
            await login_to_kase(page)

            # Парсим таблицу
            while Flag.vikl_parse_kase:
                table = await page.query_selector_all('table.watchlist__table tr')
                for row in table:
                    columns = await row.query_selector_all('td')
                    row_data = [await col.inner_text() for col in columns]
                    if row_data:
                        kase_curen_dict[row_data[0]] = {
                            'status_torg': row_data[1], 'bid': row_data[2], 'qbid': row_data[3],
                            'vbid': row_data[4], 'spresd': row_data[5], 'spread%': row_data[6],
                            'ask': row_data[7], 'qask': row_data[8], 'open': row_data[9],
                            'last(close)': row_data[10], 'qlast': row_data[11], 'sdelki': row_data[12],
                            'q': row_data[13], 'v': row_data[14], 'v$': row_data[15], 'date': row_data[16],
                            'time': row_data[17]
                        }
                await asyncio.sleep(1)




# async def parse_price_curent_kase(kase_curen_dict : dict):
#     # Запускаем Playwright
#     async with async_playwright() as p:
#         # Открываем браузер (в данном случае Chromium)
#         browser = await p.chromium.launch(headless=True)  # Установите headless=True для работы без интерфейса
#         # Открываем новую вкладку
#         context = await browser.new_context()
#         page = await context.new_page()
#         # Переходим на сайт
#         await page.goto("https://kase.kz/ru/currency/")
#         # Найти кнопку с текстом "Войти" и кликнуть
#         await page.click("text='Войти'")
#         await asyncio.sleep(5)
#         await page.fill("#id_username", LoginPasword.kase_login)
#         await page.fill("#id_password", LoginPasword.kase_pasword)
#         await asyncio.sleep(5)
#         await page.click("button[type='submit'] span:has-text('Войти')")
#         await asyncio.sleep(3)
#
#         table = await page.query_selector_all('table.watchlist__table tr')
#         await asyncio.sleep(3)
#         while table:
#             for row in table:
#                 columns = await row.query_selector_all('td')  # Извлекаем все ячейки (td) в строке
#                 row_data = [await col.inner_text() for col in columns]  # Получаем текст внутри ячеек
#                 if row_data:  # Если строка не пустая
#                     kase_curen_dict[row_data[0]] = {'status_torg' : row_data[1], 'bid' : row_data[2], 'qbid' :row_data[3],
#                                               'vbid' : row_data[4], 'spresd' : row_data[5], 'spread%' : row_data[6],
#                                               'ask' : row_data[7], 'qask' : row_data[8], 'open' : row_data[9],
#                                               'last(close)' : row_data[10] , 'qlast' : row_data[11], 'sdelki' : row_data[12],
#                                               'q' : row_data[13], 'v' : row_data[14], 'v$' : row_data[15], 'date' : row_data[16],
#                                                'time' : row_data[17]}
#             # print(table_data)
#             await asyncio.sleep(1)
#
#         # Закрываем браузер
#         await browser.close()

# Запускаем асинхронную функцию
# asyncio.run(parse_price_curent_kase(kase_curen_dict))
