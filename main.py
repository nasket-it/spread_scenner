import traceback
from yahoo_finance import  yahoo_valyata, dict_yahoo_valuta
from telethon.sync import TelegramClient, events
from info_figi_ti import *
from secrete import Token
import asyncio
from tinkoff_get_func import (
    time_range, get_last_price, expiration_date_future,
    arbtrage_future_akcii, last_prices, get_last_prices_dict)
from Config import InfoTiker, Config, Chenal
from aiogram import Bot, Dispatcher, types, executor
from datetime import *
import datetime



client2 = TelegramClient(Token.phone2, Token.api_id2, Token.api_hash2)

API_TOKEN = Token.bot_token


# Создаем объекты бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
# Создаем объекты бота и диспетчера @ask_signals_bot
bot_ask = Bot(token=Token.bot_token2)
dp_bot_ask = Dispatcher(bot_ask)
# Создаем объекты бота и диспетчера @ask_signals_bot
bot_gpt = Bot(token=Token.bot_token3)
dp_bot_gpt = Dispatcher(bot_gpt)


account = ['-1001892817733','-1001857334624']
api_id = Token.api_id  # задаем API
api_hash = Token.api_hash  # задаем HASH
phone = Token.phone







# await asyncio.sleep(5)

async def valyta_smail(percent):
    if percent < 0:
        return '📕'
    if percent > 0:
        return '📗'
    if percent == 0:
        return "📘"

async def smail_vnimanie(percent):
    percent_namber = int(percent // 0.1) if percent > 0 else int(percent * -1  // 0.1)
    if percent_namber <= 6:
        return int(percent // 0.1) *'❗️'
    else:
        return 6 * '❗' + '+'

async def valuta_replace_float(valut_para, dict, kol_znakov):
    price = dict['valuta'][valut_para][0].replace('.', '') if valut_para in ['gold_fut', 'gold_spot'] else dict['valuta'][valut_para][0]
    return round(float(price.replace(',', '.')), kol_znakov)

async def percent(num_100, num_rezultat):
    return round(num_100 / num_rezultat * 100 - 100, 2)



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
            rubli = round(tiker1_last_price - tiker2_last_price, 1)
            punkti = round(rubli / Config.info[tiker1]['minstep'])
            punkti = punkti if punkti > 0 else punkti * -1
            percents = await percent(tiker1_last_price, tiker2_last_price)

            return f"{await valyta_smail(percents)} • {tiker1} / {tiker2}{await smail_vnimanie(percents)}\n{punkti}п | {rubli}р | {percents}%\n\n" \




async def valuta_vtelegram():
    global yahoo_valyata
    current_time = datetime.datetime.now().time()
    time_10x23_50 = await time_range('09:50:00', '23:50:00', current_time)
    chenal_id = {'Сверчок': -1001854614186}
    last_message = await client2.get_messages(chenal_id['Сверчок'], limit=2)
    last_messa_id = last_message[0].id
    last_messa2_id = last_message[1].id
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

            print(f"forex {usdcnh_for}")
            print('eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
            usd_rub_ru = await get_last_price(usdrub['USD000UTSTOM'])
            si_price = last_prices.get(si['si-6.24'], 1)
            # si_sprav_price = round(1000 * (usd_rub_ru * (1 + 0.16 * (await expiration_date_future(si['si-6.24'])/365))))
            percent_si_cr_usdcnh = round(si_price / last_prices.get('FUTCNY062400', 1) / 1000 / usdcnh_for * 100 -100, 3)
            percent_eu_cr_eurcnh = round(last_prices.get('FUTEU0624000', 1) / last_prices.get('FUTCNY062400', 1) / 1000 / await valuta_replace_float('EURCNH', yahoo_valyata, 4) * 100 -100, 3)
            percent_eu_si_eurusd = round(last_prices.get('FUTEU0624000', 1) / si_price / await valuta_replace_float('EURUSD', yahoo_valyata, 4) * 100 -100, 3)
            percent_eu_si_ed = round(last_prices.get('FUTEU0624000', 1) / si_price / last_prices.get('FUTED0624000', 1) * 100 -100, 3)
            percent_us_tom_cn_tom_usdcnh = round(last_prices.get('BBG0013HGFT4', 1) / last_prices.get('BBG0013HRTL0', 1)/ usdcnh_for * 100 -100, 3)
            percent_eu_tom_cn_tom_eurcnh = round(eurrub_inv_tom / last_prices.get('BBG0013HRTL0', 1)/ await valuta_replace_float('EURCNH', yahoo_valyata, 4) * 100 -100, 3)
            percent_us_tom_kz_tom_usdkzt = round(last_prices.get('BBG0013HGFT4', 1) / last_prices.get('BBG0013HG026', 4)/ usdkzt_for * 100 * 100 -100, 3)
            percent_eu_tom_kz_tom_eurkzt = round(eurrub_inv_tom / last_prices.get('BBG0013HG026', 4)/ eurkzt_for * 100 * 100 -100, 3)
            percent_us_tom_try_tom_usdtry = round(last_prices.get('BBG0013HGFT4', 1) / last_prices.get('BBG0013J12N1', 4)/ usdtry_for * 100 -100, 2)
            percent_eu_tom_try_tom_eurtry = round(eurrub_inv_tom / last_prices.get('BBG0013J12N1', 4)/ eurtry_for * 100  -100, 2)
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
            time_apgrade = datetime.datetime.now()
            time_new = time_apgrade.strftime("%H:%M:%S")
            text = f"🧭 Время последнего обновления:\n{time_apgrade.date()}  время: {time_new}\n\n" \
                   f"Фьючерсы на валюту\n" \
                   f"{await valyta_smail(percent_si_cr_usdcnh)} •  ({percent_si_cr_usdcnh}%){await smail_vnimanie(percent_si_cr_usdcnh)}\nSi1 / CR1 / $USDCNH(for)\n\n" \
                   f"{await valyta_smail(percent_eu_cr_eurcnh)} •  ({percent_eu_cr_eurcnh}%){await smail_vnimanie(percent_eu_cr_eurcnh)}\nEu1 / CR1 / $EURCNH(for)\n\n" \
                   f"{await valyta_smail(percent_eu_si_eurusd)} •  ({percent_eu_si_eurusd}%){await smail_vnimanie(percent_eu_si_eurusd)}\nEu1 / Si1 / $EURUSD(for)\n\n" \
                   f"{await valyta_smail(percent_eu_si_ed)} •  ({percent_eu_si_ed}%){await smail_vnimanie(percent_eu_si_ed)}\nEu1 / Si1 / $ED ️\n\n\n" \
                   f"Валюта\n" \
                   f"{await valyta_smail(percent_us_tom_cn_tom_usdcnh)} •  ({percent_us_tom_cn_tom_usdcnh}%){await smail_vnimanie(percent_us_tom_cn_tom_usdcnh)}\nUS_TOM / CN_TOM / $USDCNH(for)\n\n" \
                   f"{await valyta_smail(percent_eu_tom_cn_tom_eurcnh)} •  ({percent_eu_tom_cn_tom_eurcnh}%){await smail_vnimanie(percent_eu_tom_cn_tom_eurcnh)}\nEU_TOM / CN_TOM / $EURCNH(for)\n\n" \
                   f"{await valyta_smail(percent_us_tom_kz_tom_usdkzt)} •  ({percent_us_tom_kz_tom_usdkzt}%){await smail_vnimanie(percent_us_tom_kz_tom_usdkzt)}\nUS_TOM / KZ_TOM / $USDKZT(for)\n\n" \
                   f"{await valyta_smail(percent_eu_tom_kz_tom_eurkzt)} •  ({percent_eu_tom_kz_tom_eurkzt}%){await smail_vnimanie(percent_eu_tom_kz_tom_eurkzt)}\nEU_TOM / KZ_TOM / $EURKZT(for)\n\n" \
                   f"{await valyta_smail(percent_us_tom_try_tom_usdtry)} •  ({percent_us_tom_try_tom_usdtry}%){await smail_vnimanie(percent_us_tom_try_tom_usdtry)}\nUS_TOM / TRY_TOM / $USDTRY(for)\n\n" \
                   f"{await valyta_smail(percent_eu_tom_try_tom_eurtry)} •  ({percent_eu_tom_try_tom_eurtry}%){await smail_vnimanie(percent_eu_tom_try_tom_eurtry)}\nEU_TOM / TRY_TOM / $EURTRY(for)\n\n\n" \
                   f"Акции\n" \



            fut_sb = {"SRM4" : "FUTSBRF06240"}
            fut_sbp = {"SPM4" : "FUTSBPR06240"}
            name = ['SBRF', 'SBPR']
            if time_10x23_50:
                text = text + await arbitrage_parniy_akcii('TATN', 'TATNP')
                text = text + await arbitrage_parniy_akcii('SBER', 'SBERP')
            # if time_10x23_50:
            #     text = text + await arbitrage_parniy_futures(fut_sb["SRM4"], fut_sbp["SPM4"], name=name)
            #     text = text + '\n' + await arbtrage_future_akcii()

            s = await bot.edit_message_text(text, chat_id=chenal_id['Сверчок'], message_id=last_messa2_id)

        print('valuta_vtelegram() - jhjhjjgjhgjhgf')
    except Exception as e:
        error_message = traceback.format_exc()
        print(f'Произошла ошибка функции valuta_vtelegram:\n{error_message}')
        print(e)

# async def test2():

async def start_cicl_5s():
    coun = 0
    try:
        while True:
            # await get_last_price()
            await valuta_vtelegram()
            await asyncio.sleep(5)
            await get_last_prices_dict()
            print(f"Валюта - {last_prices['BBG0013HGFT4']}   -  {last_prices['BBG0013HRTL0']}  ")
            # print(orderbooks_reltime[Info_figi.tiker_figi['SBER']])
            print(f"gggggggggggggggggggggggggggggggggggggg")
    except Exception as e:
        error_message = traceback.format_exc()
        print(f'Произошла ошибка функции valuta_vtelegram:\n{error_message}')
        print(e)
        await asyncio.sleep(5)
        await start_cicl_5s()

async def test():
    while True:
        print(344)
        await asyncio.sleep(1)



list_task = [start_cicl_5s(), test(), dict_yahoo_valuta()]

async def main():
    # Запуск периодических задач в фоновом режиме
    await asyncio.gather(*list_task)

    # Запуск бота
    await dp.start_polling()



if __name__ == '__main__':
    client2.start()
    # executor.start_polling(dp)
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