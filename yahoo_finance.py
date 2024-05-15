
import asyncio
# import yfinance as yf
from tinkoff_get_func import calculate_percentage
import aiohttp
import requests
from bs4 import BeautifulSoup

# class CurrencyData:
#     def __init__(self):
#         self.yahoo_valyata = {}
yahoo_valyata = {}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


async def parse_futures_investing(future):
    url = {
            "brent_fut" : "https://ru.investing.com/commodities/brent-oil-streaming-chart",
            "gas_fut" : "https://ru.investing.com/commodities/natural-gas-streaming-chart",
            "gold_fut" : "https://ru.investing.com/commodities/gold-streaming-chart",
            "silver_fut" : "https://ru.investing.com/commodities/silver-streaming-chart",
            "gold_spot" : "https://ru.investing.com/currencies/xau-usd-chart",
            "nasdaq" : "https://ru.investing.com/indices/nq-100-futures-chart?cid=1175151",
            "sp500" : "https://ru.investing.com/indices/us-spx-500-futures-chart?cid=1175153"
           }
    async with aiohttp.ClientSession() as session:
        print('11111')
        async with session.get(url[future], headers=headers) as response:
            print('222222')
            html = await response.text()
            # print(html)
            soup = BeautifulSoup(html, 'html.parser')
            # Поиск элемента по атрибуту data-test
            price = soup.find('div', {'data-test': 'instrument-price-last'}).text
            percent = soup.find('span', {'data-test': 'instrument-price-change-percent'}).text
            print(price, percent)
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
            print(price, percent)
            if price:
                # print(price, percent)
                return price, percent
            else:
                return None, None


async def dict_yahoo_valuta():
    prices_valuta = {}
    price_futures = {}
    global yahoo_valyata
    fut = ["brent_fut", "gas_fut", "gold_fut", "silver_fut", "gold_spot", "nasdaq", "sp500"]
    symbols = ["XAUUSD", "XAGUSD", "USDTRY", "EURTRY", "USDKZT", "EURKZT", "EURCNH", "EURRUB", "USDCNH", "EURUSD", "CNYRUB",
               "CNYUSD", "brent_fut", "gas_fut", "gold_fut", "silver_fut", "gold_spot", "nasdaq", "sp500"]
    while True:
        try:
            for i in symbols:
                # print('0000000')
                if i == "EURRUB":
                    rezult = await parse_valuta_invtsting(i[:3], i[3:6], url=False)
                elif i in fut:
                    rezult = await parse_futures_investing(i)
                else:
                    rezult = await parse_valuta_invtsting(i[:3], i[3:6])
                if rezult[0] and rezult[1] :
                    prices_valuta[i] = [rezult[0], rezult[1]]
                await asyncio.sleep(0.5)
            yahoo_valyata['valuta'] = prices_valuta

            print(yahoo_valyata)
            # print(await parse_futures_investing())
            await asyncio.sleep(5)
        except Exception as e:
            print("Ошибка:", e)  # Выводим ошибку
            await asyncio.sleep(5)
            await dict_yahoo_valuta()



