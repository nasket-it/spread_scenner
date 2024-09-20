import requests
import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime




company_tickers = {

    "ABIO" : "",
    "Русагро" : "AGRO",
    "Роснефть" : "ROSN",
    "Фосагро" : "PHOR",
    "ММК" : "MAGN",
    "Сбербанк-ао" : "SBER",
    "Сбербанк-п" : "SBERP",
    "Fix Price": "FIXP",
    "Сургутнефтегаз-п": "SNGSP",
    "МКПАО ЮМГ (ЕМС)": "EMSS",
    "НЛМК": "NLMK",
    "Совкомфлот": "FLOT",
    "ЛУКОЙЛ": "LKOH",
    "Займер": "ZAIM",
    "Северсталь": "CHMF",
    "ЛСР": "LSRG",
    "Башнефть-п": "BANEP",
    "Банк Санкт-Петербург (БСП)": "BSPB",
    "Магнит": "MGNT",
    "МТС": "MTSS",
    "Евротранс": "ETRN",
    "Татнефть-п": "TATNP",
    "Россети Центр (МРСК Центра)": "MRKC",
    "Россети Центр и Приволжье (МРСК ЦП)": "MRKP",
    "Газпром нефть": "SIBN",
    "Компании стабильных дивидендов": "IRDIV",
    "Татнефть-ао": "TATN",
    "Транснефть-п": "TRNFP",
    "Россети Московский регион (МОЭСК)": "MSRS",
    "НоваБев Групп (Белуга Групп)": "BELU",
    "IRGRO. Индекс акций роста РФ": "IRGRO",
    "Компании LargeCap": "LARGE",
    "Соллерс": "SVAV",
    "Россети Волга (МРСК Волги)": "MRKV",
    "Европлан": "EPLN",
    "Индекс МосБиржи": "IMOEX",
    "Инарктика (РусАква)": "AQUA",
    "Черкизово": "GCHE",
    "Московская биржа": "MOEX",
    "Алроса": "ALRS",
    "Ренессанс Страхование": "RENI",
    "ТМК": "TRMK",
    "Башнефть-ао": "BANE",
    "НМТП": "NMTP",
    "Ростелеком-п": "RTKMP",
    "Красноярскэнергосбыт-ао": "KRSB",
    "Россети Урал (МРСК Урала)": "MRKU",
    "Мать и дитя": "MDMG",
    "Совкомбанк": "SVCB",
    "Ростелеком-ао": "RTKM",
    "АКБ 'Приморье'": "PRMB",
    "КазаньОргСинтез-ао": "KZOSP",
    "HENDERSON": "HEND",
    "Компании MediumCap": "MEDIUM",
    "Таттелеком": "TATTL",
    "НКХП": "NKHP",
    "НКНХ-п": "NKNCP",
    "Куйбышевазот": "KUAZ",
    "Группа Позитив": "POSI",
    "Полюс": "PLZL",
    "ТГК-14": "TGKI",
    "Селигдар ао": "SELGP",
    "Сургутнефтегаз-ао": "SNGS",
    "Камаз": "KMAZ",
    "ГК Самолет": "SMLT",
    "Whoosh": "WHSH",
    "Саратовский НПЗ-ап": "KRKN",
    "ЭсЭфАй (Сафмар)": "SFI",
    "АФК Система": "AFKS",
    "Акрон": "AKRN",
    "Центральный телеграф-п": "CNTLP",
    "ВСМПО-АВИСМА": "VSMO",
    "Группа Астра": "ASTRA",
    "Левенгук": "LEVG",
    "Элемент": "ELMN",
    "Абрау-Дюрсо": "ABRD",
    "Мечел-ао": "MTLR",
    "Мечел-ап": "MTLRP",
    "Эталон": "ETLN",
    "Распадская": "RASP",
    "ОКЕЙ": "OKEY",
    "ТГК-1": "TGKA",
    "ЭЛ5-Энерго (Энел Россия)": "EL5E",
    "М.Видео": "MVID",
    "Аэрофлот": "AFLT",
    "Русал": "RUAL",
    "ПИК": "PIKK",
    "Лента": "LNTA",
    "МКБ": "CBOM",
    "Русгидро": "HYDR",
    "Юнипро": "UPRO",
    "Газпром": "GAZP",
    "Globaltrans": "GLTR",
    "Полиметалл": "POLY",
    "Русснефть-ао": "RNFT",
    "ФСК Россети": "FEES",
    "Россети Северо-Запад (МРСК СЗ)": "MRKZ",
    "Россети Сибирь (МРСК Сибири)": "MRKS",
    "ЮГК": "YUKG",
    "En Plus": "ENPL",
    "ОГК-2": "OGKB",
    "HeadHunter": "HHRU",
    "Сегежа": "SGZH",
    "Яндекс" : "YDEX"

}


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


dividend_data = {}
async def parse_dividend():
    url = 'https://www.dohod.ru/ik/analytics/dividend'
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        soup = BeautifulSoup(html, 'html.parser')
        # Здесь добавьте правильные селекторы для таблицы и её строк
        table = soup.find('table')  # Пример, найдите правильный элемент
        rows = table.find_all('tr')[1:]  # Пропускаем заголовок таблицы
        # print(rows)
        dividend_data.clear()
        for row in rows:
            columns = row.find_all('td')
            columns1 = row.find_all('span')
            div_sovdir = columns1[0]['title'] if columns1 else False
            zak_ree_sovdir = columns1[1]['title'] if columns1 and len(columns1) == 2 else False
            ticker = columns[0].text.strip()
            dividend_rub = float(columns[3].text.strip())
            dohodnost_percent = float(columns[6].text.strip().replace('%', ''))
            date_close = columns[8].text.strip()
            dsi = float(columns[11].text.strip()) if columns[11].text.strip().isdigit() else 0
        #
    #
        # Фильтрация по дате
            date_obj = datetime.strptime(date_close, '%d.%m.%Y').date() if date_close != 'n/a' else False
            tek_data = datetime.now().date()
            if date_obj and tek_data:
                if date_obj > tek_data and dividend_rub > 0 and date_obj <= datetime.strptime('20.12.2024','%d.%m.%Y').date():
                    if company_tickers.get(ticker, False) in dividend_data:
                        dividend_data[company_tickers.get(ticker, None)]['dividend_rub'] += dividend_rub
                    else:
                        dividend_data[company_tickers.get(ticker, None)] = {
                            'name': ticker,
                            'dividend_rub': dividend_rub,
                            'odobrenie': False if  date_close == "n/a" else True,
                            'dohodnost_percent': dohodnost_percent,
                            'date_close': date_close,
                            'dsi': dsi,
                            'odobrenie_div' : div_sovdir if div_sovdir else False,
                            'odobrenie_reestr' : zak_ree_sovdir if zak_ree_sovdir else False,
                            }




async def arb_fut_akcii(price_akcii, price_fut, stavka, date_exp, div_rub):
    print(f"Все данные функции1 - {price_akcii} - {price_fut} - {stavka}  - {date_exp}  - {div_rub}")
    percent_one_day = stavka / 365
    dey_exp = (date_exp - datetime.now().date()).days

    # print(f"dey_exp - {dey_exp}")
    sprav_percent_stavka = percent_one_day * dey_exp
    sprav_price_fut = (price_akcii + ((price_akcii / 100) * sprav_percent_stavka)) - div_rub
    sread = sprav_price_fut / price_fut * 100 - 100

    return sread



def parse_dividend_vsdelke():
    url = 'https://vsdelke.ru/dividendy/kalendar-vyplat-rossiyskih-kompaniy-2024.html'

    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    # Здесь добавьте правильные селекторы для таблицы и её строк
    table = soup.find('table')  # Пример, найдите правильный элемент
    rows = table.find_all('tr')[1:]  # Пропускаем заголовок таблицы
    for row in rows:
        columns = row.find_all('td')
        print(columns[3].text)
# parse_dividend_vsdelke()