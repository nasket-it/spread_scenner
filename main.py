import traceback
import math
from yahoo_finance import  yahoo_valyata, dict_yahoo_valuta
from telethon.sync import TelegramClient, events
from info_figi_ti import *
from secrete import Token
import asyncio
from tinkoff_get_func import (
    time_range, get_last_price, expiration_date_future,asy_get_percent,
    arbtrage_future_akcii, last_prices, get_last_prices_dict, sprav_price_future,
    )
from Config import InfoTiker, Config, Chenal
from aiogram import Bot, Dispatcher, types, executor
from aiogram.utils.markdown import link
from datetime import *
import datetime
import pytz

# Создаем объект временной зоны для Москвы
moscow_tz = pytz.timezone('Europe/Moscow')

client2 = TelegramClient(Token.phone2, Token.api_id2, Token.api_hash2)

API_TOKEN = Token.bot_token


# Создаем объекты бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)



account = ['-1001892817733','-1001857334624']
api_id = Token.api_id  # задаем API
api_hash = Token.api_hash  # задаем HASH
phone = Token.phone

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

async def smail_vnimanie(percent, delitel=0.1, znak='❗️'):
    # Используем абсолютное значение процента для упрощения
    abs_percent = abs(percent)
    smail = znak
    smail_stop = '  🙅‍'
    # Округляем вверх, чтобы получить правильное количество символов '❗️'
    percent_namber = math.ceil(abs_percent // delitel)
    if percent_namber == 0:
        return smail_stop
    elif percent_namber <= 6:
        return percent_namber * smail
    else:
        return 6 * smail + '+'

async def valuta_replace_float(valut_para, dict, kol_znakov):
    price = dict['valuta'][valut_para][0].replace('.', '') if valut_para in ['gold_fut', 'gold_spot', 'XAUUSD', "nasdaq", "sp500"] else dict['valuta'][valut_para][0]
    return round(float(price.replace(',', '.')), kol_znakov)

async def percent(num_100, num_rezultat):
    return round(num_100 / num_rezultat * 100 - 100, 2)


async def napravlenie_sdelok_3nogi(percent, svazka : str, price1 : float, price2 : float, price3 : float ,delitel=0.1 ):
    lot2 = round(price1 / price2, 1)
    list_tiker = svazka.split('/')
    abs_percent = abs(percent)
    percent_namber = math.ceil(abs_percent // delitel)
    if percent < 0 and percent_namber >= 1 :
        return f"Лонг {list_tiker[0].strip()}- 1 ({await link_text(price1)})\n" \
               f"Шорт {list_tiker[1].strip()}- {round(lot2 / 1000, 1) if list_tiker[1].strip() == 'CR1' or list_tiker[1].strip() == 'Cr1' else lot2} ({await link_text(price2)})\n" \
               f"Шорт {list_tiker[2].strip()}- 1 ({await link_text(price3)})\n\n"
    elif percent > 0 and percent_namber >= 1 :
        return f"Шорт {list_tiker[0].strip()}- 1 ({await link_text(price1)})\n" \
               f"Лонг {list_tiker[1].strip()}- {round(lot2 / 1000, 1) if list_tiker[1].strip() == 'CR1' or list_tiker[1].strip() == 'Cr1' else lot2} ({await link_text(price2)})\n" \
               f"Лонг {list_tiker[2].strip()}- 1 ({await link_text(price3)})\n\n"
    else:
        return f"Цена в пределах справедливой \n"\
               f"{list_tiker[0].strip()}- 1 ({await link_text(price1)})\n" \
               f"{list_tiker[1].strip()}- {round(lot2 / 1000, 1) if list_tiker[1].strip() == 'CR1' or list_tiker[1].strip() == 'Cr1' else lot2} ({await link_text(price2)})\n" \
               f"{list_tiker[2].strip()}- 1 ({await link_text(price3)})\n\n"



async def napravlenie_sdelok_2nogi(percent, svazka : str, price1 : float, price2 : float, lot1, lot2, delitel=0.1):
    list_tiker = svazka.split('/')
    abs_percent = abs(percent)
    percent_namber = math.ceil(abs_percent // delitel)
    if percent < 0 and percent_namber >= 1 :
        return f"Лонг {list_tiker[0].strip()}- {lot1} ({await link_text(price1)})\n" \
               f"Шорт {list_tiker[1].strip()}- {lot2} ({await link_text(price2)})\n\n"
    elif percent > 0 and percent_namber >= 1 :
        return f"Шорт {list_tiker[0].strip()}- {lot1} ({await link_text(price1)})\n" \
               f"Лонг {list_tiker[1].strip()}- {lot2} ({await link_text(price2)})\n\n"
    else:
        return f"Цена в пределах справедливой \n"\
               f"{list_tiker[0].strip()}- {lot1} ({await link_text(price1)})\n" \
               f"{list_tiker[1].strip()}- {lot2} ({await link_text(price2)})\n\n"
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


async def create_tex_sprav_price_future(percent, sprav_price, svyazka, svazkka_moex_forex=None):
    if svazkka_moex_forex == None:
        text =  [f"{await valyta_smail(percent)} •  ({percent}%){await smail_vnimanie(percent)}\n",
        f"{await link_text(svyazka)}\n"]
        return ''.join(text)
    else:
        text = [f"{await valyta_smail(percent)} •  ({percent}%){await smail_vnimanie(percent)}\n",
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
            eurrub_inv_tom = await valuta_replace_float('EURRUB', yahoo_valyata, 4)
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
            print(sp500_in)

            # print(f"forex {usdcnh_for}")
            # print('eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
            usd_rub_ru = await get_last_price(usdrub['USD000UTSTOM'])
            si_price = last_prices.get(si['si-6.24'], 1)
            # si_sprav_price = round(1000 * (usd_rub_ru * (1 + 0.16 * (await expiration_date_future(si['si-6.24'])/365))))
            percent_si_cr_usdcnh = round(si_price / last_prices.get('FUTCNY062400', 1) / 1000 / usdcnh_for * 100 -100, 3)
            si_cr_usdcnh = 'Si1_Cr1_USDCNH(for)'
            message_si_cr_usdcnh = f"{await valyta_smail(percent_si_cr_usdcnh)} •  ({percent_si_cr_usdcnh}%){await smail_vnimanie(percent_si_cr_usdcnh)}\nSi1 / CR1 / $USDCNH(for)\nSi - 1 лот | CNY - {si_price/100/last_prices.get('FUTCNY062400', 1)}лот\n\n"
            await send_signals(percent_si_cr_usdcnh, message_si_cr_usdcnh, si_cr_usdcnh)

            percent_eu_cr_eurcnh = round(last_prices.get('FUTEU0624000', 1) / last_prices.get('FUTCNY062400', 1) / 1000 / await valuta_replace_float('EURCNH', yahoo_valyata, 4) * 100 -100, 3)
            eu_cr_eurcnh = 'Eu1_Cr1_EURCNH(for)'
            message_eu_cr_eurcnh = f"{await valyta_smail(percent_eu_cr_eurcnh)} •  ({percent_eu_cr_eurcnh}%){await smail_vnimanie(percent_eu_cr_eurcnh)}\nEu1 / CR1 / $EURCNH(for)\n\n"
            await send_signals(percent_eu_cr_eurcnh, message_eu_cr_eurcnh, eu_cr_eurcnh)

            percent_eu_si_eurusd = round(last_prices.get('FUTEU0624000', 1) / si_price / await valuta_replace_float('EURUSD', yahoo_valyata, 4) * 100 -100, 3)
            eu_si_eurusd = 'Eu1_Si1_EURUSD(for)'
            message_eu_si_eurusd = f"{await valyta_smail(percent_eu_si_eurusd)} •  ({percent_eu_si_eurusd}%){await smail_vnimanie(percent_eu_si_eurusd)}\nEu1 / Si1 / $EURUSD(for)\n\n"
            await send_signals(percent_eu_si_eurusd, message_eu_si_eurusd, eu_si_eurusd)

            percent_eu_si_ed = round(last_prices.get('FUTEU0624000', 1) / si_price / last_prices.get('FUTED0624000', 1) * 100 -100, 3)
            eu_si_ed = 'Eu1_Si1_Ed1'
            message_eu_si_ed = f"{await valyta_smail(percent_eu_si_ed)} •  ({percent_eu_si_ed}%){await smail_vnimanie(percent_eu_si_ed)}\nEu1 / Si1 / $ED ️\n\n\n"
            await send_signals(percent_eu_si_ed, message_eu_si_ed, eu_si_ed)

            percent_us_tom_cn_tom_usdcnh = round(last_prices.get('BBG0013HGFT4', 1) / last_prices.get('BBG0013HRTL0', 1)/ usdcnh_for * 100 -100, 3)
            percent_eu_tom_cn_tom_eurcnh = round(eurrub_inv_tom / last_prices.get('BBG0013HRTL0', 1)/ await valuta_replace_float('EURCNH', yahoo_valyata, 4) * 100 -100, 3)
            percent_us_tom_kz_tom_usdkzt = round(last_prices.get('BBG0013HGFT4', 1) / last_prices.get('BBG0013HG026', 4)/ usdkzt_for * 100 * 100 -100, 3)
            percent_eu_tom_kz_tom_eurkzt = round(eurrub_inv_tom / last_prices.get('BBG0013HG026', 4)/ eurkzt_for * 100 * 100 -100, 3)
            percent_us_tom_try_tom_usdtry = round(last_prices.get('BBG0013HGFT4', 1) / last_prices.get('BBG0013J12N1', 4)/ usdtry_for * 100 -100, 3)
            percent_eu_tom_try_tom_eurtry = round(eurrub_inv_tom / last_prices.get('BBG0013J12N1', 4)/ eurtry_for * 100  -100, 3)
            percent_sv1_silver = round(last_prices.get('FUTSILV06240',None) / silver_in * 100  -100, 3)
            percent_gd1_gold = round(last_prices.get('FUTGOLD06240',None) / gold_in * 100  -100, 3)
            percent_na1_nasdaq = round(last_prices.get('FUTNASD06240',None) / nasdaq_in * 100  -100, 3)
            percent_sf1_sp500 = round((last_prices.get('FUTSPYF06240',None) * 10) / sp500_in * 100  -100, 3)
            percent_cn_tom_cr1 = round(last_prices.get('BBG0013HRTL0', 1) / last_prices.get('FUTCNY062400', 1) * 100  -100, 3)



            sprav_price_cr1 = await sprav_price_future(last_prices.get('BBG0013HRTL0', 1), figi='FUTCNY062400', max_percente_first_day=2.7)
            percent_sprav_price_cr1 = round(last_prices.get('FUTCNY062400', 1) / sprav_price_cr1 * 100 -100, 3)

            sprav_price_silver = await sprav_price_future(silver_in, figi='FUTSILV06240', max_percente_first_day=3.25)
            percent_sprav_price_silver = await asy_get_percent(sprav_price_silver, last_prices.get('FUTSILV06240', None) )

            sprav_price_gold = await sprav_price_future(gold_in, figi='FUTGOLD06240', max_percente_first_day=2.7)
            percent_sprav_price_gold = await asy_get_percent(sprav_price_gold, last_prices.get('FUTGOLD06240',None))
            # percent_sprav_price_gold =round(percent_sprav_price_gold -  1.3 if percent_sprav_price_gold >= 0 else percent_sprav_price_gold - -1.3, 3)

            sprav_price_nasdaq = await sprav_price_future(nasdaq_in, figi='FUTNASD06240', max_percente_first_day=1.7)
            percent_sprav_price_nasdaq = await asy_get_percent(sprav_price_nasdaq, last_prices.get('FUTNASD06240',None))

            sprav_price_sp500 = await sprav_price_future(sp500_in, figi='FUTSPYF06240', max_percente_first_day=1.9)
            percent_sprav_price_sp500 = await asy_get_percent(sprav_price_sp500, last_prices.get('FUTSPYF06240',None) * 10 )
            print(sprav_price_sp500)
            print(last_prices.get('FUTSPYF06240',None))




            link_name = '<a href="https://t.me/spread_sca">Eu1 / Cr1 / EURCNH(for)</a>'
            delitel1 = 0.1
            time_apgrade = datetime.datetime.now(moscow_tz)
            time_new = time_apgrade.strftime("%H:%M:%S")
            text_future = [
                   f"⚙️ {await podcher_text(await zirniy_text('Фьючерсы на валюту'))} 👇👇👇\n\n",
                   f"{await valyta_smail(percent_si_cr_usdcnh)} •  ({percent_si_cr_usdcnh}%){await smail_vnimanie(percent_si_cr_usdcnh)}\n{await link_text('Si1 / CR1 / USDCNH(for)')}\n" ,
                   await napravlenie_sdelok_3nogi(percent_si_cr_usdcnh, 'Si1 / CR1 / USDCNH(for)', price1=si_price, price2=last_prices.get('FUTCNY062400', 1), price3=usdcnh_for) ,
                   f"{await valyta_smail(percent_eu_cr_eurcnh)} •  ({percent_eu_cr_eurcnh}%){await smail_vnimanie(percent_eu_cr_eurcnh)}\n{await link_text('Eu1 / Cr1 / EURCNH(for)')}\n" ,
                   await napravlenie_sdelok_3nogi(percent_eu_cr_eurcnh, 'Eu1 / Cr1 / EURCNH(for)', price1=last_prices.get('FUTEU0624000', 1), price2=last_prices.get('FUTCNY062400', 1), price3=eurcnh_for),
                   f"{await valyta_smail(percent_eu_si_eurusd)} •  ({percent_eu_si_eurusd}%){await smail_vnimanie(percent_eu_si_eurusd)}\n{await link_text('Eu1 / Si1 / EURUSD(for)')}\n" ,
                   await napravlenie_sdelok_3nogi(percent_eu_si_eurusd, 'Eu1 / Si1 / EURUSD(for)', price1=last_prices.get('FUTEU0624000', 1), price2=si_price, price3=eurusd_for),
                   f"{await valyta_smail(percent_eu_si_ed)} •  ({percent_eu_si_ed}%){await smail_vnimanie(percent_eu_si_ed)}\n{await link_text('Eu1 / Si1 / ED')}\n" ,
                   await napravlenie_sdelok_3nogi(percent_eu_si_eurusd, 'Eu1 / Si1 / ED',  price1=last_prices.get('FUTEU0624000', 1), price2=si_price, price3=last_prices.get('FUTED0624000', 1) ),
                   f"{await valyta_smail(percent_sprav_price_cr1)} •  ({percent_sprav_price_cr1}%){await smail_vnimanie(percent_sprav_price_cr1)}\n" ,
                   f"{await link_text('CR1 (спр) / CR1 (real)')}\n\n" ,
                   f"CR1 (спр) -> цена справ-вая = {sprav_price_cr1}\n\n\n"]
            delitel2 = 0.1
            text_valuta = [f"🧭 Время последнего обновления:\n{time_apgrade.date()}  время: {time_new}\n\n" ,
                   f"Один знак  '❗' =  {delitel2}%\n\n",
                   f"⚙️ {await zirniy_text(await podcher_text('Валюта'))}👇👇👇\n\n" ,
                   f"{await valyta_smail(percent_us_tom_cn_tom_usdcnh)} •  ({percent_us_tom_cn_tom_usdcnh}%){await smail_vnimanie(percent_us_tom_cn_tom_usdcnh)}\n{await link_text('US_TOM / CN_TOM / SDCNH(for)')}\n" ,
                   await napravlenie_sdelok_3nogi(percent_us_tom_cn_tom_usdcnh, 'US_TOM / CN_TOM / USDCNH(for)', price1=last_prices.get('BBG0013HGFT4', 1),  price2=last_prices.get('BBG0013HRTL0', 1), price3=usdcnh_for),
                   f"{await valyta_smail(percent_eu_tom_cn_tom_eurcnh)} •  ({percent_eu_tom_cn_tom_eurcnh}%){await smail_vnimanie(percent_eu_tom_cn_tom_eurcnh)}\n{await link_text('EU_TOM / CN_TOM / EURCNH(for)')}\n",
                   await napravlenie_sdelok_3nogi(percent_eu_tom_cn_tom_eurcnh, 'EU_TOM / CN_TOM / EURCNH(for)', price1=eurrub_inv_tom,  price2=last_prices.get('BBG0013HRTL0', 1), price3=eurcnh_for),
                   f"{await valyta_smail(percent_us_tom_kz_tom_usdkzt)} •  ({percent_us_tom_kz_tom_usdkzt}%){await smail_vnimanie(percent_us_tom_kz_tom_usdkzt)}\n{await link_text('US_TOM / KZ_TOM / USDKZT(for)')}\n" ,
                   await napravlenie_sdelok_3nogi(percent_us_tom_kz_tom_usdkzt, 'US_TOM / KZ_TOM / USDKZT(for)', price1=last_prices.get('BBG0013HGFT4', 1) , price2=last_prices.get('BBG0013HG026', 4), price3=usdkzt_for),
                   f"{await valyta_smail(percent_eu_tom_kz_tom_eurkzt)} •  ({percent_eu_tom_kz_tom_eurkzt}%){await smail_vnimanie(percent_eu_tom_kz_tom_eurkzt)}\n{await link_text('EU_TOM / KZ_TOM / EURKZT(for)')}\n" ,
                   await napravlenie_sdelok_3nogi(percent_eu_tom_kz_tom_eurkzt, 'EU_TOM / KZ_TOM / EURKZT(for)', price1=eurrub_inv_tom,  price2=last_prices.get('BBG0013HG026', 4), price3=eurkzt_for),
                   f"{await valyta_smail(percent_us_tom_try_tom_usdtry)} •  ({percent_us_tom_try_tom_usdtry}%){await smail_vnimanie(percent_us_tom_try_tom_usdtry)}\n{await link_text('US_TOM / TRY_TOM / USDTRY(for)')}\n" ,
                   await napravlenie_sdelok_3nogi(percent_us_tom_try_tom_usdtry, 'US_TOM / TRY_TOM / USDTRY(for)', price1=last_prices.get('BBG0013HGFT4', 1), price2=last_prices.get('BBG0013J12N1', 4), price3=usdtry_for),
                   f"{await valyta_smail(percent_eu_tom_try_tom_eurtry)} •  ({percent_eu_tom_try_tom_eurtry}%){await smail_vnimanie(percent_eu_tom_try_tom_eurtry)}\n{await link_text('EU_TOM / TRY_TOM / EURTRY(for)')}\n",
                   await napravlenie_sdelok_3nogi(percent_eu_tom_try_tom_eurtry, 'EU_TOM / TRY_TOM / EURTRY(for)', price1=eurrub_inv_tom, price2=last_prices.get('BBG0013J12N1', 4), price3=eurtry_for),
                   f"\n\n"
                           ]

                   # f"Акции\n" \

            time_apgrade1 = datetime.datetime.now(moscow_tz)
            time_new1 = time_apgrade.strftime("%H:%M:%S")
            delitel = 0.1
            silver_text = await create_tex_sprav_price_future(percent_sprav_price_silver, sprav_price_silver, 'SV1 (real) / SV1 (спр)')
            silver_text += await napravlenie_sdelok_2nogi(percent_sprav_price_silver, 'SV1 / XAGUSD(for)', price1=last_prices.get('FUTSILV06240', None), price2=silver_in, lot1=lotnost_forex['silver']['moex'], lot2=lotnost_forex['silver']['forex'])
            gold_text = await create_tex_sprav_price_future(percent_sprav_price_gold, sprav_price_gold, 'GOLD1 (real) / GOLD1 (спр)')
            gold_text += await napravlenie_sdelok_2nogi(percent_sprav_price_gold, 'GOLD1 / XAUUSD(for)', price1=last_prices.get('FUTGOLD06240',None), price2=gold_in, lot1=lotnost_forex['gold']['moex'], lot2=lotnost_forex['gold']['forex'])
            nasdaq_text = await create_tex_sprav_price_future(percent_sprav_price_nasdaq, sprav_price_nasdaq, 'NA1! (real) / NA1! (спр)')
            nasdaq_text += await napravlenie_sdelok_2nogi(percent_sprav_price_nasdaq, 'NA1 / NDXUSD(for)', price1=last_prices.get('FUTNASD06240',None), price2=nasdaq_in, lot1=lotnost_forex['nasdaq']['moex'], lot2=lotnost_forex['nasdaq']['forex'])
            sp500_text = await create_tex_sprav_price_future(percent_sprav_price_sp500, sprav_price_sp500, 'SF!! (real) / SF1! (спр)')
            sp500_text += await napravlenie_sdelok_2nogi(percent_sprav_price_sp500, 'SF1 / SPXUSD(for)', price1=last_prices.get('FUTSPYF06240',None) , price2=sp500_in, lot1=lotnost_forex['sp500']['moex'], lot2=lotnost_forex['sp500']['forex'])
            list_text = [f"🧭 Время последнего обновления:\n{time_apgrade.date()}  время: {time_new1}\n\n",
                         f"Один знак  '❗' =  {delitel}%\n\n",
                         f"⚙️ {await zirniy_text(await podcher_text('Фьючерсы на металлы, индексы '))}\n\n",
                         silver_text,  gold_text, nasdaq_text, sp500_text]
            finali_message = ''.join(list_text)


            fut_sb = {"SRM4" : "FUTSBRF06240"}
            fut_sbp = {"SPM4" : "FUTSBPR06240"}
            name = ['SBRF', 'SBPR']
            if time_10x23_50:
                time_new2 = time_apgrade.strftime("%H:%M:%S")
                delitel = 0.1
                tatn_tex = await arbitrage_parniy_akcii('TATN', 'TATNP')
                sber_text = await arbitrage_parniy_akcii('SBER', 'SBERP')
                list_akcii = [f"\n⚙️ {await zirniy_text(await podcher_text('Акции'))}\n\n",
                              tatn_tex, sber_text]
                finali_message_akcii = ''.join(list_akcii)
                finali_message = finali_message + finali_message_akcii

            # if time_10x23_50:
            #     text = text + await arbitrage_parniy_futures(fut_sb["SRM4"], fut_sbp["SPM4"], name=name)
            #     text = text + '\n' + await arbtrage_future_akcii()

            # finali_message1 = ''.join(text_future)
            finali_message2 = ''.join(text_valuta + text_future)
            # <b>Жирный</b>
            # <i>Курсив</i>
            # <s>Зачеркнутый</s>
            # <u>Подчеркнутый</u>
            # <code>Копировать</code>
            # <href='Сылка'>Курсив</a>
            #<tg-spoiler>Скрытый</tg-spoiler>
            # s = await bot.edit_message_text(finali_message1, chat_id=chenal_id, message_id=last_messa3_id, parse_mode='HTML')
            s1 = await bot.edit_message_text(finali_message2, chat_id=chenal_id, message_id=last_messa2_id, parse_mode='HTML')
            s2 = await bot.edit_message_text(finali_message, chat_id=chenal_id, message_id=last_messa_id, parse_mode='HTML')

    except Exception as e:
        error_message = traceback.format_exc()
        print(f'Произошла ошибка функции valuta_vtelegram:\n{error_message}')
        print(e)

async def start_cicl_5s():
    coun = 0
    try:
        while True:
            await valuta_vtelegram()
            await asyncio.sleep(5)
            await get_last_prices_dict()
            print(dict_interva)
    except Exception as e:
        error_message = traceback.format_exc()
        print(f'Произошла ошибка функции valuta_vtelegram:\n{error_message}')
        print(e)
        await asyncio.sleep(5)
        await start_cicl_5s()


list_task = [start_cicl_5s(), dict_yahoo_valuta()]

async def main():
    # Запуск периодических задач в фоновом режиме
    await asyncio.gather(*list_task)

    # Запуск бота
    await dp.start_polling()



if __name__ == '__main__':
    client2.start()
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