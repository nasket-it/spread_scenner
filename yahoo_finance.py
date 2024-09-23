from datetime import datetime, time
import re
import pytz
import asyncio
# import yfinance as yf
from tinkoff_get_func import calculate_percentage
import aiohttp
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET


# class CurrencyData:
#     def __init__(self):
#         self.yahoo_valyata = {}
yahoo_valyata = {}
fanding = {}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


async def time_diapazone(start_time_str, end_time_str):
    moscow_tz = pytz.timezone('Europe/Moscow')
    current_time_moscow = datetime.now(moscow_tz).time()

    start_time = datetime.strptime(start_time_str, "%H:%M").time()
    end_time = datetime.strptime(end_time_str, "%H:%M").time()

    # Если диапазон времени пересекает полночь
    if start_time > end_time:
        # Текущее время должно быть либо после start_time и до полуночи, либо после полуночи и до end_time
        return current_time_moscow >= start_time or current_time_moscow <= end_time
    else:
        # Текущее время должно быть между start_time и end_time
        return start_time <= current_time_moscow <= end_time

async def parse_site_dohod():
    url2 = "https://www.dohod.ru/ik/analytics/dividend"

    async with aiohttp.ClientSession() as session1:
        # print('11111')
        async with session1.get(url2, headers=headers) as response2:
            # await asyncio.sleep(3)
            html = await response2.text()
            print(html)
            # Создаем дерево элементов из XML-данных
            # root = ET.fromstring(html)
            #
            # # Находим все элементы <row> и выводим их атрибуты SECID и SWAPRATE
            # for row in root.findall(".//row"):
            #     secid = row.get('SECID')
            #     swaprate = row.get('SWAPRATE')
            #     if float(swaprate) != 0:
            #         fanding[secid] = swaprate
        #



async def get_fanding_moex():
    url2 = "https://iss.moex.com/iss/engines/futures/markets/forts/securities?securities=IMOEXF,GLDRUBF,USDRUBF,EURRUBF,CNYRUBF&iss.meta=off&iss.only=marketdata&marketdata.columns=SECID,SWAPRATE"

    async with aiohttp.ClientSession() as session1:
        # print('11111')
        async with session1.get(url2, headers=headers) as response2:
            # await asyncio.sleep(3)
            html = await response2.text()
            # Создаем дерево элементов из XML-данных
            root = ET.fromstring(html)

            # Находим все элементы <row> и выводим их атрибуты SECID и SWAPRATE
            for row in root.findall(".//row"):
                secid = row.get('SECID')
                swaprate = row.get('SWAPRATE')
                if float(swaprate) != 0 :
                    fanding[secid] = swaprate
        #
        #
#

async def parse_futures_investing(future):
    url = {
            "brent_fut" : "https://ru.investing.com/commodities/brent-oil-streaming-chart",
            "gas_fut" : "https://ru.investing.com/commodities/natural-gas-streaming-chart",
            "gold_fut" : "https://ru.investing.com/commodities/gold-streaming-chart",
            "silver_fut" : "https://ru.investing.com/commodities/silver-streaming-chart",
            "gold_spot" : "https://ru.investing.com/currencies/xau-usd-chart",
            "nasdaq" : "https://ru.investing.com/indices/nq-100-futures-chart?cid=1175151",
            "sp500" : "https://ru.investing.com/indices/us-spx-500-futures-chart?cid=1175153",
            'QQQ':  'https://ru.investing.com/etfs/powershares-qqqq-chart'
           }

    async with aiohttp.ClientSession() as session:
        # print('11111')
        async with session.get(url[future], headers=headers) as response:
            # print('222222')
            html = await response.text()
            # print(html)
            soup = BeautifulSoup(html, 'html.parser')
            # Поиск элемента по атрибуту data-test
            if future == 'QQQ':
                pass
                # price = soup.find('span', class_='text-base/6 text-[#232526]').text.strip()
                # percent = 0.01
                # print(f"qqq price - {price}")
            else:
                price = soup.find('div', {'data-test': 'instrument-price-last'}).text
                percent = soup.find('span', {'data-test': 'instrument-price-change-percent'}).text
            # print(price, percent)
            if price:
                # print(price, percent)
                return price, percent
            else:
                print(None, None)
                return None, None


async def parse_valuta_invtsting(currency1, currency2, url=True):
    if url:
        url = f"https://ru.investing.com/currencies/{currency1.lower()}-{currency2.lower()}-chart"
    else:
        url = f"https://ru.investing.com/currencies/{currency1.lower()}-{currency2.lower()}-chart?cid=993160"
    # print(url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            html = await response.text()
            # print(html)
            soup = BeautifulSoup(html, 'html.parser')
            # Поиск элемента по атрибуту data-test
            price = soup.find('div', {'data-test': 'instrument-price-last'}).text
            percent = soup.find('span', {'data-test': 'instrument-price-change-percent'}).text
            # print(price, percent)
            if price:
                # print(price, percent)
                return price, percent
            else:
                return None, None

async def subbota_voskresen():
    today = datetime.today().weekday()
    # В Python понедельник - 0, воскресенье - 6
    return today == 5 or today == 6


count = 0
async def dict_yahoo_valuta():
    prices_valuta = {}
    price_futures = {}
    global yahoo_valyata
    global count
    fut = ["brent_fut", "gas_fut", "gold_fut", "silver_fut", "gold_spot", "nasdaq", "sp500"]
    symbols = ["USDRUB","XAUUSD", "XAGUSD", "USDTRY", "EURTRY", "USDKZT", "EURKZT", "EURCNH", "EURRUB", "USDCNH", "EURUSD", "CNYRUB",
               "CNYUSD", "brent_fut", "gas_fut", "gold_fut", "silver_fut", "gold_spot", "nasdaq", "sp500"]
    vihodnie = await subbota_voskresen()
    diapazone_23_6 = await time_diapazone('23:30', '06:00')
    # await parse_site()
    #---
    for i in symbols:
        if i in fut:
            rezult = await parse_futures_investing(i)
        else:
            rezult = await parse_valuta_invtsting(i[:3], i[3:6])
        if rezult[0] and rezult[1]:
            prices_valuta[i] = [rezult[0], rezult[1]]
        await asyncio.sleep(0.5)
    yahoo_valyata['valuta'] = prices_valuta
    count += 1
    print(yahoo_valyata, count)
    #---
    # try:
    #     while True:
    #         vihodnie = await subbota_voskresen()
    #         diapazone_23_6 = await time_diapazone('23:30', '06:00')
    #         # await parse_site()
    #         try:
    #             for i in symbols:
    #                 if  i in fut:
    #                     rezult = await parse_futures_investing(i)
    #                 else:
    #                     rezult = await parse_valuta_invtsting(i[:3], i[3:6])
    #                 if rezult[0] and rezult[1] :
    #                     prices_valuta[i] = [rezult[0], rezult[1]]
    #                 await asyncio.sleep(0.5)
    #             yahoo_valyata['valuta'] = prices_valuta
    #             await asyncio.sleep(60) if vihodnie or diapazone_23_6 else await asyncio.sleep(5)
    #             # print(f"Выходные llllllllllllllll - {diapazone_23_6} ")
    #         except Exception as e:
    #             print("Ошибка:", e)  # Выводим ошибку
    #             await asyncio.sleep(5)
    #             await dict_yahoo_valuta()
    # except KeyboardInterrupt:
    #     print('Программа остановлена пользователем')




