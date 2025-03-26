from tinkoff_get_func import price_close_max300day, last_prices
from scipy.stats import norm
from file_zamena_kvartal import Figi_future
from datetime import datetime
from secrete import Token
from black_scholef_func import  theoretical_option_price
import requests
import numpy as np
import time
import pytz
import asyncio
import aiohttp




# Создаем объект временной зоны для Москвы
moscow_tz = pytz.timezone('Europe/Moscow')
dict_otions = {}
dict_histori_volatiliti = {}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

BASE_URL = "https://iss.moex.com/iss/apps/option-calc/v1"
figi = {'Si' : Figi_future.si1_figi, 'Eu' : Figi_future.eu1_figi, 'CNY' : Figi_future.cr1_figi,
        'GOLD' : Figi_future.gold1_figi, 'RTS' : Figi_future.rts1_figi, 'GAZR' : Figi_future.gazr1_figi}
series_options = {'Si': [ 'Si-6.25M270325XA', 'Si-6.25M030425XA', 'Si-6.25M170425XA', 'Si-6.25M150525XA', 'Si-6.25M190625XA'],
                          'Eu': ['Eu-6.25M190625XA'],
                          'CNY': [ 'CNY-6.25M270325XA',  'CNY-6.25M170425XA', 'CNY-6.25M150525XA', 'CNY-6.25M190625XA'],
                          'GOLD': [  'GOLD-6.25M190625XA'],#'GOLD-6.25M270325XA',  'GOLD-6.25M030425XA', 'GOLD-6.25M170425XA',
                          'RTS': [ 'RTS-6.25M270325XA', 'RTS-6.25M030425XA', 'RTS-6.25M170425XA', 'RTS-6.25M150525XA', 'RTS-6.25M190625XA'],
                  'GAZR' : ['GAZR-6.25M180625XA'],#'GAZR-6.25M260325XA', 'GAZR-6.25M020425XA',
                  }

async def black_scholes_price(spot, strike, T, r, sigma):
    """
    Вычисляет теоретическую цену европейского опциона по формуле Блэка-Шоулза.
    Параметры:
    spot (float): Текущая цена базового актива (spot price).
    strike (float): Цена исполнения опциона (strike price).
    T (float): Время до истечения опциона в годах (time to expiration).
    r (float): Безрисковая процентная ставка (risk-free interest rate) в десятичном виде.
    sigma (float): Волатильность базового актива (volatility) в десятичном виде.
    option_type (str): Тип опциона ('call' или 'put').
    Возвращает:
    float: Теоретическая цена опциона.
    """
    # Вычисление d1 и d2
    d1 = (np.log(spot / strike) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_theorprice = spot * norm.cdf(d1) - strike * np.exp(-r * T) * norm.cdf(d2)
    put_theorprice = strike * np.exp(-r * T) * norm.cdf(-d2) - spot * norm.cdf(-d1)
    #формула паритета опционов call - put = price_baze - strake
    # paritete = (call_theorprice - put_theorprice ) - (S - K)
    # theorprice = {'call_theorprice' : call_theorprice, 'put_theorprice' : put_theorprice, 'paritete' : paritete}
    #
    # # Вычисление цены опциона
    # if option_type == 'call':
    #     price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    # elif option_type == 'put':
    #     price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    # else:
    #     raise ValueError("Тип опциона должен быть 'call' или 'put'.")

    return round(put_theorprice, 3), round(call_theorprice, 3)
#     print(f"Теоретическая цена: {theorprice}")

async def optins_smail(percent):
    if percent < 0:
        return '📕'
    elif percent > 0:
        return '📗'
    elif percent == 0:
        return "📘"

async def link_text(text, link="https://t.me/cricket_scan"):
    return f'<a href="{link}">{text}</a>'

async def days_until_expiration(date_str: str) -> int | bool:
    try:
        # Разбираем строку даты
        day = int(date_str[0:2])  # Первые две цифры - день
        month = int(date_str[2:4])  # Следующие две - месяц
        year_suffix = int(date_str[4:6])  # Последние две - год
        # Предполагаем, что год относится к 2000-м годам
        year = 2000 + year_suffix
        # Создаем объект даты из введенных данных
        expiration_date = datetime(year, month, day).date()
        # Получаем текущую дату
        current_date = datetime.now().date()
        # Вычисляем разницу в днях
        delta = (expiration_date - current_date).days
        # Если дата в будущем, возвращаем количество дней, иначе False
        if delta > 0:
            return delta
        else:
            return False
    except ValueError:
        # Если дата некорректна (например, 31 февраля), возвращаем False
        return False

async def histori_volaniliti( list_prices , all_30_60_90=True, period_day=90, param_annalizator_factor=252):
    prices = list_prices
    # Рассчитать логарифмические доходности
    log_returns = np.log(np.array(prices[1:]) / np.array(prices[:-1]))
    if all_30_60_90:
        # Найти стандартное отклонение доходностей
        std_dev_30 = np.std(log_returns[-30:], ddof=1)
        std_dev_60 = np.std(log_returns[-60:], ddof=1)
        std_dev_90 = np.std(log_returns[-90:], ddof=1)
        # Привести к годовому значению
        historical_volatility_30 = round(float(std_dev_30 * np.sqrt(param_annalizator_factor) * 100), 2)
        historical_volatility_60 = round(float(std_dev_60 * np.sqrt(param_annalizator_factor) * 100), 2)
        historical_volatility_90 = round(float(std_dev_90 * np.sqrt(param_annalizator_factor) * 100), 2)
        everenr_volatiliti = round(sum([historical_volatility_30, historical_volatility_60, historical_volatility_90]) / 3, 2)
        # print(f"Историческая волатильность: {historical_volatility_30}  {historical_volatility_60}  {historical_volatility_90}")
        return historical_volatility_30, historical_volatility_60, historical_volatility_90, everenr_volatiliti
    else:
        std_dev = np.std(log_returns[-period_day:], ddof=1)
        historical_volatility = round(float(std_dev * np.sqrt(param_annalizator_factor) * 100), 2)
        # print(f"Историческая волатильность: {historical_volatility:.2%}")
        return historical_volatility

async def create_dict_HVolatiliti_options():
    global dict_histori_volatiliti
    tek_data = datetime.now().date()
    if dict_histori_volatiliti.get('data', False) == False:
        dict_histori_volatiliti['data'] = tek_data
        for i in series_options:
            close_price = await price_close_max300day(figi[i])
            v_30 , v_60, v_90, ev_vol = await histori_volaniliti(close_price)
            dict_histori_volatiliti[i] = {'30' : v_30, '60' : v_60, '90' : v_90, 'ev_vol' : ev_vol}
            await asyncio.sleep(1)
            print(dict_histori_volatiliti)
    else:
        if dict_histori_volatiliti.get('data', False) != tek_data:
            dict_histori_volatiliti['data'] = tek_data
            for i in series_options:
                close_price = await price_close_max300day(figi[i])
                v_30, v_60, v_90 = await histori_volaniliti(close_price)
                dict_histori_volatiliti[i] = {'30': v_30, '60': v_60, '90': v_90}
                await asyncio.sleep(1)
                print(dict_histori_volatiliti)

async def get_doska_optins(asset_code, optionseries_code):
    url = f'https://iss.moex.com/iss/apps/option-calc/v1/assets/{asset_code}/optionseries/{optionseries_code}/optionboard?asset_type=futures&rows=10'
    async with aiohttp.ClientSession() as session1:
        async with session1.get(url, headers=headers) as response2:
            respose = await response2.json()
            # Создаем дерево элементов из XML-данных
            return respose['call'][10]

async def create_dict_options():
    global dict_otions
    for i in series_options:
        for y in series_options[i]:
            time_apgrade = datetime.now(moscow_tz)
            time_new = time_apgrade.strftime("%H:%M:%S")
            call_20 = await get_doska_optins(i, y)
            call_20['time_new'] = time_new
            dict_otions[y] = call_20
            await asyncio.sleep(30)
            print(dict_otions)

async def format_date_00_00_0000(date : str):
    one = date[-8:-2]
    rez = one[:2] + '.' + one[2:4] + '.20' + one[-2:]
    return rez

def get_doska_jptinss(asset_code, optionseries_code):
    url = f'https://iss.moex.com/iss/apps/option-calc/v1/assets/{asset_code}/optionseries/{optionseries_code}/optionboard?asset_type=futures&rows=10'
    response = requests.get(url).json()

    print(response['call'][20])

async def upgrade_options_mesaage_telegramm(bot , client):
    time_apgrade = datetime.now(moscow_tz)
    time_new = time_apgrade.strftime("%H:%M:%S")
    # chenal_id = Token.chenal_id
    chenal_id = Token.chenal_id_signals
    # last_message = await bot.request()
    gr_unc = 31.1035
    last_message = await client.get_messages(chenal_id, limit=100)
    # print(last_message)
    last_messa_id = last_message[-6].id
    last_messa2_id = last_message[1].id
    last_messa3_id = last_message[-3].id
    last_messa4_id = last_message[3].id
    last_messa5_id = last_message[4].id
    si1_price = last_prices.get(Figi_future.si1_figi, 1)
    cr1_price = last_prices.get(Figi_future.cr1_figi, 1)
    eu1_price = last_prices.get(Figi_future.eu1_figi, 1)
    gold1_price = last_prices.get(Figi_future.gold1_figi, 1)
    rts1_price = last_prices.get(Figi_future.rts1_figi, 1)
    message_list = []
    if len(dict_otions) > 1:
        for i in series_options:
            for y in series_options[i]:
                evereng_volatiliti = dict_histori_volatiliti[i]['ev_vol']
                if dict_otions.get(y, False):
                    date_one = y[-8:-2]
                    volReal = dict_otions[y]['volatility']
                    strike = dict_otions[y]['strike']
                    spot = last_prices.get(figi[i], None)
                    deys_expir = await days_until_expiration(date_one)
                    # teor_price_put, teor_price_call = await black_scholes_price(spot, strike, deys_expir, 0.165 ,volReal / 100)
                    teor_price_put, teor_price_call = await theoretical_option_price(spot, strike, volReal / 100, deys_expir / 365)
                    time_neww = dict_otions[y]['time_new']
                    percent_volReal_volEver = round(volReal / evereng_volatiliti * 100 - 100 , 2 )
                    # percent_volReal_volEver = round(volReal - evereng_volatiliti , 2 )
                    fut_date = y[:-9]
                    format_date = await format_date_00_00_0000(y)
                    # percent = self.volatility / self.volatility * 100 - 100
                    # self.link = "https://t.me/cricket_scan"
                    message = f"{await optins_smail(percent_volReal_volEver)} • {await link_text(str(percent_volReal_volEver) + '%')} время обн.({time_neww})\n" \
                              f"IVOL / Средняя VOL\n" \
                              f"Опцион {await link_text(fut_date)} | {await link_text(format_date)}\n" \
                              f"Теорцена PUT - {teor_price_put}\n" \
                              f"Теорцена CALL - {teor_price_call}\n" \
                              f"IVOL • {volReal}% | strike - {strike}\n" \
                              f"🔅 Средняя VOL • {evereng_volatiliti}%\n" \
                              f"🔹 Истор. VOL  30 дн • {dict_histori_volatiliti[i]['30']}%\n" \
                              f"🔹 Истор. VOL  60 дн • {dict_histori_volatiliti[i]['60']}%\n" \
                              f"🔹 Истор. VOL  90 дн • {dict_histori_volatiliti[i]['90']}%\n\n"
                    # print(message)
                    message_list.append([message, abs(percent_volReal_volEver)])
    mesage_sorted = sorted(message_list, key=lambda x: x[1], reverse=True)
    text_mesage_sorted1 = ''.join([i[0] for i in mesage_sorted[:14]])
    text_mesage_sorted2 = ''.join([i[0] for i in mesage_sorted[14:]])
    zagolovok = f"🧭 Время последнего обновления:\n{time_apgrade.date()}  время: {time_new}\n\n"
    final_text_massage = zagolovok + text_mesage_sorted1
    r = await bot.edit_message_text(final_text_massage, chat_id=chenal_id, message_id=last_messa5_id, parse_mode='HTML',
                                disable_web_page_preview=True)
    final_text_massage2 = zagolovok + text_mesage_sorted2
    r = await bot.edit_message_text(final_text_massage2, chat_id=chenal_id, message_id=last_messa4_id,
                                        parse_mode='HTML',
                                        disable_web_page_preview=True)


    # print(r)
    # print(final_text_massage)
            # self.stroka2 = f'IVOL • {self.volatility} | 104500 '
            # self.stroka3 = f'Теор цена CALL - {self.price / 3}'
            # self.stroka4 = f'Теор цена PUT -{self.price / 2}'
            # self.stroka5 = f'🔻 Истор. VOL  90 дн •{self.volatility}'
            # self.stroka6 = f'🔻 Истор. VOL  60 дн •{self.volatility}'
            # self.stroka7 = f'🔻 Истор. VOL  30 дн •{self.volatility}'


