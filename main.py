import time
import random
from file_zamena_kvartal import Figi_future , Kvartal
import test
from parse_options import create_dict_options, create_dict_HVolatiliti_options, upgrade_options_mesaage_telegramm
import traceback
from clas_text import Text
import re
from parse_kase import parse_price_curent_kase, kase_curen_dict, new_text_kase_current, kase_curen_dict
from all_function import webhook_discord, dowload_photo_adn_send, translate_text, fetch_messages, dict_sobitiy
from dohod_parse_dividend import dividend_data, arb_fut_akcii, parse_dividend
import math
from pars_dinamic_site import fetch_dividend_data
from yahoo_finance import  yahoo_valyata, dict_yahoo_valuta, time_diapazone, subbota_voskresen, get_fanding_moex, fanding
from telethon.sync import TelegramClient, events
from info_figi_ti import *
from secrete import Token, Flag, Chenal_id, WebhookDiscod, URL_rss
import asyncio
from tinkoff_get_func import ( future_all_info, akcii_moex_tiker, akcii_all_info, asy_price_float_ti,
    time_range, get_last_price, expiration_date_future,asy_get_percent, sprav_price_spread,
     last_prices, get_last_prices_dict, sprav_price_future,
    futures)
from Config import InfoTiker, Config, Chenal
from aiogram import Bot, Dispatcher, types, executor
from aiogram.utils.markdown import link
from datetime import datetime
import datetime
import pytz
import diskord
from rss_parser import check_rss
from news_site_parse import parse_komersant, parse_rbk
from diskord.ext import commands
from send_logsErrors import sendErorsTelegram

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

# async def valuta_replace_float(valut_para, dict, kol_znakov):
#     print(f'Словарь dict - {dict}')
#     price = dict['valuta'][valut_para][0]
#     proverka_na_tochku = '.' in price.split(',')[-1]
#     proverka_na_tochku2 = '.' in price
#     if proverka_na_tochku2 == False:
#         price = price.replace(',', '.')
#     elif proverka_na_tochku:
#         price = price.replace(',', '')
#     else:
#         price = price.replace('.', '').replace(',', '.')
#     return round(float(price), kol_znakov)

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

async def napravlenie_sdelok_2nogi(percent, svazka : str, price1 : float, price2 : float, lot1, lot2, delitel=0.1, ukazat_napravlenie_sdelok=True):
    list_tiker = svazka.split('/')
    abs_percent = abs(percent)
    percent_namber = math.ceil(abs_percent // delitel)
    if ukazat_napravlenie_sdelok:
        if percent < 0 and percent_namber >= 1 :
            return f"Лонг {list_tiker[0].strip()} - {lot1} ({await link_text(price1)})\n" \
                   f"Шорт {list_tiker[1].strip()} - {lot2} ({await link_text(price2)})\n\n"
        elif percent > 0 and percent_namber >= 1 :
            return f"Шорт {list_tiker[0].strip()} - {lot1} ({await link_text(price1)})\n" \
                   f"Лонг {list_tiker[1].strip()} - {lot2} ({await link_text(price2)})\n\n"
        else:
            return f"Цена {list_tiker[0].strip()} - {lot1} ({await link_text(price1)})\n" \
                   f"Цена {list_tiker[1].strip()} - {lot2} ({await link_text(price2)})\n\n"
    else:
        return f"Цена {list_tiker[0].strip()} - {lot1} ({await link_text(price1)})\n" \
               f"Цена {list_tiker[1].strip()} - {lot2} ({await link_text(price2)})\n\n"

# <i>Курсив</i>
# <s>Зачеркнутый</s>
# <u>Подчеркнутый</u>
# <code>Копировать</code>
# <href='Сылка'>Курсив</a>
#<tg-spoiler>Скрытый</tg-spoiler>


async def link_text(text, link="https://t.me/cricket_scan"):
    return f'<a href="{link}">{text}</a>'

def link_text_sinh(text, link="https://t.me/cricket_scan"):
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
    last_message = await client2.get_messages(chenal_id, limit=100)
    # print(last_message)
    last_messa_id = last_message[-6].id
    last_messa2_id = last_message[1].id
    last_messa3_id = last_message[-3].id
    last_messa4_id = last_message[3].id
    last_messa5_id = last_message[4].id
    # print(last_message[-1])
    if Flag.vikluchatel_future_akcii:
        message = []
        # print("dividend", dividend_data)
        # print(future_all_info)future_all_info[i].basic_asset
        for i in future_all_info:
            # print(akcii_moex_tiker)print(akcii_moex_tiker)
            # print(future_all_info[i]) if future_all_info[i].basic_asset == 'ABIO' else None
            # print([[future_all_info[i].basic_asset , last_prices[i], last_prices[akcii_moex_tiker[future_all_info[i].basic_asset]] * akcii_all_info[akcii_moex_tiker[future_all_info[i].basic_asset]].lot, await asy_get_percent(last_prices[i], last_prices[akcii_moex_tiker[future_all_info[i].basic_asset]]), await sprav_price_future(last_prices[akcii_moex_tiker[future_all_info[i].basic_asset]], figi=i, future_akcii=future_akcii)] for i in future_all_info if future_all_info[i].expiration_date.date().month == kvartal and  future_all_info[i].expiration_date.date().year == 2024 and future_all_info[i].basic_asset in akcii_moex_tiker])
            if (future_all_info[i].basic_asset in akcii_moex_tiker) and  (future_all_info[i].expiration_date.date().month == kvartal) and (future_all_info[i].expiration_date.date().year == 2025 ):
                # print(future_all_info[i].expiration_date.date().month, future_all_info[i].expiration_date.date().year)
                tiker = future_all_info[i].basic_asset
                figi_akcii = akcii_moex_tiker[tiker]
                lot_akcii = akcii_all_info[figi_akcii].lot
                price_akc = last_prices.get(figi_akcii, None) #if dividend_data.get(tiker, 0) == 0 else last_prices.get(figi_akcii, None) + dividend_data[tiker].get('dividend_rub', 0)
                # print(tiker , price_akc, last_prices.get(figi_akcii, None))
                if last_prices.get(i, None) != None and last_prices.get(i, None) > 0 and price_akc != None and price_akc > 0:
                    lots = math.floor(future_all_info[i].basic_asset_size.units)
                    if 'PLZL' in tiker:
                        lots = lots / 10
                    price_fut = last_prices.get(i, None)
                    spread_real = price_akc / (price_fut / lots) * 100
                    # print(spread_real)
                    spread_sprav = await sprav_price_spread(price_akc, spread_real, figi=i, divid_rub=dividend_data[tiker].get('dividend_rub', 0) if dividend_data.get(tiker, 0) != 0 else 0)
                    # print('spravspread', spread_sprav)
                    sprav_price_fut = await sprav_price_future(price_akc, figi=i, future_akcii=future_akcii, divid_rub=dividend_data[tiker].get('dividend_rub', 0) if dividend_data.get(tiker, 0) != 0 else 0)
                    # print(f"{tiker} - sprav prace = {sprav_price_fut} price {price_fut}, ")
                    percent_fut_ot_sprav_price = await asy_get_percent(price_fut, sprav_price_fut)
                    if 'PLZL' in tiker:
                        print(f"{tiker, i} - lots {lots}, price_fut {price_fut} price_akcii {price_akc} cprav_fut {sprav_price_fut}"
                          f"percent {percent_fut_ot_sprav_price}")
                    name_future = f"{future_all_info[i].basic_asset if future_all_info[i].basic_asset != 'ABIO' else 'ISKJ'}-{kvartal}-{future_all_info[i].expiration_date.date().year % 100}"
                    news = ' 📰' if tiker in dict_sobitiy['news'] else ''
                    if tiker in dividend_data:
                        if percent_fut_ot_sprav_price >= percent or percent_fut_ot_sprav_price <= -percent:
                            percen_dohodn = round(dividend_data[tiker].get('dividend_rub', 0) / (price_akc / 100), 2)
                            rez = f"{await valyta_smail(percent_fut_ot_sprav_price)} • ({percent_fut_ot_sprav_price}%) {await link_text(tiker)}{news}\n" \
                                  f"{dividend_data[tiker]['dividend_rub']}р.{'👌' if dividend_data[tiker]['odobrenie_div'] else '⁉️'} • {percen_dohodn}% • {dividend_data[tiker]['date_close']}{'👌' if dividend_data[tiker]['odobrenie_reestr'] else '⁉️'}\n" \
                                  f"{await napravlenie_sdelok_2nogi(percent_fut_ot_sprav_price,  f'{name_future} / {tiker}', price_fut, price_akc,  1, int(lots / lot_akcii))}\n"#\nPrice(справ) - {sprav_price_fut}\nPrice(реал) - {price_fut}
                                  # f"Див.(прогноз) - {dividend_data[tiker]['dividend_rub']}р.\nЗакр. реес.(ожидание)- {dividend_data[tiker]['date_close']}\nИндекс стаб. выпл. див - {dividend_data[tiker]['dsi']}\n"#\nPrice(справ) - {sprav_price_fut}\nPrice(реал) - {price_fut}

                            message.append([rez, abs(percent_fut_ot_sprav_price)])
                    else:
                        if percent_fut_ot_sprav_price >= percent or percent_fut_ot_sprav_price <= -percent:
                            rez = f"{await valyta_smail(percent_fut_ot_sprav_price)} • ({percent_fut_ot_sprav_price}%) {await link_text(tiker)}{news}\n" \
                                  f"{await napravlenie_sdelok_2nogi(percent_fut_ot_sprav_price,  f'{name_future} / {tiker}', price_fut, price_akc,   1, int(lots / lot_akcii))}\n"#\nPrice(справ) - {sprav_price_fut}\nPrice(реал) - {price_fut}

                            message.append([rez, abs(percent_fut_ot_sprav_price)])
        mesage_sorted = sorted(message, key=lambda x: x[1], reverse=True)
        # return '\n'.join(message_)
        text_mesage_sorted  = ''.join([i[0] for i in mesage_sorted]) + '\n' if len(mesage_sorted) <= 24 else ''.join([i[0] for i in mesage_sorted[:24]]) + '\n'
        zagolovok = f"🧭 Время последнего обновления:\n{time_apgrade.date()}  время: {time_new}\n\n⚙️ {await podcher_text('Сканер поиска несправедливых цен фьючерсы на акций, сравнение текущей цены с её справедливым значением.')}\nЦена текущая / Цена справедливая\n\n" \
                    f"Ставка ЦБ используется - 21%\nДиапазон отк-я цены:  (- 0.5%) - (+0.5%)\n⁉️ - прогноз \n👌 - рекомендован сов.дир \n\n"
        finale_message = zagolovok + '\n' +  text_mesage_sorted
        print(f"dlina zagolovka {len(zagolovok)} - text {len(mesage_sorted) } ")
        s1 = await bot.edit_message_text(finale_message, chat_id=chenal_id, message_id=last_messa_id, parse_mode='HTML', disable_web_page_preview=True)
        if Flag.vikl_parse_kase:
            message_curent_kase = await new_text_kase_current(kase_curen_dict)
            if message_curent_kase and len(message_curent_kase ) > 1 :
                s2 = await bot.edit_message_text(message_curent_kase, chat_id=chenal_id, message_id=last_messa3_id, parse_mode='HTML', disable_web_page_preview=True)
        # print(mesage_sorted)
    else:
        message = f"🧭 Время последнего обновления:\n{time_apgrade.date()}  время: {time_new}\n\n " \
                  f"Технические работы"
        await bot.edit_message_text(message, chat_id=chenal_id, message_id=last_messa_id, parse_mode='HTML',
                                    disable_web_page_preview=True)

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

async def valuta_vtelegram():
    global yahoo_valyata
    current_time = datetime.datetime.now(moscow_tz).time()
    time_10x23_50 = await time_range('09:50:00', '23:50:00', current_time)

    # chenal_id = {'Сверчок': -1001854614186}
    chenal_id = Token.chenal_id
    # last_message = await bot.request()
    gr_unc = 31.1035
    last_message = await client2.get_messages(chenal_id, limit=100)
    last_messa_id = last_message[-6].id
    last_messa2_id = last_message[-5].id
    last_messa3_id = last_message[-4].id
    last_messa4_id = last_message[-3].id
    last_messa5_id = last_message[-2].id
    # print('Id message - ', last_messa2_id, last_messa3_id, last_messa_id)
    # try:
    if len(yahoo_valyata) == 20:
        print(yahoo_valyata)
        si1_price = last_prices.get(Figi_future.si1_figi, 1)
        si2_price = last_prices.get(Figi_future.si2_figi, 1)
        cr1_price = last_prices.get(Figi_future.cr1_figi, 1)
        cr2_price = last_prices.get(Figi_future.cr2_figi, 1)
        eu1_price = last_prices.get(Figi_future.eu1_figi, 1)
        eu2_price = last_prices.get(Figi_future.eu2_figi, 1)
        ucny1_price = last_prices.get(Figi_future.ucny1_figi, 1)
        ed1_price = last_prices.get(Figi_future.ed1_figi, 1)
        ed2_price = last_prices.get(Figi_future.ed2_figi, 1)
        gold1_price = last_prices.get(Figi_future.gold1_figi, 1)
        silver1_price = last_prices.get(Figi_future.silver1_figi, 1)
        nasdaq1_price = last_prices.get(Figi_future.nasdaq1_figi, 1)
        sp5001_price = last_prices.get(Figi_future.sp5001_figi, 1)
        usdcnh_for = yahoo_valyata['USDCNH'][0]
        cnyrub_megbank = yahoo_valyata['CNYRUB'][0]
        eurrub_megbank = yahoo_valyata['EURRUB'][0]
        usdrub_megbank = yahoo_valyata['USDRUB'][0]
        eurcnh_for = yahoo_valyata["EURCNH"][0]
        eurusd_for = yahoo_valyata["EURUSD"][0]
        silver_in = yahoo_valyata["XAGUSD"][0]
        gold_in = yahoo_valyata["XAUUSD"][0]
        nasdaq_in = yahoo_valyata["nasdaq"][0]
        sp500_in = yahoo_valyata["sp500"][0]
        percent_megbank_eur_cnh_eurcnh = round(eurrub_megbank / cnyrub_megbank /eurcnh_for, 2)
        percent_megbank_eur_usd_eurusd = round(eurrub_megbank / usdrub_megbank /eurusd_for, 2)
        percent_megbank_usd_cnh_usdcnh = round(usdrub_megbank / cnyrub_megbank /usdcnh_for, 2)
        print(f"Megbank - eur/cnh {percent_megbank_eur_cnh_eurcnh} eur/usd {percent_megbank_eur_usd_eurusd} usd/cnh - {percent_megbank_usd_cnh_usdcnh}")
        price_gold_gr_usd = round(gold_in / gr_unc, 2)
        # print(qqq_in)
        kurs_usdrub_spr = round(last_prices.get('BBG0013HRTL0', 1) * usdcnh_for, 4)
        kurs_eurrub_spr = round(last_prices.get('BBG0013HRTL0', 1) * eurcnh_for, 4)
        kurs_cb_usdrub = 87.0354
        kurs_cb_eurrub = 93.2994
        kurs_cb_cnyrub = 11.7964
        kurs_usdrub_spr = round(last_prices.get('BBG0013HRTL0', 1) * usdcnh_for, 4)
        kurs_eurrub_spr = round(last_prices.get('BBG0013HRTL0', 1) * eurcnh_for, 4)
        # si_sprav_price = round(1000 * (usd_rub_ru * (1 + 0.16 * (await expiration_date_future(si['si-6.24'])/365))))
        percent_si2_cr2_usdcnh = round(si2_price / cr2_price / 1000 / usdcnh_for * 100 -100, 3)
        percent_si_cr_ucny = round(si1_price / cr1_price / 1000 / ucny1_price * 100 -100, 3)#usdcnh_for
        percent_si_cr_usdcnh = round(si1_price / cr1_price / 1000 / usdcnh_for * 100 -100, 3)#usdcnh_for
        percent_eu2_cr2_eurcnh = round(eu2_price / cr2_price / 1000 / eurcnh_for * 100 -100, 3)
        percent_eu_cr_eurcnh = round(eu1_price / cr1_price / 1000 /eurcnh_for * 100 -100, 3) # await valuta_replace_float('EURCNH', yahoo_valyata, 4)
        percent_eu2_si2_eurusd = round(eu2_price / si2_price / eurusd_for * 100 -100, 3)
        percent_eu_si_eurusd = round(eu1_price / si1_price / eurusd_for * 100 -100, 3)
        percent_eu2_si2_ed2 = round(eu2_price / si2_price / ed2_price * 100 -100, 3)
        percent_eu_si_ed = round(eu1_price / si1_price / ed1_price * 100 -100, 3)
        percent_usf_cnf_ucny = round(last_prices.get(futures['USDRUBF'], 1) / last_prices.get(futures['CNYRUBF'], 1) / ucny1_price * 100 -100, 3)
        percent_usf_cnf_usdcnh = round(last_prices.get(futures['USDRUBF'], 1) / last_prices.get(futures['CNYRUBF'], 1) / usdcnh_for * 100 -100, 3)
        percent_euf_cnf_eurcnh = round(last_prices.get('FUTEURRUBF00', 1) / last_prices.get(futures['CNYRUBF'], 1) / eurcnh_for * 100 -100, 3)
        percent_euf_usf_eurusd = round(last_prices.get('FUTEURRUBF00', 1) / last_prices.get(futures['USDRUBF'], 1) / eurusd_for * 100 -100, 3)
        percent_ed_eurusd = round(ed1_price / eurusd_for * 100 - 100, 3)
        percent_ucny_usdcnh = round(ucny1_price / usdcnh_for * 100 - 100, 3)
        percent_ed2_eurusd = round(ed2_price / eurusd_for * 100 - 100, 3)
        percent_ed2_ed1 = round(ed2_price / ed1_price * 100 - 100, 3)
        percent_si2_si1 = round(si2_price / si1_price * 100 - 100, 3)
        percent_eu2_eu1 = round(eu2_price / eu1_price * 100 - 100, 3)
        percent_cr2_cr1 = round(cr2_price / cr1_price * 100 - 100, 3)
        percent_si1_usf = round((si1_price / last_prices.get(futures['USDRUBF'], 1)  / 1000) * 100 - 100, 3)
        percent_eu1_euf = round((eu1_price / 1000) / last_prices.get('FUTEURRUBF00', 1) * 100 - 100, 3)
        percent_cr1_crf = round(cr1_price / last_prices.get(futures['CNYRUBF'], 1)  * 100 - 100, 3)
        percent_cr1_cr_tom = round(cr1_price / last_prices.get('BBG0013HRTL0', 1) * 100 - 100, 3)
        percent_cr2_cr_tom = round(cr2_price / last_prices.get('BBG0013HRTL0', 1) * 100 - 100, 3)
        percent_usdrub_megb_spr = round(usdrub_megbank / kurs_usdrub_spr * 100 - 100 , 2)
        percent_eurrub_megb_spr = round(eurrub_megbank / kurs_eurrub_spr * 100 - 100 , 2)
        percent_si1_usdrub_megb = round(si1_price / 1000 / usdrub_megbank * 100 - 100 , 2)
        percent_eu1_eurrub_megb = round(eu1_price / 1000 / eurrub_megbank * 100 - 100 , 2)
        percent_euf_eurrub_megb = round(last_prices.get('FUTEURRUBF00', 1)  / eurrub_megbank * 100 - 100 , 2)
        percent_usf_usdrub_megb = round(last_prices.get(futures['USDRUBF'], 1)  / usdrub_megbank * 100 - 100 , 2)
        percent_cnf_cn_tom = round(last_prices.get(futures['CNYRUBF']) / last_prices.get('BBG0013HRTL0', 1) * 100 - 100 , 2)
        percent_cnyrub_megb_cn_tom = round(cnyrub_megbank / last_prices.get('BBG0013HRTL0', 1) * 100 - 100 , 2)
        print('ioioioiooioiio', usdrub_megbank, last_prices.get('BBG0013HRTL0'), percent_cnyrub_megb_cn_tom)
        kurs_cb_usdrub = 89.0499
        kurs_cb_eurrub = 95.3906
        percent_glf_gd1_si = round((last_prices.get('FUTGLDRUBF00', 1 ) * 31.1035) / gold1_price / (si1_price / 1000) * 100 - 100 , 3)
        percent_sv1_silver = round(silver1_price / silver_in * 100  -100, 3)
        percent_gd1_gold = round(gold1_price / gold_in * 100  -100, 3)
        percent_na1_nasdaq = round(nasdaq1_price / nasdaq_in * 100  -100, 3)
        percent_sf1_sp500 = round((sp5001_price * 10) / sp500_in * 100  -100, 3)
        sprav_price_cr1 = await sprav_price_future(last_prices.get('BBG0013HRTL0', 1), figi='FUTCNY062500', max_percente_first_day=2.7)
        percent_sprav_price_cr1 = round(cr1_price / sprav_price_cr1 * 100 -100, 3)
        # sprav_price_silver = await sprav_price_future(silver_in, figi='FUTSILV03250', max_percente_first_day=3.25)
        # percent_sprav_price_silver = await asy_get_percent(sprav_price_silver, last_prices.get('FUTSILV03250', None) )
        # sprav_price_gold = await sprav_price_future(gold_in, figi='FUTGOLD03250', max_percente_first_day=2.7)
        # percent_sprav_price_gold = await asy_get_percent(sprav_price_gold, last_prices.get('FUTGOLD03250',None))
        # # percent_sprav_price_gold =round(percent_sprav_price_gold -  1.3 if percent_sprav_price_gold >= 0 else percent_sprav_price_gold - -1.3, 3)
        #
        # sprav_price_nasdaq = await sprav_price_future(nasdaq_in, figi='FUTNASD03250', max_percente_first_day=1.7)
        # percent_sprav_price_nasdaq = await asy_get_percent(sprav_price_nasdaq, last_prices.get('FUTNASD03250',None))
        #
        # sprav_price_sp500 = await sprav_price_future(sp500_in, figi='FUTSPYF03250', max_percente_first_day=1.9)
        # percent_sprav_price_sp500 = await asy_get_percent(sprav_price_sp500, last_prices.get('FUTSPYF03250',None) * 10 )
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
                                await napravlenie_sdelok_3nogi(percent_si_cr_ucny, 'Si1 / CR1 / UCNY', price1=si1_price, price2=cr1_price, price3=ucny1_price) , abs(percent_si_cr_ucny)],
                                [f"{await valyta_smail(percent_si_cr_usdcnh)} •  ({percent_si_cr_usdcnh}%){await smail_vnimanie(percent_si_cr_usdcnh)}\n{await link_text('Si1 / CR1 / USDCNH(for)')}\n" +
                                await napravlenie_sdelok_3nogi(percent_si_cr_usdcnh, 'Si1 / CR1 / USDCNH(for)', price1=si1_price, price2=cr1_price, price3=usdcnh_for) , abs(percent_si_cr_usdcnh)],
                                [f"{await valyta_smail(percent_si2_cr2_usdcnh)} •  ({percent_si2_cr2_usdcnh}%){await smail_vnimanie(percent_si2_cr2_usdcnh)}\n{await link_text('Si2 / CR2 / USDCNH(for)')}\n" +
                                await napravlenie_sdelok_3nogi(percent_si2_cr2_usdcnh, 'Si2 / CR2 / USDCNH(for)', price1=si2_price, price2=cr2_price, price3=usdcnh_for) , abs(percent_si2_cr2_usdcnh)],
                                [f"{await valyta_smail(percent_eu_cr_eurcnh)} •  ({percent_eu_cr_eurcnh}%){await smail_vnimanie(percent_eu_cr_eurcnh)}\n{await link_text('Eu1 / Cr1 / EURCNH(for)')}\n" +
                                await napravlenie_sdelok_3nogi(percent_eu_cr_eurcnh, 'Eu1 / Cr1 / EURCNH(for)', price1=eu1_price, price2=cr1_price, price3=eurcnh_for), abs(percent_eu_cr_eurcnh)],
                                [f"{await valyta_smail(percent_eu2_cr2_eurcnh)} •  ({percent_eu2_cr2_eurcnh}%){await smail_vnimanie(percent_eu2_cr2_eurcnh)}\n{await link_text('Eu2 / Cr2 / EURCNH(for)')}\n" +
                                await napravlenie_sdelok_3nogi(percent_eu2_cr2_eurcnh, 'Eu2 / Cr2 / EURCNH(for)', price1=eu2_price, price2=cr2_price, price3=eurcnh_for), abs(percent_eu2_cr2_eurcnh)],
                                [f"{await valyta_smail(percent_eu_si_eurusd)} •  ({percent_eu_si_eurusd}%){await smail_vnimanie(percent_eu_si_eurusd)}\n{await link_text('Eu1 / Si1 / EURUSD(for)')}\n" +
                                await napravlenie_sdelok_3nogi(percent_eu_si_eurusd, 'Eu1 / Si1 / EURUSD(for)', price1=eu1_price, price2=si1_price, price3=eurusd_for), abs(percent_eu_si_eurusd)],
                                [f"{await valyta_smail(percent_eu2_si2_eurusd)} •  ({percent_eu2_si2_eurusd}%){await smail_vnimanie(percent_eu2_si2_eurusd)}\n{await link_text('Eu2 / Si2 / EURUSD(for)')}\n" +
                                await napravlenie_sdelok_3nogi(percent_eu2_si2_eurusd, 'Eu2 / Si2 / EURUSD(for)', price1=eu2_price, price2=si2_price, price3=eurusd_for), abs(percent_eu2_si2_eurusd)],
                                [f"{await valyta_smail(percent_eu_si_ed)} •  ({percent_eu_si_ed}%){await smail_vnimanie(percent_eu_si_ed)}\n{await link_text('Eu1 / Si1 / ED')}\n" +
                                await napravlenie_sdelok_3nogi(percent_eu_si_ed, 'Eu1 / Si1 / ED',  price1=eu1_price, price2=si1_price, price3=ed1_price ), abs(percent_eu_si_ed)],
                                [f"{await valyta_smail(percent_eu2_si2_ed2)} •  ({percent_eu2_si2_ed2}%){await smail_vnimanie(percent_eu2_si2_ed2)}\n{await link_text('Eu2 / Si2 / ED2')}\n" +
                                await napravlenie_sdelok_3nogi(percent_eu2_si2_ed2, 'Eu2 / Si2 / ED2',  price1=eu2_price, price2=si2_price, price3=ed2_price ), abs(percent_eu2_si2_ed2)],
                                [f"{await valyta_smail(percent_usf_cnf_usdcnh)} •  ({percent_usf_cnf_usdcnh}%){await smail_vnimanie(percent_usf_cnf_usdcnh)}\n{await link_text('US.F / CN.F / USDCNH(for)')}\n" +
                                await napravlenie_sdelok_3nogi(percent_usf_cnf_usdcnh, 'US.F / CN.F / USDCNH(for)', price1=last_prices.get(futures['USDRUBF'], 1), price2=last_prices.get(futures['CNYRUBF'], 1), price3=usdcnh_for), abs(percent_usf_cnf_usdcnh)],
                                [f"{await valyta_smail(percent_usf_cnf_ucny)} •  ({percent_usf_cnf_ucny}%){await smail_vnimanie(percent_usf_cnf_ucny)}\n{await link_text('US.F / CN.F / UCNY')}\n" +
                                await napravlenie_sdelok_3nogi(percent_usf_cnf_ucny, 'US.F / CN.F / UCNY', price1=last_prices.get(futures['USDRUBF'], 1), price2=last_prices.get(futures['CNYRUBF'], 1), price3=ucny1_price), abs(percent_usf_cnf_ucny)],
                                [f"{await valyta_smail(percent_euf_cnf_eurcnh)} •  ({percent_euf_cnf_eurcnh}%){await smail_vnimanie(percent_euf_cnf_eurcnh)}\n{await link_text('EU.F / CN.F / EURCNH(for)')}\n" +
                                await napravlenie_sdelok_3nogi(percent_euf_cnf_eurcnh, 'EU.F / CN.F / EURCNH(for)', price1=last_prices.get('FUTEURRUBF00', 1), price2=last_prices.get(futures['CNYRUBF'], 1), price3=eurcnh_for), abs(percent_euf_cnf_eurcnh)],
                                [f"{await valyta_smail(percent_euf_usf_eurusd)} •  ({percent_euf_usf_eurusd}%){await smail_vnimanie(percent_euf_usf_eurusd)}\n{await link_text('EU.F / US.F / EURUSD(for)')}\n" +
                                await napravlenie_sdelok_3nogi(percent_euf_usf_eurusd, 'EU.F / US.F / EURUSD(for)', price1=last_prices.get('FUTEURRUBF00', 1), price2=last_prices.get(futures['USDRUBF'], 1), price3=eurusd_for), abs(percent_euf_usf_eurusd)],
                                [f"{await valyta_smail(percent_ed_eurusd)} •  ({percent_ed_eurusd}%){await smail_vnimanie(percent_ed_eurusd)}\n{await link_text('ED / EURUSD(for)')}\n" +
                                await napravlenie_sdelok_2nogi(percent_ed_eurusd, 'ED / EURUSD(for)', price1=ed1_price, price2=eurusd_for, lot1=1, lot2=lotnost_forex['EURUSD']), abs(percent_ed_eurusd)],
                                [f"{await valyta_smail(percent_ed2_eurusd)} •  ({percent_ed2_eurusd}%){await smail_vnimanie(percent_ed2_eurusd)}\n{await link_text('ED2 / EURUSD(for)')}\n" +
                                await napravlenie_sdelok_2nogi(percent_ed2_eurusd, 'ED2 / EURUSD(for)', price1=ed2_price, price2=eurusd_for, lot1=1, lot2=lotnost_forex['EURUSD']), abs(percent_ed2_eurusd)],
                                [f"{await valyta_smail(percent_ucny_usdcnh)} •  ({percent_ucny_usdcnh}%){await smail_vnimanie(percent_ucny_usdcnh)}\n{await link_text('UCNY / USDCNH(for)')}\n" +
                                await napravlenie_sdelok_2nogi(percent_ucny_usdcnh, 'UCNY / USDCNH(for)', price1=ucny1_price, price2=usdcnh_for, lot1=1, lot2=lotnost_forex['EURUSD']), abs(percent_ucny_usdcnh)],

                                 ]
        text_future_kotirovri2 = [[f"{await valyta_smail(percent_si2_si1)} •  ({percent_si2_si1}%)\n{await link_text('SI2 / SI1')}\n" +
                                await napravlenie_sdelok_2nogi(percent_si2_si1, 'SI2 / SI1', price1=round(si2_price / 1000, 3), price2=round(si1_price / 1000, 3), lot1=1, lot2=1, ukazat_napravlenie_sdelok=False), abs(percent_si2_si1)],
                                [f"{await valyta_smail(percent_eu2_eu1)} •  ({percent_eu2_eu1}%)\n{await link_text('EU2 / EU1')}\n" +
                                await napravlenie_sdelok_2nogi(percent_eu2_eu1, 'EU2 / EU1', price1=round(eu2_price / 1000, 3), price2=round(eu1_price / 1000, 3), lot1=1, lot2=1, ukazat_napravlenie_sdelok=False), abs(percent_eu2_eu1)],
                                [f"{await valyta_smail(percent_cr2_cr1)} •  ({percent_cr2_cr1}%)\n{await link_text('CR2 / CR1')}\n" +
                                await napravlenie_sdelok_2nogi(percent_cr2_cr1, 'CR2 / CR1', price1=cr2_price, price2=cr1_price, lot1=1, lot2=1, ukazat_napravlenie_sdelok=False), abs(percent_cr2_cr1)],
                                [f"{await valyta_smail(percent_si1_usf)} •  ({percent_si1_usf}%)\n{await link_text('Si1 / US.F')}\n" +
                                await napravlenie_sdelok_2nogi(percent_si1_usf, 'Si1 / US.F', price1=round(si1_price / 1000, 3), price2=last_prices.get(futures['USDRUBF'], 1), lot1=1, lot2=1, ukazat_napravlenie_sdelok=False), abs(percent_si1_usf)],
                                [f"{await valyta_smail(percent_eu1_euf)} •  ({percent_eu1_euf}%)\n{await link_text('EU1 / EU.F')}\n" +
                                await napravlenie_sdelok_2nogi(percent_eu1_euf, 'EU1 / EU.F', price1=round(eu1_price / 1000, 3), price2=last_prices.get('FUTEURRUBF00', 1), lot1=1, lot2=1, ukazat_napravlenie_sdelok=False), abs(percent_eu1_euf)],
                                [f"{await valyta_smail(percent_cr1_crf)} •  ({percent_cr1_crf}%)\n{await link_text('CR1 / CR.F')}\n" +
                                await napravlenie_sdelok_2nogi(percent_cr1_crf, 'CR1 / CR.F', price1=cr1_price, price2=last_prices.get(futures['CNYRUBF'], 1), lot1=1, lot2=1, ukazat_napravlenie_sdelok=False), abs(percent_cr1_crf)],
                                # [f"{await valyta_smail(percent_cr1_cr_tom)} •  ({percent_cr1_cr_tom}%)\n{await link_text('CR1 / CR_TOM')}\n" +
                                # await napravlenie_sdelok_2nogi(percent_cr1_cr_tom, 'CR1 / CR_TOM', price1=last_prices.get('FUTCNY122400', 1), price2=last_prices.get('BBG0013HRTL0', 1), lot1=1, lot2=1, ukazat_napravlenie_sdelok=False), abs(percent_cr1_cr_tom)],
                                [f"{await valyta_smail(percent_cr2_cr_tom)} •  ({percent_cr2_cr_tom}%)\n{await link_text('CR2 / CR_TOM')}\n" +
                                await napravlenie_sdelok_2nogi(percent_cr2_cr_tom, 'CR2 / CR_TOM', price1=cr2_price, price2=last_prices.get('BBG0013HRTL0', 1), lot1=1, lot2=1, ukazat_napravlenie_sdelok=False), abs(percent_cr2_cr_tom)],
                                [f"{await valyta_smail(percent_ed2_ed1)} •  ({percent_ed2_ed1}%)\n{await link_text('ED2 / ED1')}\n" +
                                await napravlenie_sdelok_2nogi(percent_ed2_ed1, 'ED2 / ED1', price1=ed2_price, price2=ed1_price, lot1=1, lot2=1, ukazat_napravlenie_sdelok=False), abs(percent_ed2_ed1)],

                                 ]
        text_fur_spot = [f"{await valyta_smail(percent_sprav_price_cr1)} •  ({percent_sprav_price_cr1}%){await smail_vnimanie(percent_sprav_price_cr1)}\n" ,
                         f"{await link_text('CR1 (спр) / CR1 (real)')}\n" ,
                         f"CR1 (спр) -> цена справ-вая = {sprav_price_cr1}\n\n\n"]
        delitel2 = 0.1
        text_valuta_zagolovok = [f"🧭 Время последнего обновления:\n{time_apgrade.date()}  время: {time_new}\n\n" ,
               f"Один знак  '❗' =  {delitel2}%\n\n",
               f"⚙️ Валюта , межбанк👇👇👇\n\n"]
        text_valuta_kotirovki = [[f"{await valyta_smail(percent_usdrub_megb_spr)} •  ({percent_usdrub_megb_spr}%)\n{await link_text('USDRUB(межб) / USDRUB(спр)')}\nCNY_TOM x USDCNH(for) • {kurs_usdrub_spr}\nКурс {await link_text('USDRUB межбанк')} • {usdrub_megbank}\n\n", abs(percent_usdrub_megb_spr)],
                                 [f"{await valyta_smail(percent_eurrub_megb_spr)} •  ({percent_eurrub_megb_spr}%)\n{await link_text('EURRUB(межб) / EURRUB(спр)')}\nCNY_TOM x EURCNH(for) • {kurs_eurrub_spr}\nКурс {await link_text('EURRUB межбанк')} • {eurrub_megbank}\n\n", abs(percent_eurrub_megb_spr)],
                                 [f"{await valyta_smail(percent_cnyrub_megb_cn_tom)} •  ({percent_cnyrub_megb_cn_tom}%)\n{await link_text('CNYRUB(межб) / CNY_TOM')}\nCNY_TOM • {last_prices.get('BBG0013HRTL0', 1)}\nCNYRUB({await link_text('межбанк')}) • {cnyrub_megbank}\n\n", abs(percent_cnyrub_megb_cn_tom)],
                                 [f"\n{await valyta_smail(percent_cr1_cr_tom)} •  ({percent_cr1_cr_tom}%)\n{await link_text('CR1 / CNY_TOM')}\nCR1  • {cr1_price}\nCNY_TOM' • {last_prices.get('BBG0013HRTL0', 1)}\n\n", 0],
                                 [f"{await valyta_smail(percent_cnf_cn_tom)} •  ({percent_cnf_cn_tom}%)\n{await link_text('CNYRUBF / CNY_TOM')}\nCNYRUBF  • {last_prices.get(futures['CNYRUBF'])}\nCNY_TOM' • {last_prices.get('BBG0013HRTL0', 1)}\n\n", 0],
                                 [f"{await valyta_smail(percent_si1_usdrub_megb)} •  ({percent_si1_usdrub_megb}%)\n{await link_text('SI1 / USDRUB(межб)')}\nSI1  • {si1_price}\nUSDRUB({await link_text('межбанк')}) • {usdrub_megbank}\n\n", 0],
                                 [f"{await valyta_smail(percent_usf_usdrub_megb)} •  ({percent_usf_usdrub_megb}%)\n{await link_text('USDRUBF / USDRUB(межб)')}\nUSF  • {last_prices.get(futures['USDRUBF'], 1)}\nUSDRUB({await link_text('межбанк')}) • {usdrub_megbank}\n\n", 0],
                                 [f"{await valyta_smail(percent_eu1_eurrub_megb)} •  ({percent_eu1_eurrub_megb}%)\n{await link_text('EU1 / EURRUB(межб)')}\nEU1 • {eu1_price}\nEURRUB({await link_text('межбанк')}) • {eurrub_megbank}\n\n", 0],
                                 [f"{await valyta_smail(percent_euf_eurrub_megb)} •  ({percent_euf_eurrub_megb}%)\n{await link_text('EURRUBF / EURRUB(межб)')}\nEU1 • {last_prices.get('FUTEURRUBF00', 1)}\nEURRUB({await link_text('межбанк')}) • {eurrub_megbank}\n\n", 0],
                                 [f"{await valyta_smail(percent_glf_gd1_si)} •  ({percent_glf_gd1_si}%)\n🔒 {await link_text('***P** / *1* / *I1**')}\n\n", 0],

                                 ]

        time_apgrade1 = datetime.datetime.now(moscow_tz)
        time_new1 = time_apgrade.strftime("%H:%M:%S")
        delitel = 0.5
        silver_text = await create_tex_sprav_price_future(percent_sv1_silver, 'SV1 / XAGUSD(for)', delitel=0.5)
        silver_text += await napravlenie_sdelok_2nogi(percent_sv1_silver, 'SV1 / XAGUSD(for)', price1=silver1_price, price2=silver_in, lot1=lotnost_forex['silver']['moex'], lot2=lotnost_forex['silver']['forex'])
        gold_text = await create_tex_sprav_price_future(percent_gd1_gold, 'GOLD1 / XAUUSD(for)', delitel=0.5)
        gold_text += await napravlenie_sdelok_2nogi(percent_gd1_gold, 'GOLD1 / XAUUSD(for)', price1=gold1_price, price2=gold_in, lot1=lotnost_forex['gold']['moex'], lot2=lotnost_forex['gold']['forex'])
        nasdaq_text = await create_tex_sprav_price_future(percent_na1_nasdaq, 'NA1 / NDXUSD(for)', delitel=0.5)
        nasdaq_text += await napravlenie_sdelok_2nogi(percent_na1_nasdaq, 'NA1 / NDXUSD(for)', price1=nasdaq1_price, price2=nasdaq_in, lot1=lotnost_forex['nasdaq']['moex'], lot2=lotnost_forex['nasdaq']['forex'])
        sp500_text = await create_tex_sprav_price_future(percent_sf1_sp500, 'SF1 / SPXUSD(for)', delitel=0.5)
        sp500_text += await napravlenie_sdelok_2nogi(percent_sf1_sp500, 'SF1 / SPXUSD(for)', price1=sp5001_price , price2=sp500_in, lot1=lotnost_forex['sp500']['moex'], lot2=lotnost_forex['sp500']['forex'])
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
        s1 = await bot.edit_message_text(finali_message2, chat_id=chenal_id, message_id=last_messa3_id, parse_mode='HTML', disable_web_page_preview=True)
        s2 = await bot.edit_message_text(finali_message, chat_id=chenal_id, message_id=last_messa2_id, parse_mode='HTML', disable_web_page_preview=True)
        current_time2 = datetime.datetime.now(moscow_tz).time()
        # print(f"time func: {current_time2} - {current_time}")
    # except Exception as e:
    #     error_message = traceback.format_exc()
    #     print(f'Произошла ошибка функции valuta_vtelegram:\n{error_message}')
    #     print(e)

url_moex = "https://www.moex.com/ru/contract.aspx?code=GLDRUBF"

async def start_cicl_5s():
    coun = 0
    flag1 = True
    flag2 = False
    while True:
        try:
            print(f"start")
            if flag1:
                print('flag1')
                await valuta_vtelegram()
                flag1 = False
                flag2 = True
            elif flag2:
                print('flag2')
                await arbtrage_future_akcii(Kvartal.real_kvartal, future_akcii=True)
                flag1 = True
                flag2 = False
            await get_last_prices_dict()
            await upgrade_options_mesaage_telegramm(bot, client2)
        except Exception as e:
            await sendErorsTelegram(bot, sec_start=5)
            error_message = traceback.format_exc()
            print(f'Произошла ошибка функции valuta_vtelegram:\n{error_message}')
            print(e)
        await asyncio.sleep(5)

async def start_cicl_15m():
    coun = 0
    try:
        while True:
            current_time = datetime.datetime.now(moscow_tz).time()
            time_10_15_18_50 = await time_range('10:15:00', '18:50:00', current_time)
            if time_10_15_18_50:
                await get_fanding_moex()
            # print(fanding)
            await asyncio.sleep(60)

    except Exception as e:
        await sendErorsTelegram(bot, sec_start=5)
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
        await sendErorsTelegram(bot, sec_start=5)
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
            # print(565656565, last_prices.get('BBG0013HGFT4'))
            # print(f"cxtnxbr = {x}")
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
        await sendErorsTelegram(bot, sec_start=5)
        error_message = traceback.format_exc()
        print(f'Произошла ошибка функции valuta_vtelegram:\n{error_message}')
        print(e)
        await asyncio.sleep(5)
        await start_get_last_prices_dict()

async def start_parse_rss():
    while Flag.parse_rss:
        try:
            await check_rss(URL_rss.rss_tass_all_news, 'tass', bot, link_text)
            await check_rss(URL_rss.rss_interfaks_all_news, 'interfaks', bot, link_text)
            google_alerts = [await check_rss(i, 'google_alerts', bot, link_text) for i in URL_rss.list_rss_googleAlert]
            if google_alerts:
                for i in google_alerts:
                    print(i)
        except Exception:
            await sendErorsTelegram(bot, sec_start=60)
            await asyncio.sleep(60)

async def start_dic_yaho_valuta():
 try:
     while True:
         print(dict_sobitiy)
         vihodnie = await subbota_voskresen()
         diapazone_23_6 = await time_diapazone('23:30', '06:00')
         await dict_yahoo_valuta()
         await asyncio.sleep(60) if vihodnie or diapazone_23_6 else await asyncio.sleep(5)
 except Exception:
     await sendErorsTelegram(bot, sec_start=5)
     await asyncio.sleep(5)
     await start_dic_yaho_valuta()

list_100_last_news = []
async def start_parse_news_site():
    last_message = await client2.get_messages(Chenal_id.trading_times_id, limit=100)
    for i in last_message:
        news = str(i.message).split('\n\n')
        if len(news) == 3:
            list_100_last_news.append(news[1])
    # print(list_100_last_news)
    # print(last_message)
    while Flag.parse_news:
        try:
            await parse_rbk(list_100_last_news, bot, link_text)
            await parse_komersant(list_100_last_news, bot, link_text)
            await asyncio.sleep(random.uniform(10, 120))
        except Exception:
            await sendErorsTelegram(bot, sec_start='random')
            await asyncio.sleep(random.uniform(2, 60))


async def start_parse_options():
    while True:
        await create_dict_options()

async def start_create_histiri_volatiliti():
    while True:
        await create_dict_HVolatiliti_options()
        await asyncio.sleep(5)

list_task = [ start_create_histiri_volatiliti(), start_parse_options() , start_cicl_5s(), start_dic_yaho_valuta(), start_get_last_prices_dict(), start_cicl_15m(), start_cicl_60m(), start_parse_news_site(), start_parse_rss(), fetch_messages(client=client, id_channel=Chenal_id.istochnik_news1)]#bot_discord.start(Token.discordBot_WarrenWallet) , запуск парсинга с биржи касе parse_price_curent_kase(kase_curen_dict)

async def main():
    # Запуск периодических задач в фоновом режиме
    await asyncio.gather(*list_task)

    # Запуск бота
    await dp.start_polling()

p = ['KZOSP', 'TATNP', 'NKHP', 'BANEP', 'MRKP', 'TRNFP', 'SNGSP', 'KAZTP', 'TGKBP',
     'KRKNP', 'NKNCP', 'RTKMP', 'FIXP', 'MGTSP', 'PMSBP', 'GAZP', 'SBERP', 'LNZLP', 'RASP',
     'LSNGP', 'NMTP', 'CNTLP', 'MTLRP', '📅', '🔮', '📁', '🛩', '#отчётность',  '#мсфо' , '#банки',
     '#консенсус',  '#металлурги' , '⭐', '#календарь', '#никель', '#цбрф', 'PN Alert', '#рсбу', '#дивиденды',
     '📏', '💼', '— PN', '📘', '#банки' , '#авиа', '❗', '💳', 'Bloomberg ✅', '-[статья]', '[статья]', 'stocksi', '@prioritynews_bot',
     'ultimate', 'prior', 'PN Alert']


fast_id  = [-1001750058000,]

@client.on(events.NewMessage(chats=[Chenal_id.istochnik_news1, Chenal_id.istochnik_news2]))#chats=Config.fast_id + Chenal.all_chenal_list_client + Config.news_vip_id    #chats=[news.get('ALL NEWS MOEX | Priority News') + news.get('Королёвский | вестник')]
async def hendler(event):
    global dict_sobitiy
    # print(akcii_moex_tiker)
    id_chennal = event.message.chat_id
    text = Text(event.message.message)
    blumberg_chek_list = ['🇨🇳', '🇷🇺', '⚔️', '🛢']
    if id_chennal == Chenal_id.istochnik_news1:
        if len(text.strip()) >= 20:
            # print(text)
            text = text.replace_all(['$', '@prioritynews_bot', 'Alert'])
            # text = text.replace('$', '').replace('@prioritynews_bot', '').replace('Alert', '')
            text_list = text.split('\n')
            text = ' '.join([i for i in text.split() if  i.strip()])
            tiker = text_list[0] if len(text_list) > 1 else ''
            flag1 = tiker.replace(',', '').replace('`', '') in akcii_moex_tiker.keys()
            if flag1:
                dict_sobitiy['news'].add(tiker)
            text = Text(text.replace(tiker, ''))
            text = text.replace_all(p)
            text = text.replace_all(akcii_moex_tiker)
            text = text.strip()
            text_discord = tiker +'\n' + text if len(text_list) > 1 else text
            text_telegram = '🔹🔻🔸\n\n' + tiker +'\n' + text if len(text_list) > 1 else '🔹🔻🔸\n\n' + text
            text_discord = f"{text_discord}\n\n▫️ The Trading Times"
            text_telegram = f"{text_telegram}\n\n🅾️ {await link_text('The Trading Times')}"
            text_lower = text.lower()
            flag = 'привет' in text_lower or 'новый сервис' in text_lower or 'пульс' in text_lower or 'преимущест' in text_lower or 'запуск' in text_lower \
                   or 'условия' in text_lower or 'лента новостей' in text_lower or 'проп' in text_lower or 'напом' in text_lower or 'тариф' in text_lower \
                   or 'ultim' in text_lower or 'prior' in text_lower or 'stocksi' in text_lower or 't.me' in text_lower or 'telegram', 'источник' in text_lower \
                   or 'ultimate' in text_lower
            if Flag.vikluchatel_webhook and flag1:
                await webhook_discord(WebhookDiscod.webhook2, text_discord)
                await webhook_discord(WebhookDiscod.webhook1, text)
            if Flag.knoka_send_post and flag == False and flag == False and flag1:
                await bot.send_message(Chenal_id.trading_times_id, text_telegram, parse_mode='HTML', disable_web_page_preview=True)
    elif Chenal_id.istochnik_news2 == id_chennal and text.check_words_in_text(blumberg_chek_list):
        if len(text.strip()) >= 20:
            # print(text)
            text = text.replace_all([ '💳', 'Bloomberg ✅', '-[статья]', '[статья]'])
            text = text.strip()
            text_discord = text
            text_telegram = '🔹🔻🔸\n\n' + text
            text_discord = f"{text_discord}\n\n▫️ The Trading Times"
            text_telegram = f"{text_telegram}\n\n🅾️ {await link_text('The Trading Times')}"
            if Flag.vikluchatel_webhook:
                await webhook_discord(WebhookDiscod.webhook2, text_discord)
                await webhook_discord(WebhookDiscod.webhook1, text)
            if Flag.knoka_send_post:
                await bot.send_message(Chenal_id.trading_times_id, text_telegram, parse_mode='HTML', disable_web_page_preview=True)




def trtetete(cek):
    time.sleep(cek)
    print(1111111111111111111111111111111111111111111111111111111111)


crypto_blumberg = -1001872252940
cointelegraph =  -1001072723547
cripto_time = -1002330259431
ya = 321329414
@client2.on(events.NewMessage(chats=[cointelegraph, crypto_blumberg, ya]))#chats=[]chats=[cointelegraph,]
async def hendler(event):
    id_chennal = event.message.chat_id
    time_data = event.message.date
    print(time_data.day)
    text = Text(event.message.message)
    if id_chennal == cointelegraph or id_chennal == ya:
        loop = asyncio.get_event_loop()
        ru_text = await loop.run_in_executor(None, translate_text, text)
        if event.photo:
            await dowload_photo_adn_send(bot, event, ru_text, cripto_time)
        else:
            await bot.send_message(chat_id=cripto_time, text=ru_text)
    elif id_chennal == crypto_blumberg:
        if event.photo:
            await dowload_photo_adn_send(bot, event, text, cripto_time)
        else:
            await bot.send_message(chat_id=cripto_time, text=text)
    elif id_chennal == ya:
        pass




def finali_func():
    loop1 = asyncio.get_event_loop()
    loop1.run_until_complete(bot.send_message(Chenal_id.LogsErroors, f"‼️ Скрипт остановился на сервере"))


def finalli_error():
    loop1 = asyncio.get_event_loop()
    loop1.run_until_complete(sendErorsTelegram(bot))

if __name__ == '__main__':
    # client.start()
    # client2.start()
    # # bot_discord.start(Token.discordBot_WarrenWallet)
    # # bot_discord.run(Token.discordBot_WarrenWallet)
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())

    try:
        # Запуск ваших клиентовзш
        client.start()
        client2.start()

        # Запуск основного асинхронного цикла
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except Exception as e:
        # Обработка ошибок
        time.sleep(2)
        finalli_error()
        print(f"Произошла ошибка: {e}")
    finally:
        # Этот блок выполнится всегда, независимо от успеха или ошибки
         finali_func()