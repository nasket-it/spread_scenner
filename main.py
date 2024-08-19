import traceback
from clas_text import Text
import re
from all_function import webhook_discord
from funkction_future_akcii import dividend_data, arb_fut_akcii, parse_dividend
import math
from pars_dinamic_site import fetch_dividend_data
from yahoo_finance import  yahoo_valyata, dict_yahoo_valuta, time_diapazone, subbota_voskresen, get_fanding_moex, fanding
from telethon.sync import TelegramClient, events
from info_figi_ti import *
from secrete import Token, Flag, Chenal_id, WebhookDiscod
import asyncio
from tinkoff_get_func import ( future_all_info, akcii_moex_tiker, akcii_all_info, asy_price_float_ti,
    time_range, get_last_price, expiration_date_future,asy_get_percent, sprav_price_spread,
     last_prices, get_last_prices_dict, sprav_price_future,
    futures)
from Config import InfoTiker, Config, Chenal
from aiogram import Bot, Dispatcher, types, executor
from aiogram.utils.markdown import link
from datetime import *
import datetime
import pytz
import diskord
from diskord.ext import commands
# Создаем объект временной зоны для Москвы
moscow_tz = pytz.timezone('Europe/Moscow')

client2 = TelegramClient(Token.phone2, Token.api_id2, Token.api_hash2)
bot_discord = commands.Bot(command_prefix='/')
API_TOKEN = Token.bot_token


# Создаем объекты бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


account = ['-1001892817733','-1001857334624']
api_id = Token.api_id  # задаем API
api_hash = Token.api_hash  # задаем HASH
phone = Token.phone
client = TelegramClient(Token.phone, api_id, api_hash)
#<b>Жирный</b>
#<i>Курсив</i>
#<s>Зачеркнутый</s>
#<u>Подчеркнутый</u>
#<code>Копировать</code>
#<href='Сылка'>Курсив</a>


lotnost_forex = {'USDCNH' : 0.01, 'EURUSD' : 0.01, 'EURCNH' : 0.01,
                 'XAUUSD' : 0.01, 'XAGUSD' : 0.01, 'USDTRY' : 0.01,
                 'EURTRY' : 0.01, 'NDXUSD' : 0.1, 'SPXUSD' : 0.1,
                 'silver' : {'forex' : 0.01, 'moex' : 5},
                 'gold' : {'forex' : 0.01, 'moex' : 1},
                 'nasdaq' : {'forex' : 0.1, 'moex' : 100},
                 'sp500' : {'forex' : 0.1, 'moex' : 10}}




# await asyncio.sleep(5)

async def valyta_smail(percent):
    if percent < 0:
        return '📕'
    if percent > 0:
        return '📗'
    if percent == 0:
        return "📘"

async def smail_vnimanie(percent, delitel=0.1, znak='❗️', sma_stop=True):
    # Используем абсолютное значение процента для упрощения
    abs_percent = abs(percent)
    smail = znak
    smail_stop = '  🙅‍'
    # Округляем вверх, чтобы получить правильное количество символов '❗️'
    percent_namber = math.ceil(abs_percent // delitel)
    if percent_namber == 0 and sma_stop:
        return smail_stop
    elif percent_namber <= 6:
        return percent_namber * smail
    else:
        return 6 * smail + '+'

async def valuta_replace_float(valut_para, dict, kol_znakov):
    price = dict['valuta'][valut_para][0]
    proverka_na_tochku = '.' in price.split(',')[-1]
    if proverka_na_tochku:
        price = price.replace(',', '')
    else:
        price = price.replace('.', '').replace(',', '.')


    #price = dict['valuta'][valut_para][0].replace('.', '') if valut_para in ['gold_fut', 'gold_spot', 'XAUUSD', "nasdaq", "sp500"] else dict['valuta'][valut_para][0]
    # Удаляем запятые, используемые в качестве разделителей тысяч
    # price = dict['valuta'][valut_para][0].replace(',', '')

    return round(float(price), kol_znakov)

async def percent(num_100, num_rezultat):
    return round(num_100 / num_rezultat * 100 - 100, 2)


async def napravlenie_sdelok_3nogi(percent, svazka : str, price1 : float, price2 : float, price3 : float ,delitel=0.1 ):
    lot2 = round(price1 / price2, 1)
    list_tiker = svazka.split('/')
    abs_percent = abs(percent)
    percent_namber = math.ceil(abs_percent // delitel)
    if percent < 0 and percent_namber >= 1 :
        return f"Лонг {list_tiker[0].strip()}- 1 ({await link_text(price1)})\n" \
               f"Шорт {list_tiker[1].strip()}- {round(lot2 / 1000, 1) if list_tiker[1].strip() == 'CR1' or list_tiker[1].strip() == 'Cr1'  or list_tiker[1].strip() == 'CR2' or list_tiker[1].strip() == 'Cr2'  else lot2} ({await link_text(price2)})\n" \
               f"Шорт {list_tiker[2].strip()}- {0.01 if list_tiker[2].strip() != 'ED' else 1 } ({await link_text(price3)})\n\n"
    elif percent > 0 and percent_namber >= 1 :
        return f"Шорт {list_tiker[0].strip()}- 1 ({await link_text(price1)})\n" \
               f"Лонг {list_tiker[1].strip()}- {round(lot2 / 1000, 1) if list_tiker[1].strip() == 'CR1' or list_tiker[1].strip() == 'Cr1' or list_tiker[1].strip() == 'CR2' or list_tiker[1].strip() == 'Cr2' else lot2} ({await link_text(price2)})\n" \
               f"Лонг {list_tiker[2].strip()}- {0.01 if list_tiker[2].strip() != 'ED' else 1 } ({await link_text(price3)})\n\n"
    else:
        return f"Цена в пределах справедливой \n"\
               f"{list_tiker[0].strip()}- 1 ({await link_text(price1)})\n" \
               f"{list_tiker[1].strip()}- {round(lot2 / 1000, 1) if list_tiker[1].strip() == 'CR1' or list_tiker[1].strip() == 'Cr1' or list_tiker[1].strip() == 'CR2' or list_tiker[1].strip() == 'Cr2' else lot2} ({await link_text(price2)})\n" \
               f"{list_tiker[2].strip()}- {0.01 if list_tiker[2].strip() != 'ED' else 1 } ({await link_text(price3)})\n\n"



async def napravlenie_sdelok_2nogi(percent, svazka : str, price1 : float, price2 : float, lot1, lot2, delitel=0.1):
    list_tiker = svazka.split('/')
    abs_percent = abs(percent)
    percent_namber = math.ceil(abs_percent // delitel)
    if percent < 0 and percent_namber >= 1 :
        return f"Лонг {list_tiker[0].strip()} - {lot1} ({await link_text(price2)})\n" \
               f"Шорт {list_tiker[1].strip()} - {lot2} ({await link_text(price1)})\n\n"
    elif percent > 0 and percent_namber >= 1 :
        return f"Шорт {list_tiker[0].strip()} - {lot1} ({await link_text(price2)})\n" \
               f"Лонг {list_tiker[1].strip()} - {lot2} ({await link_text(price1)})\n\n"
    else:
        return f"Цена в пределах справедливой \n"\
               f"{list_tiker[0].strip()} - {lot1} ({await link_text(price2)})\n" \
               f"{list_tiker[1].strip()} - {lot2} ({await link_text(price1)})\n\n"
# <i>Курсив</i>
# <s>Зачеркнутый</s>
# <u>Подчеркнутый</u>
# <code>Копировать</code>
# <href='Сылка'>Курсив</a>
#<tg-spoiler>Скрытый</tg-spoiler>


async def link_text(text, link="https://t.me/spread_sca"):
    return f'<a href="{link}">{text}</a>'

async def podcher_text(text, link="https://t.me/spread_sca"):
    return f'<u>{text}</u>'

async def zirniy_text(text, link="https://t.me/spread_sca"):
    return f'<b>{text}</b>'


async def citate_text(text):
    return f'<blockquote>{text}</blockquote>'


async def arbitrage_parniy_futures(tiker1, tiker2, price_percent=True, perenos_stroki=1, name=list):
    tiker1_last_price = await get_last_price(tiker1)
    tiker2_last_price = await get_last_price(tiker2)
    perenos = "\n" * perenos_stroki
    if tiker1_last_price and tiker2_last_price:
        if price_percent:
            rubli = round(tiker1_last_price - tiker2_last_price, 1)
            punkti = int(rubli / 1)
            punkti = punkti if punkti > 0 else punkti * -1
            if name and len(name) == 2:
                return f"🔸-fut ${name[0]}({tiker1_last_price}) / ${name[1]}({tiker2_last_price})\n        {punkti}п | {rubli}p | {await percent(tiker1_last_price, tiker2_last_price)}%{perenos}"
            else:
                return f"🔸-fut ${tiker1}({tiker1_last_price}) / ${tiker2}( {tiker2_last_price})\n        {punkti}п | {rubli}p | {await percent(tiker1_last_price, tiker2_last_price)}%{perenos}"
        else:
            if name and len(name) == 2:
                return f"{tiker1_last_price} • ${name[0]}  ({await percent(tiker1_last_price, tiker2_last_price)}%)  ${name[1]} • {tiker2_last_price}{perenos}"

            else:
                return f"{tiker1_last_price} • ${tiker1}  ({await percent(tiker1_last_price, tiker2_last_price)}%)  ${tiker2} • {tiker2_last_price}{perenos}"


async def arbitrage_parniy_akcii(tiker1, tiker2, price_percent=True, perenos_stroki=1):
    tiker1_last_price = last_prices.get(Info_figi.tiker_figi[tiker1])
    tiker2_last_price = last_prices.get(Info_figi.tiker_figi[tiker2])
    perenos = "\n" * perenos_stroki

    if tiker1_last_price and tiker2_last_price:
        if price_percent:
            rubli = round(tiker1_last_price - tiker2_last_price, 2)
            punkti = round(rubli / Config.info[tiker1]['minstep'])
            punkti = punkti if punkti > 0 else punkti * -1
            percents = await percent(tiker1_last_price, tiker2_last_price)
            text = f"{tiker1} / {tiker2}"
            return f"{await valyta_smail(percents)} • {await link_text(text)}{await smail_vnimanie(percents)}\n{punkti}п | {rubli}р | {percents}%\n" \
                   f"{await napravlenie_sdelok_2nogi(percents, text, price1=tiker1_last_price, price2=tiker2_last_price, lot1=1, lot2=1)}\n"



async def arbtrage_future_akcii(kvartal, future_akcii=False, percent=0.5):
    time_apgrade = datetime.datetime.now(moscow_tz)
    time_new = time_apgrade.strftime("%H:%M:%S")
    chenal_id = Token.chenal_id
    # last_message = await bot.request()
    gr_unc = 31.1035
    last_message = await client2.get_messages(chenal_id, limit=5)
    last_messa_id = last_message[0].id
    last_messa2_id = last_message[1].id
    last_messa3_id = last_message[2].id
    last_messa4_id = last_message[3].id
    last_messa5_id = last_message[4].id
    message = []
    for i in future_all_info:
        # print(future_all_info[i]) if future_all_info[i].basic_asset == 'ABIO' else None
        # print([[future_all_info[i].basic_asset , last_prices[i], last_prices[akcii_moex_tiker[future_all_info[i].basic_asset]] * akcii_all_info[akcii_moex_tiker[future_all_info[i].basic_asset]].lot, await asy_get_percent(last_prices[i], last_prices[akcii_moex_tiker[future_all_info[i].basic_asset]]), await sprav_price_future(last_prices[akcii_moex_tiker[future_all_info[i].basic_asset]], figi=i, future_akcii=future_akcii)] for i in future_all_info if future_all_info[i].expiration_date.date().month == kvartal and  future_all_info[i].expiration_date.date().year == 2024 and future_all_info[i].basic_asset in akcii_moex_tiker])
        if (future_all_info[i].basic_asset in akcii_moex_tiker) and  (future_all_info[i].expiration_date.date().month == kvartal) and (future_all_info[i].expiration_date.date().year == 2024 ):
            # print(f"Функция арбитраж проверка 2")
            tiker = future_all_info[i].basic_asset
            figi_akcii = akcii_moex_tiker[tiker]
            lot_akcii = akcii_all_info[figi_akcii].lot
            price_akc = last_prices.get(figi_akcii, None) #if dividend_data.get(tiker, 0) == 0 else last_prices.get(figi_akcii, None) + dividend_data[tiker].get('dividend_rub', 0)
            # print(tiker , price_akc, last_prices.get(figi_akcii, None))
            if last_prices.get(i, None) != None and last_prices.get(i, None) > 0 and price_akc != None and price_akc > 0:
                lots = math.floor(future_all_info[i].basic_asset_size.units)
                price_fut = last_prices.get(i, None)
                spread_real = price_akc / (price_fut / lots) * 100
                spread_sprav = await sprav_price_spread(price_akc, spread_real, figi=i, divid_rub=dividend_data[tiker].get('dividend_rub', 0) if dividend_data.get(tiker, 0) != 0 else 0)
                # print(f"{tiker} - {spread_sprav} real {spread_real}")
                sprav_price_fut = await sprav_price_future(price_akc, figi=i, future_akcii=future_akcii, divid_rub=dividend_data[tiker].get('dividend_rub', 0) if dividend_data.get(tiker, 0) != 0 else 0)
                # print(f"{tiker} price fut  - {price_fut} , price akcii {price_akc} , sprav price - {sprav_price_fut}")
                percent_fut_ot_sprav_price = await asy_get_percent(spread_real, spread_sprav)
                name_future = f"{future_all_info[i].basic_asset if future_all_info[i].basic_asset != 'ABIO' else 'ISKJ'}-{kvartal}-{future_all_info[i].expiration_date.date().year % 100}"
                if tiker in dividend_data:
                    if percent_fut_ot_sprav_price >= percent or percent_fut_ot_sprav_price <= -percent:

                        percen_dohodn = round(dividend_data[tiker].get('dividend_rub', 0) / (price_akc / 100), 2)
                        rez = f"{await valyta_smail(percent_fut_ot_sprav_price)} • ({percent_fut_ot_sprav_price}%) {await link_text(tiker)}\n" \
                              f"{dividend_data[tiker]['dividend_rub']}р.{'👌' if dividend_data[tiker]['odobrenie_div'] else '⁉️'} • {percen_dohodn}% • {dividend_data[tiker]['date_close']}{'👌' if dividend_data[tiker]['odobrenie_reestr'] else '⁉️'}\n" \
                              f"{await napravlenie_sdelok_2nogi(percent_fut_ot_sprav_price,  f'{tiker} / {name_future}', price_fut, price_akc,  1, int(lots / lot_akcii))}\n"#\nPrice(справ) - {sprav_price_fut}\nPrice(реал) - {price_fut}
                              # f"Див.(прогноз) - {dividend_data[tiker]['dividend_rub']}р.\nЗакр. реес.(ожидание)- {dividend_data[tiker]['date_close']}\nИндекс стаб. выпл. див - {dividend_data[tiker]['dsi']}\n"#\nPrice(справ) - {sprav_price_fut}\nPrice(реал) - {price_fut}

                        message.append([rez, abs(percent_fut_ot_sprav_price)])
                else:
                    if percent_fut_ot_sprav_price >= percent or percent_fut_ot_sprav_price <= -percent:
                        rez = f"{await valyta_smail(percent_fut_ot_sprav_price)} • ({percent_fut_ot_sprav_price}%) {await link_text(tiker)}\n" \
                              f"{await napravlenie_sdelok_2nogi(percent_fut_ot_sprav_price,  f'{tiker} / {name_future}', price_fut, price_akc,  1, int(lots / lot_akcii))}\n"#\nPrice(справ) - {sprav_price_fut}\nPrice(реал) - {price_fut}

                        message.append([rez, abs(percent_fut_ot_sprav_price)])
    mesage_sorted = sorted(message, key=lambda x: x[1], reverse=True)
    # return '\n'.join(message_)
    text_mesage_sorted  = ''.join([i[0] for i in mesage_sorted]) + '\n' if len(mesage_sorted) <= 25 else ''.join([i[0] for i in mesage_sorted[:25]]) + '\n'
    zagolovok = f"🧭 Время последнего обновления:\n{time_apgrade.date()}  время: {time_new}\n\n⚙️ {await podcher_text('Сканер спредовых расхождений')}\nSPREAD(реал) / SPREAD(справ)\n\n" \
                f"Ставка ЦБ используется - 18%\nДиапазон отк-я цены:  (- 0.5%) - (+0.5%)\n⁉️ - прогноз \n👌 - рекомендован сов.дир \n\n"
    finale_message = zagolovok + '\n' +  text_mesage_sorted
    print(f"dlina zagolovka {len(zagolovok)} - text {len(mesage_sorted) } ")
    s1 = await bot.edit_message_text(finale_message, chat_id=chenal_id, message_id=last_messa_id, parse_mode='HTML')




dict_interva = {}
async def send_signals(percent, message, svyazka):
    abs_percent = abs(percent)
    print(abs_percent ,  svyazka)
    if 0 <= abs_percent < 0.03:
        if svyazka not in dict_interva:
            await bot.send_message(Token.chenal_id_signals, message)
            dict_interva[svyazka] = {0.0: 1}
        elif svyazka in dict_interva and dict_interva[svyazka].get(0.0, False) == False:
            await bot.send_message(Token.chenal_id_signals, message)
            dict_interva[svyazka] = {0.0: 1}
    elif 0.07 < abs_percent <= 0.1:
        if svyazka not in dict_interva:
            await bot.send_message(Token.chenal_id_signals, message)
            dict_interva[svyazka] = {0.1: 1}
        elif svyazka in dict_interva and dict_interva[svyazka].get(0.1, False) == False:
            await bot.send_message(Token.chenal_id_signals, message)
            dict_interva[svyazka] = {0.1: 1}
    elif 0.17 < abs_percent <= 0.2:
        if svyazka not in dict_interva:
            await bot.send_message(Token.chenal_id_signals, message)
            dict_interva[svyazka] = {0.2: 1}
        elif svyazka in dict_interva and dict_interva[svyazka].get(0.2, False) == False:
            await bot.send_message(Token.chenal_id_signals, message)
            dict_interva[svyazka] = {0.2: 1}
    elif 0.27 < abs_percent <= 0.3:
        if svyazka not in dict_interva:
            await bot.send_message(Token.chenal_id_signals, message)
            dict_interva[svyazka] = {0.3: 1}
        elif svyazka in dict_interva and 0.3 not in dict_interva[svyazka]:
            await bot.send_message(Token.chenal_id_signals, message)
            dict_interva[svyazka] = {0.3: 1}
        elif svyazka in dict_interva and 0.3 in dict_interva[svyazka]:
            if dict_interva[svyazka][0.3] < 180:
                dict_interva[svyazka][0.3] += 1
            else:
                await bot.send_message(Token.chenal_id_signals, message)
                dict_interva[svyazka] = {0.3: 1}
    elif 0.37 < abs_percent <= 0.4:
        if svyazka not in dict_interva:
            await bot.send_message(Token.chenal_id_signals, message)
            dict_interva[svyazka] = {0.4: 1}
        elif svyazka in dict_interva and 0.4 not in dict_interva[svyazka]:
            await bot.send_message(Token.chenal_id_signals, message)
            dict_interva[svyazka] = {0.4: 1}
        elif svyazka in dict_interva and 0.4 in dict_interva[svyazka]:
            if dict_interva[svyazka][0.4] < 120:
                dict_interva[svyazka][0.4] += 1
            else:
                await bot.send_message(Token.chenal_id_signals, message)
                dict_interva[svyazka] = {0.4: 1}
    # elif abs_percent < 0.1 and svyazka in dict_interva:
    #     await bot.send_message(Token.chenal_id_signals, message)
    #     del dict_interva[svyazka]


async def create_tex_sprav_price_future(percent, svyazka, svazkka_moex_forex=None, delitel=0.1):
    if svazkka_moex_forex == None:
        text =  [f"{await valyta_smail(percent)} •  ({percent}%){await smail_vnimanie(percent, delitel=delitel, sma_stop=False)}\n",
        f"{await link_text(svyazka)}\n"]
        return ''.join(text)
    else:
        text = [f"{await valyta_smail(percent)} •  ({percent}%){await smail_vnimanie(percent, delitel=delitel, sma_stop=False)}\n",
                f"{await link_text(svyazka)}\n", ]
        return ''.join(text)


#link_name = '<a href="https://t.me/spread_sca">Eu1 / Cr1 / EURCNH(for)</a>'


async def valuta_vtelegram():
    global yahoo_valyata
    current_time = datetime.datetime.now(moscow_tz).time()
    time_10x23_50 = await time_range('09:50:00', '23:50:00', current_time)

    # chenal_id = {'Сверчок': -1001854614186}
    chenal_id = Token.chenal_id
    # last_message = await bot.request()
    gr_unc = 31.1035
    last_message = await client2.get_messages(chenal_id, limit=5)
    last_messa_id = last_message[0].id
    last_messa2_id = last_message[1].id
    last_messa3_id = last_message[2].id
    last_messa4_id = last_message[3].id
    last_messa5_id = last_message[4].id
    # print(bool(yahoo_valyata['valuta']))
    try:
        if yahoo_valyata.get('valuta', False):
            usdrub = {'USD000UTSTOM': 'BBG0013HGFT4'}
            cnyrub = {'CNYRUB_TOM': 'BBG0013HRTL0'}
            si = {'si-6.24' : 'FUTSI0624000'}
            gas_fures = {'NGH4' : 'FUTNG0424000'}
            gold_futures = {'GDH4' : 'FUTGOLD03240'}
            brent_futures = {'BRJ4' : 'FUTBR0424000'}
            silver_futures = {'SVH4' : 'FUTSILV03240'}
            usdcnh_for = await valuta_replace_float('USDCNH', yahoo_valyata, 4)
            eurrub_megbank = await valuta_replace_float('EURRUB', yahoo_valyata, 4)
            usdrub_megbank = await valuta_replace_float('USDRUB', yahoo_valyata, 4)
            usdkzt_for = await valuta_replace_float("USDKZT", yahoo_valyata, 4 )
            eurkzt_for = await valuta_replace_float("EURKZT", yahoo_valyata, 4 )
            usdtry_for = await valuta_replace_float("USDTRY", yahoo_valyata, 4)
            eurtry_for = await valuta_replace_float("EURTRY", yahoo_valyata, 4)
            eurcnh_for = await valuta_replace_float("EURCNH", yahoo_valyata, 4)
            eurusd_for = await valuta_replace_float("EURUSD", yahoo_valyata, 4)
            silver_in = await valuta_replace_float("XAGUSD", yahoo_valyata, 4)
            gold_in = await valuta_replace_float("XAUUSD", yahoo_valyata, 4)
            nasdaq_in = await valuta_replace_float("nasdaq", yahoo_valyata, 4)
            sp500_in = await valuta_replace_float("sp500", yahoo_valyata, 4)
            price_gold_gr_usd = round(gold_in / gr_unc, 2)

            kurs_usdrub_spr = round(last_prices.get('BBG0013HRTL0', 1) * usdcnh_for, 4)
            kurs_eurrub_spr = round(last_prices.get('BBG0013HRTL0', 1) * eurcnh_for, 4)

            kurs_cb_usdrub = 87.0354
            kurs_cb_eurrub = 93.2994
            kurs_cb_cnyrub = 11.7964


            kurs_usdrub_spr = round(last_prices.get('BBG0013HRTL0', 1) * usdcnh_for, 4)
            kurs_eurrub_spr = round(last_prices.get('BBG0013HRTL0', 1) * eurcnh_for, 4)

            print(sp500_in)

            # print(f"forex {usdcnh_for}")
            # print('eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
            # usd_rub_ru = await get_last_price(usdrub['USD000UTSTOM'])
            # eur_rub_tom = last_prices.get('EUR000UTSTOM')
            # print('ldldldldldldldldldldldldlldldldld', eur_rub_tom)
            si_price = last_prices.get('FUTSI0924000', 1)
            # si_sprav_price = round(1000 * (usd_rub_ru * (1 + 0.16 * (await expiration_date_future(si['si-6.24'])/365))))


            percent_si2_cr2_usdcnh = round(last_prices.get('FUTSI1224000', 1) / last_prices.get('FUTCNY122400', 1) / 1000 / usdcnh_for * 100 -100, 3)

            percent_si_cr_ucny = round(si_price / last_prices.get('FUTCNY092400', 1) / 1000 / last_prices.get('FUTUCNY09240', 1) * 100 -100, 3)#usdcnh_for

            percent_si_cr_usdcnh = round(si_price / last_prices.get('FUTCNY092400', 1) / 1000 / usdcnh_for * 100 -100, 3)#usdcnh_for
            si_cr_usdcnh = 'Si1_Cr1_USDCNH(for)'
            # message_si_cr_usdcnh = f"{await valyta_smail(percent_si_cr_usdcnh)} •  ({percent_si_cr_usdcnh}%){await smail_vnimanie(percent_si_cr_usdcnh)}\nSi1 / CR1 / $USDCNH(for)\nSi - 1 лот | CNY - {si_price/100/last_prices.get('FUTCNY092400', 1)}лот\n\n"
            # await send_signals(percent_si_cr_usdcnh, message_si_cr_usdcnh, si_cr_usdcnh)

            percent_eu2_cr2_eurcnh = round(last_prices.get('FUTEU1224000', 1) / last_prices.get('FUTCNY122400', 1) / 1000 / await valuta_replace_float('EURCNH', yahoo_valyata, 4) * 100 -100, 3)

            percent_eu_cr_eurcnh = round(last_prices.get('FUTEU0924000', 1) / last_prices.get('FUTCNY092400', 1) / 1000 / await valuta_replace_float('EURCNH', yahoo_valyata, 4) * 100 -100, 3) # await valuta_replace_float('EURCNH', yahoo_valyata, 4)
            eu_cr_eurcnh = 'Eu1_Cr1_EURCNH(for)'
            # message_eu_cr_eurcnh = f"{await valyta_smail(percent_eu_cr_eurcnh)} •  ({percent_eu_cr_eurcnh}%){await smail_vnimanie(percent_eu_cr_eurcnh)}\nEu1 / CR1 / $EURCNH(for)\n\n"
            # await send_signals(percent_eu_cr_eurcnh, message_eu_cr_eurcnh, eu_cr_eurcnh)

            percent_eu2_si2_eurusd = round(last_prices.get('FUTEU1224000', 1) / last_prices.get('FUTSI1224000', 1)/ await valuta_replace_float('EURUSD', yahoo_valyata, 4) * 100 -100, 3)

            percent_eu_si_eurusd = round(last_prices.get('FUTEU0924000', 1) / si_price / await valuta_replace_float('EURUSD', yahoo_valyata, 4) * 100 -100, 3)
            # eu_si_eurusd = 'Eu1_Si1_EURUSD(for)'
            # message_eu_si_eurusd = f"{await valyta_smail(percent_eu_si_eurusd)} •  ({percent_eu_si_eurusd}%){await smail_vnimanie(percent_eu_si_eurusd)}\nEu1 / Si1 / $EURUSD(for)\n\n"
            # await send_signals(percent_eu_si_eurusd, message_eu_si_eurusd, eu_si_eurusd)

            percent_eu2_si2_ed2 = round(last_prices.get('FUTEU1224000', 1) / last_prices.get('FUTSI1224000', 1) / last_prices.get('FUTED1224000', 1) * 100 -100, 3)

            percent_eu_si_ed = round(last_prices.get('FUTEU0924000', 1) / si_price / last_prices.get('FUTED0924000', 1) * 100 -100, 3)
            print()

            # eu_si_ed = 'Eu1_Si1_Ed1'
            # message_eu_si_ed = f"{await valyta_smail(percent_eu_si_ed)} •  ({percent_eu_si_ed}%){await smail_vnimanie(percent_eu_si_ed)}\nEu1 / Si1 / $ED ️\n\n\n"
            # await send_signals(percent_eu_si_ed, message_eu_si_ed, eu_si_ed)

            percent_usf_cnf_ucny = round(last_prices.get(futures['USDRUBF'], 1) / last_prices.get(futures['CNYRUBF'], 1) / last_prices.get('FUTUCNY09240', 1) * 100 -100, 3)

            percent_usf_cnf_usdcnh = round(last_prices.get(futures['USDRUBF'], 1) / last_prices.get(futures['CNYRUBF'], 1) / usdcnh_for * 100 -100, 3)
            # usf_cnf_usdcnh = 'US.F_CN.F_USDCNH(for)'
            # message_usf_cnf_usdcnh = f"{await valyta_smail(percent_usf_cnf_usdcnh)} •  ({percent_usf_cnf_usdcnh}%){await smail_vnimanie(percent_usf_cnf_usdcnh)}\nUS.F / CN.F / USDCNH(for) ️\n\n\n"
            # await send_signals(percent_usf_cnf_usdcnh, message_usf_cnf_usdcnh, usf_cnf_usdcnh)

            percent_euf_cnf_eurcnh = round(last_prices.get('FUTEURRUBF00', 1) / last_prices.get(futures['CNYRUBF'], 1) / eurcnh_for * 100 -100, 3)
            # euf_cnf_eurcnh = 'EU.F_CN.F_EURCNH(for)'
            # message_euf_cnf_eurcnh = f"{await valyta_smail(percent_euf_cnf_eurcnh)} •  ({percent_euf_cnf_eurcnh}%){await smail_vnimanie(percent_euf_cnf_eurcnh)}\nUS.F / CN.F / USDCNH(for) ️\n\n\n"
            # await send_signals(percent_euf_cnf_eurcnh, message_euf_cnf_eurcnh, euf_cnf_eurcnh)

            percent_euf_usf_eurusd = round(last_prices.get('FUTEURRUBF00', 1) / last_prices.get(futures['USDRUBF'], 1) / eurusd_for * 100 -100, 3)

            percent_ed_eurusd = round(last_prices.get('FUTED0924000', 1) / await valuta_replace_float('EURUSD', yahoo_valyata, 4) * 100 - 100, 3)
            percent_ucny_usdcnh = round(last_prices.get('FUTUCNY09240', 1) / usdcnh_for * 100 - 100, 3)
            percent_ed2_eurusd = round(last_prices.get('FUTED1224000', 1) / await valuta_replace_float('EURUSD', yahoo_valyata, 4) * 100 - 100, 3)
            percent_ed_ed2 = round(last_prices.get('FUTED0924000', 1) / last_prices.get('FUTED1224000', 1) * 100 - 100, 3)
            percent_si_si2 = round(last_prices.get('FUTSI0924000', 1) / last_prices.get('FUTSI1224000', 1) * 100 - 100, 3)
            percent_eu_eu2 = round(last_prices.get('FUTEU0924000', 1) / last_prices.get('FUTEU1224000', 1) * 100 - 100, 3)
            percent_cr_cr2 = round(last_prices.get('FUTCNY092400', 1) / last_prices.get('FUTCNY122400', 1) * 100 - 100, 3)
            percent_usf_si = round(last_prices.get(futures['USDRUBF'], 1) / (last_prices.get('FUTSI0924000', 1) / 1000) * 100 - 100, 3)
            percent_euf_eu = round(last_prices.get('FUTEURRUBF00', 1) / (last_prices.get('FUTEU0924000', 1) / 1000)* 100 - 100, 3)
            percent_crf_cr = round(last_prices.get(futures['CNYRUBF'], 1) / last_prices.get('FUTCNY092400', 1) * 100 - 100, 3)
            percent_cr1_cr_tom = round(last_prices.get('FUTCNY092400', 1) / last_prices.get('BBG0013HRTL0', 1) * 100 - 100, 3)
            percent_cr2_cr_tom = round(last_prices.get('FUTCNY122400', 1) / last_prices.get('BBG0013HRTL0', 1) * 100 - 100, 3)




            percent_us_tom_cn_tom_usdcnh = round(last_prices.get('BBG0013HGFT4', 1) / last_prices.get('BBG0013HRTL0', 1)/ usdcnh_for * 100 -100, 3)
            percent_eu_tom_cn_tom_eurcnh = round(eurrub_megbank / last_prices.get('BBG0013HRTL0', 1)/ await valuta_replace_float('EURCNH', yahoo_valyata, 4) * 100 -100, 3)
            percent_us_tom_kz_tom_usdkzt = round(last_prices.get('BBG0013HGFT4', 1) / last_prices.get('BBG0013HG026', 4)/ usdkzt_for * 100 * 100 -100, 3)
            percent_eu_tom_kz_tom_eurkzt = round(eurrub_megbank / last_prices.get('BBG0013HG026', 4)/ eurkzt_for * 100 * 100 -100, 3)
            percent_us_tom_try_tom_usdtry = round(last_prices.get('BBG0013HGFT4', 1) / last_prices.get('BBG0013J12N1', 4)/ usdtry_for * 100 -100, 3)
            percent_eu_tom_try_tom_eurtry = round(eurrub_megbank / last_prices.get('BBG0013J12N1', 4)/ eurtry_for * 100  -100, 3)
            percent_eu_tom_us_tom_eurusd = round(eurrub_megbank / last_prices.get('BBG0013HGFT4', 1) / eurusd_for * 100 -100, 3)
            percent_usdrub_megb_spr = round(usdrub_megbank / kurs_usdrub_spr * 100 - 100 , 2)
            percent_eurrub_megb_spr = round(eurrub_megbank / kurs_eurrub_spr * 100 - 100 , 2)
            percent_si1_usdrub_megb = round(last_prices.get('FUTSI0924000', 1) / 1000 / usdrub_megbank * 100 - 100 , 2)
            percent_eu1_eurrub_megb = round(last_prices.get('FUTEU0924000', 1) / 1000 / eurrub_megbank * 100 - 100 , 2)
            percent_euf_eurrub_megb = round(last_prices.get('FUTEURRUBF00', 1)  / eurrub_megbank * 100 - 100 , 2)
            percent_usf_usdrub_megb = round(last_prices.get(futures['USDRUBF'], 1)  / usdrub_megbank * 100 - 100 , 2)
            print('ioioioiooioiio', usdrub_megbank, eurrub_megbank)
            kurs_cb_usdrub = 89.0499
            kurs_cb_eurrub = 95.3906



            percent_glf_gd1_si = round((last_prices.get('FUTGLDRUBF00', 1 ) * 31.1035) / last_prices.get('FUTGOLD09240',None) / (last_prices.get('FUTSI0924000', 1) / 1000) * 100 - 100 , 3)


            percent_sv1_silver = round(last_prices.get('FUTSILV09240',None) / silver_in * 100  -100, 3)
            percent_gd1_gold = round(last_prices.get('FUTGOLD09240',None) / gold_in * 100  -100, 3)
            percent_na1_nasdaq = round(last_prices.get('FUTNASD09240',None) / nasdaq_in * 100  -100, 3)
            percent_sf1_sp500 = round((last_prices.get('FUTSPYF09240',None) * 10) / sp500_in * 100  -100, 3)
            percent_sv2_silver = round(last_prices.get('FUTSILV12240',None) / silver_in * 100  -100, 3)
            percent_gd2_gold = round(last_prices.get('FUTGOLD12240',None) / gold_in * 100  -100, 3)
            percent_na2_nasdaq = round(last_prices.get('FUTNASD12240',None) / nasdaq_in * 100  -100, 3)
            percent_sf2_sp500 = round((last_prices.get('FUTSPYF12240',None) * 10) / sp500_in * 100  -100, 3)



            sprav_price_cr1 = await sprav_price_future(last_prices.get('BBG0013HRTL0', 1), figi='FUTCNY092400', max_percente_first_day=2.7)
            percent_sprav_price_cr1 = round(last_prices.get('FUTCNY092400', 1) / sprav_price_cr1 * 100 -100, 3)

            sprav_price_silver = await sprav_price_future(silver_in, figi='FUTSILV09240', max_percente_first_day=3.25)
            percent_sprav_price_silver = await asy_get_percent(sprav_price_silver, last_prices.get('FUTSILV09240', None) )

            sprav_price_gold = await sprav_price_future(gold_in, figi='FUTGOLD09240', max_percente_first_day=2.7)
            percent_sprav_price_gold = await asy_get_percent(sprav_price_gold, last_prices.get('FUTGOLD09240',None))
            # percent_sprav_price_gold =round(percent_sprav_price_gold -  1.3 if percent_sprav_price_gold >= 0 else percent_sprav_price_gold - -1.3, 3)

            sprav_price_nasdaq = await sprav_price_future(nasdaq_in, figi='FUTNASD09240', max_percente_first_day=1.7)
            percent_sprav_price_nasdaq = await asy_get_percent(sprav_price_nasdaq, last_prices.get('FUTNASD09240',None))

            sprav_price_sp500 = await sprav_price_future(sp500_in, figi='FUTSPYF09240', max_percente_first_day=1.9)
            percent_sprav_price_sp500 = await asy_get_percent(sprav_price_sp500, last_prices.get('FUTSPYF09240',None) * 10 )



            text_fandung_zagolovok = f"💰 {await podcher_text(await zirniy_text('Фандинг(тест❗ )'))}\nЗадержка 15м \nОбновление каждые 60с \nЧасы работы с 10:15 до 18:50, в нерабочие часы последнее значение или None\n"
            text_fanding = [f"USDRUBF - {await link_text(fanding.get('USDRUBF', None))}\n",
                            f"EURRUBF - {await link_text(fanding.get('EURRUBF', None))}\n",
                            f"CNYRUBF - {await link_text(fanding.get('CNYRUBF', None))}\n",
                            f"GLDRUBF - {await link_text(fanding.get('GLDRUBF', None))}\n",
                            f"IMOEXF - {await link_text(fanding.get('IMOEXF', None))}\n\n"]

            link_name = '<a href="https://t.me/spread_sca">Eu1 / Cr1 / EURCNH(for)</a>'
            delitel1 = 0.1
            time_apgrade = datetime.datetime.now(moscow_tz)
            time_new = time_apgrade.strftime("%H:%M:%S")
            text_future_zagolovok = f"⚙️ {await podcher_text(await zirniy_text('Фьючерсы на валюту'))} 👇👇👇\n\n"

            text_future_kotirovri = [[f"{await valyta_smail(percent_si_cr_ucny)} •  ({percent_si_cr_ucny}%){await smail_vnimanie(percent_si_cr_ucny)}\n{await link_text('Si1 / CR1 / UCNY')}\n" +
                                    await napravlenie_sdelok_3nogi(percent_si_cr_ucny, 'Si1 / CR1 / UCNY', price1=si_price, price2=last_prices.get('FUTCNY092400', 1), price3=last_prices.get('FUTUCNY09240', 1)) , abs(percent_si_cr_ucny)],
                                    [f"{await valyta_smail(percent_si_cr_usdcnh)} •  ({percent_si_cr_usdcnh}%){await smail_vnimanie(percent_si_cr_usdcnh)}\n{await link_text('Si1 / CR1 / USDCNH(for)')}\n" +
                                    await napravlenie_sdelok_3nogi(percent_si_cr_usdcnh, 'Si1 / CR1 / USDCNH(for)', price1=si_price, price2=last_prices.get('FUTCNY092400', 1), price3=usdcnh_for) , abs(percent_si_cr_usdcnh)],
                                    [f"{await valyta_smail(percent_si2_cr2_usdcnh)} •  ({percent_si2_cr2_usdcnh}%){await smail_vnimanie(percent_si2_cr2_usdcnh)}\n{await link_text('Si2 / CR2 / USDCNH(for)')}\n" +
                                    await napravlenie_sdelok_3nogi(percent_si2_cr2_usdcnh, 'Si2 / CR2 / USDCNH(for)', price1=last_prices.get('FUTSI1224000', 1), price2=last_prices.get('FUTCNY122400', 1), price3=usdcnh_for) , abs(percent_si2_cr2_usdcnh)],
                                    [f"{await valyta_smail(percent_eu_cr_eurcnh)} •  ({percent_eu_cr_eurcnh}%){await smail_vnimanie(percent_eu_cr_eurcnh)}\n{await link_text('Eu1 / Cr1 / EURCNH(for)')}\n" +
                                    await napravlenie_sdelok_3nogi(percent_eu_cr_eurcnh, 'Eu1 / Cr1 / EURCNH(for)', price1=last_prices.get('FUTEU0924000', 1), price2=last_prices.get('FUTCNY092400', 1), price3=eurcnh_for), abs(percent_eu_cr_eurcnh)],
                                    [f"{await valyta_smail(percent_eu2_cr2_eurcnh)} •  ({percent_eu2_cr2_eurcnh}%){await smail_vnimanie(percent_eu2_cr2_eurcnh)}\n{await link_text('Eu2 / Cr2 / EURCNH(for)')}\n" +
                                    await napravlenie_sdelok_3nogi(percent_eu2_cr2_eurcnh, 'Eu2 / Cr2 / EURCNH(for)', price1=last_prices.get('FUTEU1224000', 1), price2=last_prices.get('FUTCNY122400', 1), price3=eurcnh_for), abs(percent_eu2_cr2_eurcnh)],
                                    [f"{await valyta_smail(percent_eu_si_eurusd)} •  ({percent_eu_si_eurusd}%){await smail_vnimanie(percent_eu_si_eurusd)}\n{await link_text('Eu1 / Si1 / EURUSD(for)')}\n" +
                                    await napravlenie_sdelok_3nogi(percent_eu_si_eurusd, 'Eu1 / Si1 / EURUSD(for)', price1=last_prices.get('FUTEU0924000', 1), price2=si_price, price3=eurusd_for), abs(percent_eu_si_eurusd)],
                                    [f"{await valyta_smail(percent_eu2_si2_eurusd)} •  ({percent_eu2_si2_eurusd}%){await smail_vnimanie(percent_eu2_si2_eurusd)}\n{await link_text('Eu2 / Si2 / EURUSD(for)')}\n" +
                                    await napravlenie_sdelok_3nogi(percent_eu2_si2_eurusd, 'Eu2 / Si2 / EURUSD(for)', price1=last_prices.get('FUTEU1224000', 1), price2=last_prices.get('FUTSI1224000', 1), price3=eurusd_for), abs(percent_eu2_si2_eurusd)],
                                    [f"{await valyta_smail(percent_eu_si_ed)} •  ({percent_eu_si_ed}%){await smail_vnimanie(percent_eu_si_ed)}\n{await link_text('Eu1 / Si1 / ED')}\n" +
                                    await napravlenie_sdelok_3nogi(percent_eu_si_ed, 'Eu1 / Si1 / ED',  price1=last_prices.get('FUTEU0924000', 1), price2=si_price, price3=last_prices.get('FUTED0924000', 1) ), abs(percent_eu_si_ed)],
                                    [f"{await valyta_smail(percent_eu2_si2_ed2)} •  ({percent_eu2_si2_ed2}%){await smail_vnimanie(percent_eu2_si2_ed2)}\n{await link_text('Eu2 / Si2 / ED2')}\n" +
                                    await napravlenie_sdelok_3nogi(percent_eu2_si2_ed2, 'Eu2 / Si2 / ED2',  price1=last_prices.get('FUTEU1224000', 1), price2=last_prices.get('FUTSI1224000', 1), price3=last_prices.get('FUTED1224000', 1) ), abs(percent_eu2_si2_ed2)],
                                    [f"{await valyta_smail(percent_usf_cnf_usdcnh)} •  ({percent_usf_cnf_usdcnh}%){await smail_vnimanie(percent_usf_cnf_usdcnh)}\n{await link_text('US.F / CN.F / USDCNH(for)')}\n" +
                                    await napravlenie_sdelok_3nogi(percent_usf_cnf_usdcnh, 'US.F / CN.F / USDCNH(for)', price1=last_prices.get(futures['USDRUBF'], 1), price2=last_prices.get(futures['CNYRUBF'], 1), price3=usdcnh_for), abs(percent_usf_cnf_usdcnh)],
                                    [f"{await valyta_smail(percent_usf_cnf_ucny)} •  ({percent_usf_cnf_ucny}%){await smail_vnimanie(percent_usf_cnf_ucny)}\n{await link_text('US.F / CN.F / UCNY')}\n" +
                                    await napravlenie_sdelok_3nogi(percent_usf_cnf_ucny, 'US.F / CN.F / UCNY', price1=last_prices.get(futures['USDRUBF'], 1), price2=last_prices.get(futures['CNYRUBF'], 1), price3=last_prices.get('FUTUCNY09240', 1)), abs(percent_usf_cnf_ucny)],
                                    [f"{await valyta_smail(percent_euf_cnf_eurcnh)} •  ({percent_euf_cnf_eurcnh}%){await smail_vnimanie(percent_euf_cnf_eurcnh)}\n{await link_text('EU.F / CN.F / EURCNH(for)')}\n" +
                                    await napravlenie_sdelok_3nogi(percent_euf_cnf_eurcnh, 'EU.F / CN.F / EURCNH(for)', price1=last_prices.get('FUTEURRUBF00', 1), price2=last_prices.get(futures['CNYRUBF'], 1), price3=eurcnh_for), abs(percent_euf_cnf_eurcnh)],
                                    [f"{await valyta_smail(percent_euf_usf_eurusd)} •  ({percent_euf_usf_eurusd}%){await smail_vnimanie(percent_euf_usf_eurusd)}\n{await link_text('EU.F / US.F / EURUSD(for)')}\n" +
                                    await napravlenie_sdelok_3nogi(percent_euf_usf_eurusd, 'EU.F / US.F / EURUSD(for)', price1=last_prices.get('FUTEURRUBF00', 1), price2=last_prices.get(futures['USDRUBF'], 1), price3=eurusd_for), abs(percent_euf_usf_eurusd)],
                                    [f"{await valyta_smail(percent_ed_eurusd)} •  ({percent_ed_eurusd}%){await smail_vnimanie(percent_ed_eurusd)}\n{await link_text('ED / EURUSD(for)')}\n" +
                                    await napravlenie_sdelok_2nogi(percent_ed_eurusd, 'ED / EURUSD(for)', price1=last_prices.get('FUTED0924000', 1), price2=eurusd_for, lot1=1, lot2=lotnost_forex['EURUSD']), abs(percent_ed_eurusd)],
                                    [f"{await valyta_smail(percent_ed2_eurusd)} •  ({percent_ed2_eurusd}%){await smail_vnimanie(percent_ed2_eurusd)}\n{await link_text('ED2 / EURUSD(for)')}\n" +
                                    await napravlenie_sdelok_2nogi(percent_ed2_eurusd, 'ED2 / EURUSD(for)', price1=last_prices.get('FUTED1224000', 1), price2=eurusd_for, lot1=1, lot2=lotnost_forex['EURUSD']), abs(percent_ed2_eurusd)],

                                     ]

            text_future_kotirovri2 = [[f"{await valyta_smail(percent_si_si2)} •  ({percent_si_si2}%)\n{await link_text('SI1 / SI2')}\n" +
                                    await napravlenie_sdelok_2nogi(percent_si_si2, 'SI1 / SI2', price1=last_prices.get('FUTSI0924000', 1), price2=last_prices.get('FUTSI1224000', 1), lot1=1, lot2=1), abs(percent_si_si2)],
                                    [f"{await valyta_smail(percent_eu_eu2)} •  ({percent_eu_eu2}%)\n{await link_text('EU1 / EU2')}\n" +
                                    await napravlenie_sdelok_2nogi(percent_eu_eu2, 'EU1 / EU2', price1=last_prices.get('FUTEU0924000', 1), price2=last_prices.get('FUTEU1224000', 1), lot1=1, lot2=1), abs(percent_eu_eu2)],
                                    [f"{await valyta_smail(percent_cr_cr2)} •  ({percent_cr_cr2}%)\n{await link_text('CR1 / CR2')}\n" +
                                    await napravlenie_sdelok_2nogi(percent_cr_cr2, 'CR1 / CR2', price1=last_prices.get('FUTCNY092400', 1), price2=last_prices.get('FUTCNY122400', 1), lot1=1, lot2=1), abs(percent_cr_cr2)],
                                    [f"{await valyta_smail(percent_usf_si)} •  ({percent_usf_si}%)\n{await link_text('US.F / SI1')}\n" +
                                    await napravlenie_sdelok_2nogi(percent_usf_si, 'US.F / SI1', price1=last_prices.get(futures['USDRUBF'], 1), price2=last_prices.get('FUTSI0924000', 1), lot1=1, lot2=1), abs(percent_usf_si)],
                                    [f"{await valyta_smail(percent_euf_eu)} •  ({percent_euf_eu}%)\n{await link_text('EU.F / EU1')}\n" +
                                    await napravlenie_sdelok_2nogi(percent_euf_eu, 'EU.F / EU1', price1=last_prices.get('FUTEURRUBF00', 1), price2=last_prices.get('FUTEU0924000', 1), lot1=1, lot2=1), abs(percent_euf_eu)],
                                    [f"{await valyta_smail(percent_crf_cr)} •  ({percent_crf_cr}%)\n{await link_text('CR.F / CR1')}\n" +
                                    await napravlenie_sdelok_2nogi(percent_crf_cr, 'CR.F / CR1', price1=last_prices.get(futures['CNYRUBF'], 1), price2=last_prices.get('FUTCNY092400', 1), lot1=1, lot2=1), abs(percent_crf_cr)],
                                    [f"{await valyta_smail(percent_cr1_cr_tom)} •  ({percent_cr1_cr_tom}%)\n{await link_text('CR1 / CR_TOM')}\n" +
                                    await napravlenie_sdelok_2nogi(percent_cr1_cr_tom, 'CR1 / CR_TOM', price1=last_prices.get('FUTCNY092400', 1), price2=last_prices.get('BBG0013HRTL0', 1), lot1=1, lot2=1), abs(percent_cr1_cr_tom)],
                                    [f"{await valyta_smail(percent_cr2_cr_tom)} •  ({percent_cr2_cr_tom}%)\n{await link_text('CR2 / CR_TOM')}\n" +
                                    await napravlenie_sdelok_2nogi(percent_cr2_cr_tom, 'CR2 / CR_TOM', price1=last_prices.get('FUTCNY122400', 1), price2=last_prices.get('BBG0013HRTL0', 1), lot1=1, lot2=1), abs(percent_cr2_cr_tom)],
                                    [f"{await valyta_smail(percent_ed_ed2)} •  ({percent_ed_ed2}%)\n{await link_text('ED / ED2')}\n" +
                                    await napravlenie_sdelok_2nogi(percent_ed_ed2, 'ED / ED2', price1=last_prices.get('FUTED0924000', 1), price2=last_prices.get('FUTED1224000', 1), lot1=1, lot2=1), abs(percent_ed_ed2)],

                                     ]

            text_fur_spot = [f"{await valyta_smail(percent_sprav_price_cr1)} •  ({percent_sprav_price_cr1}%){await smail_vnimanie(percent_sprav_price_cr1)}\n" ,
                             f"{await link_text('CR1 (спр) / CR1 (real)')}\n" ,
                             f"CR1 (спр) -> цена справ-вая = {sprav_price_cr1}\n\n\n"]
            delitel2 = 0.1
            text_valuta_zagolovok = [f"🧭 Время последнего обновления:\n{time_apgrade.date()}  время: {time_new}\n\n" ,
                   f"Один знак  '❗' =  {delitel2}%\n\n",
                   f"⚙️ {await zirniy_text(await podcher_text('Валюта'))}👇👇👇\n⚠️ Источник курса -межбанк- тестируется\n\n"]
            # text_valuta_kotirovki =[ [f"{await valyta_smail(percent_us_tom_cn_tom_usdcnh)} •  ({percent_us_tom_cn_tom_usdcnh}%){await smail_vnimanie(percent_us_tom_cn_tom_usdcnh)}\n{await link_text('US_TOM / CN_TOM / SDCNH(for)')}\n" +
            #        await napravlenie_sdelok_3nogi(percent_us_tom_cn_tom_usdcnh, 'US_TOM / CN_TOM / USDCNH(for)', price1=last_prices.get('BBG0013HGFT4', 1),  price2=last_prices.get('BBG0013HRTL0', 1), price3=usdcnh_for), abs(percent_us_tom_cn_tom_usdcnh)],
            #        [f"{await valyta_smail(percent_eu_tom_cn_tom_eurcnh)} •  ({percent_eu_tom_cn_tom_eurcnh}%){await smail_vnimanie(percent_eu_tom_cn_tom_eurcnh)}\n{await link_text('EU_TOM / CN_TOM / EURCNH(for)')}\n" +
            #        await napravlenie_sdelok_3nogi(percent_eu_tom_cn_tom_eurcnh, 'EU_TOM / CN_TOM / EURCNH(for)', price1=eurrub_megbank,  price2=last_prices.get('BBG0013HRTL0', 1), price3=eurcnh_for),abs(percent_eu_tom_cn_tom_eurcnh)],
            #        [f"{await valyta_smail(percent_us_tom_kz_tom_usdkzt)} •  ({percent_us_tom_kz_tom_usdkzt}%){await smail_vnimanie(percent_us_tom_kz_tom_usdkzt)}\n{await link_text('US_TOM / KZ_TOM / USDKZT(for)')}\n" +
            #        await napravlenie_sdelok_3nogi(percent_us_tom_kz_tom_usdkzt, 'US_TOM / KZ_TOM / USDKZT(for)', price1=last_prices.get('BBG0013HGFT4', 1) , price2=last_prices.get('BBG0013HG026', 4), price3=usdkzt_for), abs(percent_us_tom_kz_tom_usdkzt)],
            #        [f"{await valyta_smail(percent_eu_tom_kz_tom_eurkzt)} •  ({percent_eu_tom_kz_tom_eurkzt}%){await smail_vnimanie(percent_eu_tom_kz_tom_eurkzt)}\n{await link_text('EU_TOM / KZ_TOM / EURKZT(for)')}\n" +
            #        await napravlenie_sdelok_3nogi(percent_eu_tom_kz_tom_eurkzt, 'EU_TOM / KZ_TOM / EURKZT(for)', price1=eurrub_megbank,  price2=last_prices.get('BBG0013HG026', 4), price3=eurkzt_for), abs(percent_eu_tom_kz_tom_eurkzt)],
            #        [f"{await valyta_smail(percent_us_tom_try_tom_usdtry)} •  ({percent_us_tom_try_tom_usdtry}%){await smail_vnimanie(percent_us_tom_try_tom_usdtry)}\n{await link_text('US_TOM / TRY_TOM / USDTRY(for)')}\n" +
            #        await napravlenie_sdelok_3nogi(percent_us_tom_try_tom_usdtry, 'US_TOM / TRY_TOM / USDTRY(for)', price1=last_prices.get('BBG0013HGFT4', 1), price2=last_prices.get('BBG0013J12N1', 4), price3=usdtry_for), abs(percent_us_tom_try_tom_usdtry)],
            #        [f"{await valyta_smail(percent_eu_tom_try_tom_eurtry)} •  ({percent_eu_tom_try_tom_eurtry}%){await smail_vnimanie(percent_eu_tom_try_tom_eurtry)}\n{await link_text('EU_TOM / TRY_TOM / EURTRY(for)')}\n" +
            #        await napravlenie_sdelok_3nogi(percent_eu_tom_try_tom_eurtry, 'EU_TOM / TRY_TOM / EURTRY(for)', price1=eurrub_megbank, price2=last_prices.get('BBG0013J12N1', 4), price3=eurtry_for) , abs(percent_eu_tom_try_tom_eurtry) ],
            #        [f"{await valyta_smail(percent_eu_tom_us_tom_eurusd)} •  ({percent_eu_tom_us_tom_eurusd}%){await smail_vnimanie(percent_eu_tom_us_tom_eurusd)}\n{await link_text('EU_TOM / US_TOM / EURUSD(for)')}\n" +
            #        await napravlenie_sdelok_3nogi(percent_eu_tom_us_tom_eurusd, 'EU_TOM / US_TOM / EURUSD(for)', price1=eurrub_megbank, price2=last_prices.get('BBG0013HGFT4', 1), price3=eurusd_for) , abs(percent_eu_tom_us_tom_eurusd) ]
            #        ]
            text_valuta_kotirovki = [[f"{await valyta_smail(percent_usdrub_megb_spr)} •  ({percent_usdrub_megb_spr}%)\n{await link_text('USDRUB(межб) / USDRUB(спр)')}\nCNY_TOM x USDCNH(for) • {kurs_usdrub_spr}\nКурс {await link_text('USDRUB межбанк')} • {usdrub_megbank}\n\n", abs(percent_usdrub_megb_spr)],
                                     [f"{await valyta_smail(percent_eurrub_megb_spr)} •  ({percent_eurrub_megb_spr}%)\n{await link_text('EURRUB(межб) / EURRUB(спр)')}\nCNY_TOM x EURCNH(for) • {kurs_eurrub_spr}\nКурс {await link_text('EURRUB межбанк')} • {eurrub_megbank}\n\n", abs(percent_eurrub_megb_spr)],
                                     [f"\n{await valyta_smail(percent_si1_usdrub_megb)} •  ({percent_si1_usdrub_megb}%)\n{await link_text('SI1 / USDRUB(межб)')}\nSI1  • {last_prices.get('FUTSI0924000', 1)}\nUSDRUB({await link_text('межбанк')}) • {usdrub_megbank}\n\n", 0],
                                     [f"{await valyta_smail(percent_usf_usdrub_megb)} •  ({percent_usf_usdrub_megb}%)\n{await link_text('USDRUBF / USDRUB(межб)')}\nUSF  • {last_prices.get(futures['USDRUBF'], 1)}\nUSDRUB({await link_text('межбанк')}) • {usdrub_megbank}\n\n", 0],
                                     [f"{await valyta_smail(percent_eu1_eurrub_megb)} •  ({percent_eu1_eurrub_megb}%)\n{await link_text('EU1 / EURRUB(межб)')}\nEU1 • {last_prices.get('FUTEU0924000', 1)}\nEURRUB({await link_text('межбанк')}) • {eurrub_megbank}\n\n", 0],
                                     [f"{await valyta_smail(percent_euf_eurrub_megb)} •  ({percent_euf_eurrub_megb}%)\n{await link_text('EURRUBF / EURRUB(межб)')}\nEU1 • {last_prices.get('FUTEURRUBF00', 1)}\nEURRUB({await link_text('межбанк')}) • {eurrub_megbank}\n\n", 0],
                                     [f"{await valyta_smail(percent_glf_gd1_si)} •  ({percent_glf_gd1_si}%)\n🔒 {await link_text('***P** / *1* / *I1**')}\n\n", 0],

                                     ]


                   # f"Акции\n"

            time_apgrade1 = datetime.datetime.now(moscow_tz)
            time_new1 = time_apgrade.strftime("%H:%M:%S")
            delitel = 0.5
            silver_text = await create_tex_sprav_price_future(percent_sv1_silver, 'SV1 / XAGUSD(for)', delitel=0.5)
            silver_text += await napravlenie_sdelok_2nogi(percent_sv1_silver, 'SV1 / XAGUSD(for)', price1=last_prices.get('FUTSILV09240', None), price2=silver_in, lot1=lotnost_forex['silver']['moex'], lot2=lotnost_forex['silver']['forex'])
            gold_text = await create_tex_sprav_price_future(percent_gd1_gold, 'GOLD1 / XAUUSD(for)', delitel=0.5)
            gold_text += await napravlenie_sdelok_2nogi(percent_gd1_gold, 'GOLD1 / XAUUSD(for)', price1=last_prices.get('FUTGOLD09240',None), price2=gold_in, lot1=lotnost_forex['gold']['moex'], lot2=lotnost_forex['gold']['forex'])
            nasdaq_text = await create_tex_sprav_price_future(percent_na1_nasdaq, 'NA1 / NDXUSD(for)', delitel=0.5)
            nasdaq_text += await napravlenie_sdelok_2nogi(percent_na1_nasdaq, 'NA1 / NDXUSD(for)', price1=last_prices.get('FUTNASD09240',None), price2=nasdaq_in, lot1=lotnost_forex['nasdaq']['moex'], lot2=lotnost_forex['nasdaq']['forex'])
            sp500_text = await create_tex_sprav_price_future(percent_sf1_sp500, 'SF1 / SPXUSD(for)', delitel=0.5)
            sp500_text += await napravlenie_sdelok_2nogi(percent_sf1_sp500, 'SF1 / SPXUSD(for)', price1=last_prices.get('FUTSPYF09240',None) , price2=sp500_in, lot1=lotnost_forex['sp500']['moex'], lot2=lotnost_forex['sp500']['forex'])
            text_index_metals_zagolovok = [f"🧭 Время последнего обновления:\n{time_apgrade.date()}  время: {time_new1}\n\n",
                         f"Один знак  '❗' =  {delitel}%\n\n", f"⚙️ {await zirniy_text(await podcher_text('Фьючерсы на металлы, индексы '))}\n\n",]
            text_index_metals_kotirovki = [[silver_text, abs(percent_sv1_silver)],  [gold_text, abs(percent_gd1_gold)], [nasdaq_text, abs(percent_na1_nasdaq)], [sp500_text, abs(percent_sf1_sp500)]]
            text_index_metals_zagolovok_string = ''.join(text_index_metals_zagolovok)
            text_index_metals_kotirovki_sorted = sorted(text_index_metals_kotirovki, key=lambda x: x[1] , reverse=True)
            text_index_metals_kotirovki_string = ''.join([i[0] for i in text_index_metals_kotirovki_sorted]) + '\n\n'
            finali_message = text_index_metals_zagolovok_string + text_index_metals_kotirovki_string #+ await arbtrage_future_akcii(9, future_akcii=True)

            # print(f"Функция арбитраж проверка {await arbtrage_future_akcii(9)}")

            fut_sb = {"SRM4" : "FUTSBRF06240"}
            fut_sbp = {"SPM4" : "FUTSBPR06240"}
            name = ['SBRF', 'SBPR']
            if time_10x23_50:
                time_new2 = time_apgrade.strftime("%H:%M:%S")
                delitel = 0.1
                tatn_tex = await arbitrage_parniy_akcii('TATN', 'TATNP')
                sber_text = await arbitrage_parniy_akcii('SBER', 'SBERP')
                zagolovok_akcii = 'Акции(торговля на выходных в Тиньков)' if await subbota_voskresen() else 'Акции'
                list_akcii = [f"\n⚙️ {await zirniy_text(await podcher_text(zagolovok_akcii))}\n\n",
                              tatn_tex, sber_text]
                finali_message_akcii = ''.join(list_akcii)
                finali_message = finali_message + finali_message_akcii

            # if time_10x23_50:
            #     text = text + await arbitrage_parniy_futures(fut_sb["SRM4"], fut_sbp["SPM4"], name=name)
            #     text = text + '\n' + await arbtrage_future_akcii()
            text_fur_sorted = sorted(text_future_kotirovri, key=lambda x: x[1] , reverse=True)
            text_fur2_sorted = sorted(text_future_kotirovri2, key=lambda x: x[1] , reverse=True)
            text_future_string  = ''.join(text_future_zagolovok) + ''.join([i[0] for i in text_fur_sorted]) +  text_fandung_zagolovok + ''.join(text_fanding) + ''.join([i[0] for i in text_fur2_sorted]) + '\n\n'
            text_valuta_sorted = sorted(text_valuta_kotirovki, key=lambda x: x[1] , reverse=True)
            text_valuta_string =  ''.join(text_valuta_zagolovok) + ''.join([i[0] for i in text_valuta_sorted] ) + '\n\n'
            # text_valuta_string =  ''.join(text_valuta_zagolovok) + 'В разработке ... 👨‍💻' + '\n\n\n'

            finali_message2 = text_valuta_string + text_future_string # ''.join( text_fur_spot)
            # <b>Жирный</b>
            # <i>Курсив</i>
            # <s>Зачеркнутый</s>
            # <u>Подчеркнутый</u>
            # <code>Копировать</code>
            # <href='Сылка'>Курсив</a>
            #<tg-spoiler>Скрытый</tg-spoiler>
            # s = await bot.edit_message_text(finali_message1, chat_id=chenal_id, message_id=last_messa3_id, parse_mode='HTML')
            s1 = await bot.edit_message_text(finali_message2, chat_id=chenal_id, message_id=last_messa3_id, parse_mode='HTML')
            s2 = await bot.edit_message_text(finali_message, chat_id=chenal_id, message_id=last_messa2_id, parse_mode='HTML')

    except Exception as e:
        error_message = traceback.format_exc()
        print(f'Произошла ошибка функции valuta_vtelegram:\n{error_message}')
        print(e)


url_moex = "https://www.moex.com/ru/contract.aspx?code=GLDRUBF"

async def update_message1_2():
    await valuta_vtelegram()
    await asyncio.sleep(5)


async def update_message3_4():
    await arbtrage_future_akcii(9, future_akcii=True)
    await asyncio.sleep(5)
    await get_last_prices_dict()







async def start_cicl_5s():
    coun = 0
    try:
        while True:
            await update_message1_2()
            await update_message3_4()
            # await asyncio.sleep(5)
            # await valuta_vtelegram()
            # await asyncio.sleep(5)
            # await arbtrage_future_akcii(9, future_akcii=True)
            # await get_last_prices_dict()

            print(dict_interva)
            # await parse_site(url_moex)
    except Exception as e:
        error_message = traceback.format_exc()
        print(f'Произошла ошибка функции valuta_vtelegram:\n{error_message}')
        print(e)
        await asyncio.sleep(5)
        await start_cicl_5s()

async def start_cicl_15m():
    coun = 0
    try:
        while True:
            current_time = datetime.datetime.now(moscow_tz).time()
            time_10_15_18_50 = await time_range('10:15:00', '18:50:00', current_time)
            if time_10_15_18_50:
                await get_fanding_moex()
            print(fanding)
            await asyncio.sleep(60)

    except Exception as e:
        error_message = traceback.format_exc()
        print(f'Произошла ошибка функции start_cicl_15m :\n{error_message}')
        print(e)
        await asyncio.sleep(5)
        await start_cicl_15m()

async def start_cicl_60m():
    coun = 0
    try:
        while True:
            current_time = datetime.datetime.now(moscow_tz).time()
            diapazone  = await time_range('07:00:00', '23:50:00', current_time)
            if coun == 0  :
                print(f"count 1 ")
                await parse_dividend()
                await asyncio.sleep(60)
                coun += 1
            elif coun == 1 and diapazone == False:
                print(f"count 2 ")
                await parse_dividend()
                await asyncio.sleep(4000)
            else:
                print(f"count 3 ")
                await parse_dividend()
                await asyncio.sleep(3600)
            print(dividend_data)
    except Exception as e:
        error_message = traceback.format_exc()
        print(f'Произошла ошибка функции start_cicl_60m :\n{error_message}')
        print(e)

        await asyncio.sleep(5)
        coun = 0
        await start_cicl_60m()


async def start_get_last_prices_dict():
    x = 0
    try:
        while True:
            print(565656565, last_prices.get('BBG0013HGFT4'))
            print(f"cxtnxbr = {x}")
            vihodnie = await subbota_voskresen()
            if  x < 5:
                await asyncio.sleep(5)
                await get_last_prices_dict()
                x += 1
                print(111111111111111)
            elif (vihodnie and x == 5) and  (await time_diapazone('23:59', '06:00') == False)  and x == 5:
                await get_last_prices_dict()
                await asyncio.sleep(60)
                print(222222222222222)
            elif await time_diapazone('23:59', '06:00') and x == 5:
                await get_last_prices_dict()
                await asyncio.sleep(1800)
            else:
                await get_last_prices_dict()
                await asyncio.sleep(5)
                print(3333333333333333)
            print(0000000000000)


    except Exception as e:
            error_message = traceback.format_exc()
            print(f'Произошла ошибка функции valuta_vtelegram:\n{error_message}')
            print(e)
            await asyncio.sleep(5)
            await start_get_last_prices_dict()




list_task = [start_cicl_5s(), dict_yahoo_valuta(), start_get_last_prices_dict(), start_cicl_15m(), start_cicl_60m()]#bot_discord.start(Token.discordBot_WarrenWallet)

async def main():
    # Запуск периодических задач в фоновом режиме
    await asyncio.gather(*list_task)

    # Запуск бота
    await dp.start_polling()

p = ['KZOSP', 'TATNP', 'NKHP', 'BANEP', 'MRKP', 'TRNFP', 'SNGSP', 'KAZTP', 'TGKBP',
     'KRKNP', 'NKNCP', 'RTKMP', 'FIXP', 'MGTSP', 'PMSBP', 'GAZP', 'SBERP', 'LNZLP', 'RASP',
     'LSNGP', 'NMTP', 'CNTLP', 'MTLRP', '📅', '🔮', '📁', '🛩', '#отчётность',  '#мсфо' , '#банки',
     '#консенсус',  '#металлурги' , '⭐', '#календарь', '#никель', '#цбрф', 'PN Alert', '#рсбу', '#дивиденды',
     '📏', '💼', '— PN', '📘', '#банки' , '#авиа', '❗', '💳', 'Bloomberg ✅', '-[статья]', '[статья]']


fast_id  = [-1001750058000,]
url_jont_news_moex = 'https://discordapp.com/api/webhooks/1262849198882164766/WACqtXgL9TAgLu-I2kZCiWj_sNy8ZWTGLlOGQkbm6B29a-18m9Ef95oSUr43ajYXtUI4'
webhook_BST2_server_news = 'https://discord.com/api/webhooks/1263747088697528360/oEVrj6anDzx0Qzw_qmcUHCFZENhpzFdEY-O4iyc_O-I4GatGie-vq_EP62b3nVEP61VE'
@client.on(events.NewMessage(chats=[Chenal_id.istochnik_news1, Chenal_id.istochnik_news2]))#chats=Config.fast_id + Chenal.all_chenal_list_client + Config.news_vip_id    #chats=[news.get('ALL NEWS MOEX | Priority News') + news.get('Королёвский | вестник')]
async def hendler(event):
    id_chennal = event.message.chat_id
    text = Text(event.message.message)
    blumberg_chek_list = ['🇨🇳', '🇷🇺', '⚔️', '🛢']
    if (Chenal_id.istochnik_news2 == id_chennal and text.check_words_in_text(blumberg_chek_list)) or (id_chennal == Chenal_id.istochnik_news1):
        if len(text.strip()) >= 20:
            print(text)
            text = text.replace_all(['$', '@prioritynews_bot', 'Alert'])
            # text = text.replace('$', '').replace('@prioritynews_bot', '').replace('Alert', '')
            text_list = text.split('\n')
            text = ' '.join([i for i in text.split() if  i.strip()])
            tiker = text_list[0] if len(text_list) > 1 else ''
            text = Text(text.replace(tiker, ''))
            text = text.replace_all(p)
            text = text.replace_all(akcii_moex_tiker)
            # for i in p:
            #     text = text.replace(i, '')
            # for i in akcii_moex_tiker:
            #     text = text.replace(i, '')
            text = text.strip()
            text_discord = tiker +'\n' + text if len(text_list) > 1 else text
            text_telegram = '🔹🔻🔸\n\n' + tiker +'\n' + text if len(text_list) > 1 else '🔹🔻🔸\n\n' + text
            text_discord = f"{text_discord}\n\n▫️ The Trading Times"
            text_telegram = f"{text_telegram}\n\n🅾️ The Trading Times"
            if Flag.vikluchatel_webhook:
                await webhook_discord(WebhookDiscod.webhook2, text_discord)
                await webhook_discord(WebhookDiscod.webhook1, text)
            if Flag.knoka_send_post:
                await bot.send_message(Chenal_id.trading_times_id, text_telegram)
        # dialogs = await client.get_dialogs()
        # for i in dialogs:
        #     if i.name == 'Bloomberg':
        #         print(f"'Bloomberg' - {i.entity.id}")










if __name__ == '__main__':
    client.start()
    client2.start()
    # bot_discord.start(Token.discordBot_WarrenWallet)
    # bot_discord.run(Token.discordBot_WarrenWallet)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

# if __name__ == '__main__':
#     # loop = asyncio.get_event_loop()
#     # loop.run_until_complete(main())
#     # main()
#     # Запуск клиента Telethon
#     client.start()
#     client2.start()
#     # Запуск бота aiogram
#     executor.start_polling(dp)
#     # loop = asyncio.get_event_loop()
#     # loop.run_until_complete(main())

# cny_rub_ru = await get_last_price(cnyrub['CNYRUB_TOM'])
            # silver = await get_last_price(silver_futures['SVH4'])
            # percent_silver = round(await valuta_replace_float('silver_fut', yahoo_valyata, 3) / silver * 100 - 100, 2)
            # gas = await get_last_price(gas_fures['NGH4'])
            # percent_gas = round(await valuta_replace_float('gas_fut', yahoo_valyata, 3) / gas * 100 - 100, 2)
            # gold = await get_last_price(gold_futures['GDH4'])
            # gold_sprav_price_fut = gold * (1 + 0.16 * (await expiration_date_future(gold_futures['GDH4'])/365))
            # percent_gold = round(gold_sprav_price_fut / gold * 100 - 100, 2)
            # brent = await get_last_price(brent_futures['BRJ4'])
            # percent_brent = round(await valuta_replace_float('brent_fut', yahoo_valyata, 4) / brent * 100 - 100, 2)
            # percent_usd_rub = round(await valuta_replace_float('USDRUB', yahoo_valyata, 4) / usd_rub_ru * 100 - 100, 2)
            # smail_usd_rub = await valyta_smail(percent_usd_rub)
            # percent_cny_rub = round(await valuta_replace_float('CNYRUB', yahoo_valyata, 2) / cny_rub_ru * 100 - 100, 2)
            # smail_cny_rub = await valyta_smail(percent_cny_rub)
            # sprav_price_cnyrub = round(usd_rub_ru * await valuta_replace_float('CNYUSD', yahoo_valyata, 4), 4)