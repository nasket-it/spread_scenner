import math
from time import timezone, time
from secrete import Token
from pytz import timezone
from tinkoff import invest
from tinkoff.invest import (
    AsyncClient,
    CandleInstrument,
    MarketDataRequest,
    SubscribeCandlesRequest,
    SubscriptionAction,
    SubscriptionInterval,
SubscribeOrderBookRequest,
OrderBookInstrument,
Order,
Client,
PostOrderRequest,
Quotation,
PositionsRequest
)
from tinkoff.invest import Client, SecurityTradingStatus, OrderType, OrderDirection, Quotation,\
    GetOrderBookRequest, PositionsRequest, InstrumentRequest, InstrumentType, InstrumentIdType, InstrumentStatus, CandleInterval
from tinkoff.invest.services import InstrumentsService
from tinkoff.invest.utils import quotation_to_decimal
from info_figi_ti import Info_figi
from datetime import datetime, timedelta
from tinkoff.invest.utils import now
import asyncio
import os
from datetime import timedelta
from tinkoff.invest import AsyncClient, CandleInterval
from tinkoff.invest.utils import now

TOKEN = Token.tinkov_token_slv
acaunt_id = '2028504625'
future_all_info ={}
orderbooks_reltime = {}

price_plus = {i : [] for i in  Info_figi.figi_tiker}
valuta_fut = {'USDRUBF': {'figi': 'FUTUSDRUBF00', 'name': 'USDRUBF Доллар - Рубль'},
                  'SiH5': {'figi': 'FUTSI0325000', 'name': 'Si-3.25 Курс доллар - рубль'},
                  'SiU4': {'figi': 'FUTSI0924000', 'name': 'Si-9.24 Курс доллар - рубль'},
                  'SiM5': {'figi': 'FUTSI0625000', 'name': 'Si-6.25 Курс доллар - рубль'},
                  'SiZ4': {'figi': 'FUTSI1224000', 'name': 'Si-12.24 Курс доллар - рубль'},
                  'EDM4': {'figi': 'FUTED0624000', 'name': 'ED-6.24 Курс евро - доллар'},
                  'SiM4': {'figi': 'FUTSI0624000', 'name': 'Si-6.24 Курс доллар - рубль'},
                  'GUH4': {'figi': 'FUTGBPU03240', 'name': 'GBPU-3.24 Курс Фунт стерлингов - Доллар'},
                  'JPZ3': {'figi': 'FUTUJPY12230', 'name': 'UJPY-12.23 Курс доллар США - Японская йена'},
                  'GUZ3': {'figi': 'FUTGBPU12230', 'name': 'GBPU-12.23 Курс Фунт стерлингов - Доллар'},
                  'EDZ3': {'figi': 'FUTED1223000', 'name': 'ED-12.23 Курс евро-доллар'},
                  'EDH4': {'figi': 'FUTED0324000', 'name': 'ED-3.24 Курс евро-доллар'},
                  'CAZ3': {'figi': 'FUTUCAD12230', 'name': 'UCAD-12.23 Курс Доллар США - Канадский доллар'},
                  'SiH4': {'figi': 'FUTSI0324000', 'name': 'Si-3.24 Курс доллар - рубль'},
                  'UCM4': {'figi': 'FUTUCNY06240', 'name': 'UCNY-6.24 Курс доллар США - Юань'},
                  'AUZ3': {'figi': 'FUTAUDU12230', 'name': 'AUDU-12.23 Курс Австралийский доллар - Доллар США'},
                  'SiZ3': {'figi': 'FUTSI1223000', 'name': 'Si-12.23 Курс доллар - рубль'},
                  'SiU5': {'figi': 'FUTSI0925000', 'name': 'Si-9.25 Курс доллар - рубль'},
                  'JPH4': {'figi': 'FUTUJPY03240', 'name': 'UJPY-3.24 Курс доллар США - Японская йена'},
                  'UCH4': {'figi': 'FUTUCNY03240', 'name': 'UCNY-3.24 Курс доллар США - Юань'},
                  'AUH4': {'figi': 'FUTAUDU03240', 'name': 'AUDU-3.24 Курс Австралийский доллар - Доллар США'},
                  'CFH4': {'figi': 'FUTUCHF03240', 'name': 'UCHF-3.24 Курс доллар США - Швейцарский франк'},
                  'CAH4': {'figi': 'FUTUCAD03240', 'name': 'UCAD-3.24 Курс Доллар США - Канадский доллар'},
                  'UCU4': {'figi': 'FUTUCNY09240', 'name': 'UCNY-9.24 Курс доллар США - Юань'},
                  'CFZ3': {'figi': 'FUTUCHF12230', 'name': 'UCHF-12.23 Курс доллар США - Швейцарский франк'},
                  'UCZ3': {'figi': 'FUTUCNY12230', 'name': 'UCNY-12.23 Курс доллар США - Юань'}}

futures = {'SRM4': 'FUTSBRF06240', 'VKU4': 'FUTVKCO09240', 'NGQ4': 'FUTNG0824000', 'RNM5': 'FUTROSN06250',
           'BRZ4': 'FUTBR1224000', 'UTM4': 'FUTUKZT06240', 'EDU4': 'FUTED0924000', 'MTM4': 'FUTMTSI06240',
           'MGH4': 'FUTMAGN03240', 'CRH4': 'FUTCNY032400', 'RIH5': 'FUTRTS032500', 'GZH4': 'FUTGAZR03240',
           'IRH4': 'FUTIRAO03240', 'HSZ4': 'FUTHANG12240', 'N2H4': 'FUTNIKK03240', 'NGM4': 'FUTNG0624000',
           'VIJ4': 'FUTRVI042400', 'GDM4': 'FUTGOLD06240', 'RIH4': 'FUTRTS032400', 'AEH4': 'FUTAED032400',
           'CNYRUBF': 'FUTCNYRUBF00', 'NKH4': 'FUTNOTK03240', 'GZU4': 'FUTGAZR09240', 'GKH4': 'FUTGMKN03240',
           'MXH4': 'FUTMIX032400', 'UCZ4': 'FUTUCNY12240', 'W4M4': 'FUTWHEA06240', 'AFM4': 'FUTAFLT06240',
           'LKM4': 'FUTLKOH06240', 'PHH4': 'FUTPHOR03240', 'W4X4': 'FUTWHEAT1124', 'NGK4': 'FUTNG0524000',
           'CRZ4': 'FUTCNY122400', 'RBM4': 'FUTRGBI06240', 'CoJ4': 'FUTCO0424000', 'SPH4': 'FUTSBPR03240',
           'W4Z4': 'FUTWHEAT1224', 'GZM6': 'FUTGAZR06260', 'EURRUBF': 'FUTEURRUBF00', 'GDZ4': 'FUTGOLD12240',
           'MCH4': 'FUTMTLR03240', 'CoH4': 'FUTCO0324000', 'W4J4': 'FUTWHEAT0424', 'SuH4': 'FUTSUGAR0324',
           'GZZ4': 'FUTGAZR12240', 'NAU4': 'FUTNASD09240', 'AEM4': 'FUTAED062400', 'SZH4': 'FUTSGZH03240',
           'OGH4': 'FUTOGI032400', 'BRK4': 'FUTBR0524000', 'RMH4': 'FUTRTSM03240', 'EuH4': 'FUTEU0324000',
           'ISM4': 'FUTISKJ06240', 'CHM4': 'FUTCHMF06240', 'BNU4': 'FUTBANE09240', 'RNM4': 'FUTROSN06240',
           'W4F5': 'FUTWHEAT0125', 'SXZ4': 'FUTSTOX12240', 'NMM4': 'FUTNLMK06240', 'EuU4': 'FUTEU0924000',
           'PDH4': 'FUTPLD032400', 'SNH4': 'FUTSNGR03240', 'NAZ4': 'FUTNASD12240', 'WUH4': 'FUTWUSH03240',
           'NAM4': 'FUTNASD06240', 'MMM5': 'FUTMXI062500', 'KZZ4': 'FUTKZT122400', 'RNH4': 'FUTROSN03240',
           'RNZ5': 'FUTROSN12250', 'BRF5': 'FUTBR0125000', 'N2M4': 'FUTNIKK06240', 'MXM4': 'FUTMIX062400',
           'BNM4': 'FUTBANE06240', 'PSM4': 'FUTPOSI06240', 'KZM4': 'FUTKZT062400', 'S0H4': 'FUTSOFL03240',
           'SiU4': 'FUTSI0924000', 'CRU4': 'FUTCNY092400', 'CFH4': 'FUTUCHF03240', 'SFH4': 'FUTSPYF03240',
           'MMM6': 'FUTMXI062600', 'BSM4': 'FUTBSPB06240', 'PZM4': 'FUTPLZL06240', 'CMM4': 'FUTCBOM06240',
           'FLU4': 'FUTFLOT09240', 'SuN4': 'FUTSUGAR0724', 'BEZ4': 'FUTBELU12240', 'GUM4': 'FUTGBPU06240',
           'BNZ4': 'FUTBANE12240', 'RNU5': 'FUTROSN09250', 'SGH4': 'FUTSNGP03240', 'NMH4': 'FUTNLMK03240',
           'FNM4': 'FUTFNI062400', 'CHH4': 'FUTCHMF03240', 'GLU4': 'FUTGL0924000', 'SPM4': 'FUTSBPR06240',
           'VBH4': 'FUTVTBR03240', 'MVU4': 'FUTMVID09240', 'MTH4': 'FUTMTSI03240', 'HKH4': 'FUTHKD032400',
           'SSM4': 'FUTSMLT06240', 'AFU4': 'FUTAFLT09240', 'SRU4': 'FUTSBRF09240', 'AUM4': 'FUTAUDU06240',
           'WUZ4': 'FUTWUSH12240', 'EuH5': 'FUTEU0325000', 'RNM6': 'FUTROSN06260', 'MEM4': 'FUTMOEX06240',
           'RMU4': 'FUTRTSM09240', 'FSH4': 'FUTFEES03240', 'GZM5': 'FUTGAZR06250', 'TYZ4': 'FUTTRY122400',
           'AEU4': 'FUTAED092400', 'PTH4': 'FUTPLT032400', 'HOM4': 'FUTHOME06240', 'ALH4': 'FUTALRS03240',
           'RIM5': 'FUTRTS062500', 'ASM4': 'FUTASTR06240', 'VIH4': 'FUTRVI032400', 'N2U4': 'FUTNIKK09240',
           'BRJ4': 'FUTBR0424000', 'AUH4': 'FUTAUDU03240', 'NlJ4': 'FUTNL0424000', 'BRU4': 'FUTBR0924000',
           'POH4': 'FUTPOLY03240', 'CSM4': 'FUTCNI062400', 'GLM4': 'FUTGL0624000', 'CRM5': 'FUTCNY062500',
           'SiU5': 'FUTSI0925000', 'PTM4': 'FUTPLT062400', 'W4G5': 'FUTWHEAT0225', 'SFM4': 'FUTSPYF06240',
           'RNZ4': 'FUTROSN12240', 'HYM4': 'FUTHYDR06240', 'SSH4': 'FUTSMLT03240', 'WUM4': 'FUTWUSH06240',
           'KZH4': 'FUTKZT032400', 'FVH4': 'FUTFIVE03240', 'MVZ4': 'FUTMVID12240', 'RNU4': 'FUTROSN09240',
           'KMU4': 'FUTKMAZ09240', 'MMZ6': 'FUTMXI122600', 'NGJ4': 'FUTNG0424000', 'JPM4': 'FUTUJPY06240',
           'GLZ4': 'FUTGL1224000', 'CoK4': 'FUTCO0524000', 'ARU4': 'FUTAMD092400', 'SuQ4': 'FUTSUGAR0824',
           'MVH4': 'FUTMVID03240', 'CRH5': 'FUTCNY032500', 'ALU4': 'FUTALRS09240', 'FLZ4': 'FUTFLOT12240',
           'BEM4': 'FUTBELU06240', 'W4K4': 'FUTWHEAT0524', 'SuJ4': 'FUTSUGAR0424', 'PZH4': 'FUTPLZL03240',
           'SNM4': 'FUTSNGR06240', 'EDM4': 'FUTED0624000', 'EuZ4': 'FUTEU1224000', 'GKM4': 'FUTGMKN06240',
           'NlH4': 'FUTNL0324000', 'RNH6': 'FUTROSN03260', 'GLDRUBF': 'FUTGLDRUBF00', 'SiM4': 'FUTSI0624000',
           'TNU4': 'FUTTRNF09240', 'OZH4': 'FUTOZON03240', 'RIZ4': 'FUTRTS122400', 'MMH4': 'FUTMXI032400',
           'VBU4': 'FUTVTBR09240', 'NGN4': 'FUTNG0724000', 'HOU4': 'FUTHOME09240', 'MEH4': 'FUTMOEX03240',
           'MMU5': 'FUTMXI092500', 'GDH4': 'FUTGOLD03240', 'PIM4': 'FUTPIKK06240', 'RIU5': 'FUTRTS092500',
           'MTU4': 'FUTMTSI09240', 'VBM4': 'FUTVTBR06240', 'GZZ5': 'FUTGAZR12250', 'UCU4': 'FUTUCNY09240',
           'SFU4': 'FUTSPYF09240', 'AKM4': 'FUTAFKS06240', 'RNH5': 'FUTROSN03250', 'SiH5': 'FUTSI0325000',
           'RTH4': 'FUTRTKM03240', 'SVU4': 'FUTSILV09240', 'SVH4': 'FUTSILV03240', 'SXM4': 'FUTSTOX06240',
           'SAN4': 'FUTSUGR07240', 'PHM4': 'FUTPHOR06240', 'I2U4': 'FUTINR092400', 'RLM4': 'FUTRUAL06240',
           'PDU4': 'FUTPLD092400', 'FLH4': 'FUTFLOT03240', 'CAH4': 'FUTUCAD03240', 'MMZ7': 'FUTMXI122700',
           'BEH4': 'FUTBELU03240', 'W4Q4': 'FUTWHEAT0824', 'AEZ4': 'FUTAED122400', 'TTM4': 'FUTTATN06240',
           'S0M4': 'FUTSOFL06240', 'DXH4': 'FUTDAX032400', 'MMZ5': 'FUTMXI122500', 'GZH6': 'FUTGAZR03260',
           'WUU4': 'FUTWUSH09240', 'SAK4': 'FUTSUGR05240', 'CMU4': 'FUTCBOM09240', 'SVM4': 'FUTSILV06240',
           'HSH4': 'FUTHANG03240', 'UCH4': 'FUTUCNY03240', 'KMZ4': 'FUTKMAZ12240', 'SiZ4': 'FUTSI1224000',
           'GLH4': 'FUTGL0324000', 'PTU4': 'FUTPLT092400', 'POM4': 'FUTPOLY06240', 'SiM5': 'FUTSI0625000',
           'SuK4': 'FUTSUGAR0524', 'BRQ4': 'FUTBR0824000', 'MXU4': 'FUTMIX092400', 'MMZ4': 'FUTMXI122400',
           'DXZ4': 'FUTDAX122400', 'HOH4': 'FUTHOME03240', 'I2M4': 'FUTINR062400', 'CRM4': 'FUTCNY062400',
           'AFH4': 'FUTAFLT03240', 'PIH4': 'FUTPIKK03240', 'SiH4': 'FUTSI0324000', 'RMM4': 'FUTRTSM06240',
           'TYU4': 'FUTTRY092400', 'RBU4': 'FUTRGBI09240', 'LKZ4': 'FUTLKOH12240', 'W4H4': 'FUTWHEA03240',
           'IMOEXF': 'FUTIMOEXF000', 'SXH4': 'FUTSTOX03240', 'VKZ4': 'FUTVKCO12240', 'SiZ5': 'FUTSI1225000',
           'VKM4': 'FUTVKCO06240', 'SRH4': 'FUTSBRF03240', 'BYH4': 'FUTBYN032400', 'JPH4': 'FUTUJPY03240',
           'CAM4': 'FUTUCAD06240', 'FLM4': 'FUTFLOT06240', 'MNH4': 'FUTMGNT03240', 'FSM4': 'FUTFEES06240',
           'KMH4': 'FUTKMAZ03240', 'USDRUBF': 'FUTUSDRUBF00', 'NMU4': 'FUTNLMK09240', 'BSU4': 'FUTBSPB09240',
           'W4N4': 'FUTWHEAT0724', 'HYH4': 'FUTHYDR03240', 'MAH4': 'FUTMMI032400', 'BRN4': 'FUTBR0724000',
           'YNH4': 'FUTYNDF03240', 'ASH4': 'FUTASTR03240', 'I2Z4': 'FUTINR122400', 'SZZ4': 'FUTSGZH12240',
           'UCM4': 'FUTUCNY06240', 'MMH5': 'FUTMXI032500', 'SOH4': 'FUTSIBN03240', 'GDU4': 'FUTGOLD09240',
           'ARH4': 'FUTAMD032400', 'TNM4': 'FUTTRNF06240', 'NGH4': 'FUTNG0324000', 'MMU6': 'FUTMXI092600',
           'DXM4': 'FUTDAX062400', 'ARZ4': 'FUTAMD122400', 'NlK4': 'FUTNL0524000', 'I2H4': 'FUTINR032400',
           'BYM4': 'FUTBYN062400', 'FNH4': 'FUTFNI032400', 'OGM4': 'FUTOGI062400', 'SGM4': 'FUTSNGP06240',
           'EDH4': 'FUTED0324000', 'PDM4': 'FUTPLD062400', 'MMU4': 'FUTMXI092400', 'CSH4': 'FUTCNI032400',
           'N2Z4': 'FUTNIKK12240', 'EuM5': 'FUTEU0625000', 'ALM4': 'FUTALRS06240', 'RMZ4': 'FUTRTSM12240',
           'NAH4': 'FUTNASD03240', 'LKH4': 'FUTLKOH03240', 'IRM4': 'FUTIRAO06240', 'BRV4': 'FUTBR1024000',
           'PSH4': 'FUTPOSI03240', 'MGM4': 'FUTMAGN06240', 'TYH4': 'FUTTRY032400', 'MMH6': 'FUTMXI032600',
           'RTM4': 'FUTRTKM06240', 'MVM4': 'FUTMVID06240', 'BSZ4': 'FUTBSPB12240', 'GZU5': 'FUTGAZR09250',
           'MCM4': 'FUTMTLR06240', 'SZM4': 'FUTSGZH06240', 'BRX4': 'FUTBR1124000', 'BEU4': 'FUTBELU09240',
           'BNH4': 'FUTBANE03240', 'BSH4': 'FUTBSPB03240', 'AKH4': 'FUTAFKS03240', 'DXU4': 'FUTDAX092400',
           'NKM4': 'FUTNOTK06240', 'HKZ4': 'FUTHKD122400', 'GZM4': 'FUTGAZR06240', 'SZU4': 'FUTSGZH09240',
           'TTU4': 'FUTTATN09240', 'LKU4': 'FUTLKOH09240', 'GUH4': 'FUTGBPU03240', 'RIM4': 'FUTRTS062400',
           'SOM4': 'FUTSIBN06240', 'CFM4': 'FUTUCHF06240', 'ARM4': 'FUTAMD062400', 'BRM4': 'FUTBR0624000',
           'TYM4': 'FUTTRY062400', 'SXU4': 'FUTSTOX09240', 'MAM4': 'FUTMMI062400', 'CMH4': 'FUTCBOM03240',
           'HKM4': 'FUTHKD062400', 'MNU4': 'FUTMGNT09240', 'UTH4': 'FUTUKZT03240', 'MXZ4': 'FUTMIX122400',
           'HKU4': 'FUTHKD092400', 'MNM4': 'FUTMGNT06240', 'W4U4': 'FUTWHEAT0924', 'SRZ4': 'FUTSBRF12240',
           'MMH7': 'FUTMXI032700', 'SVZ4': 'FUTSILV12240', 'RLH4': 'FUTRUAL03240', 'RIU4': 'FUTRTS092400',
           'ISH4': 'FUTISKJ03240', 'BRG5': 'FUTBR0225000', 'EuM4': 'FUTEU0624000', 'HSU4': 'FUTHANG09240',
           'VKH4': 'FUTVKCO03240', 'W4V4': 'FUTWHEAT1024', 'RIZ5': 'FUTRTS122500', 'MMM4': 'FUTMXI062400',
           'GZH5': 'FUTGAZR03250', 'HSM4': 'FUTHANG06240', 'SFZ4': 'FUTSPYF12240', 'TTH4': 'FUTTATN03240',
           'KMM4': 'FUTKMAZ06240', 'CMZ4': 'FUTCBOM12240', 'KZU4': 'FUTKZT092400'}
# print(futures['EURRRUB'])
f = '456,768,890.987'
print(f.split(',')[-1])
async def time_range(start_time: str, end_time: str, current_time: time) -> bool:
    """
    Проверяет, находится ли текущее время в указанном диапазоне.

    :param start_time: Начальное время диапазона в формате "часы:минуты:секунды".
    :param end_time: Конечное время диапазона в формате "часы:минуты:секунды".
    :param current_time: Текущее время для проверки в формате datetime.time.

    :return: Возвращает True, если текущее время находится в указанном диапазоне, и False в противном случае.
    """
    start_datetime = datetime.strptime(start_time, '%H:%M:%S').time()
    end_datetime = datetime.strptime(end_time, '%H:%M:%S').time()

    return start_datetime <= current_time <= end_datetime


async def aukcion(asks_pro: dict, bids_pok: dict):
    while True:
        # Проверяем, что есть как минимум одна заявка и предложение, и что минимальная цена заявки меньше или равна максимальной цене предложения
        if not asks_pro or not bids_pok or min(asks_pro) > max(bids_pok):
            break # Выходим из цикла, если условие не выполняется

        ask_price, ask_quantity = min(asks_pro.items())
        bid_price, bid_quantity = max(bids_pok.items())

        spread = ask_price - bid_price

        if spread > 0:
            bids_pok[bid_price] = spread
        elif spread < 0:
            asks_pro[ask_price] = abs(spread)
        elif spread == 0:
            del asks_pro[ask_price]
            del bids_pok[bid_price]

        await asyncio.sleep(0) # Дать возможность выполниться другим задачам

    return bids_pok, asks_pro

async def expiration_date_future(figi):
    try:
        async with AsyncClient(TOKEN) as client:
            info = await client.instruments.future_by(id_type=InstrumentIdType(1), id=figi)
            yty = info.instrument.expiration_date.date() - datetime.now().date()
            return yty.days
    except:
        return None

async def sprav_price_future(price_base, lots=None, stavka_cb=0.16, figi=None, date_expiration=None, max_percente_first_day=None):
    stavka = stavka_cb if max_percente_first_day == None else (max_percente_first_day * 0.16) / 4
    date_exp = future_all_info[figi].expiration_date.date() if figi else date_expiration
    lot = future_all_info[figi].lot if lots == None else lots
    day_expiration = date_exp - datetime.now().date()
    return round(lot * (price_base * (1 + stavka * (day_expiration.days / 365))), 3)




def price_float_ti(price , namber_nuls=9):
    price_float = price.units + price.nano / 1e9
    return round(float(price_float), namber_nuls)

async def asy_price_float_ti(price, namber_nuls=9):
    price_float = price.units + price.nano / 1e9
    return round(float(price_float), namber_nuls)

def units(price):
    units=int(price // 1)
    return units

def get_percent(price, new_price):
    return round(((new_price - price) / price) * 100, 3) if new_price != None and price > 0 else None

async def asy_get_percent(price, new_price):
    return round(((new_price - price) / price) * 100, 3) if new_price != None and price > 0 else None

def nano(price):
    price = round(price, 9)  # Округляем число до 9 знаков после запятой
    nano = int(round((price - (price // 1)) % 1 * 1000000000))
    return nano







async def test1():
    while True:
        await asyncio.sleep(3)
        print('tinkoff_get_func')

usdrub = {'USD000UTSTOM': 'BBG0013HGFT4'}




async def get_last_price(figi):
    async with AsyncClient(TOKEN) as client:
        info = await client.market_data.get_last_trades(
            instrument_id=figi
        )
        if info.trades:
            info = info.trades[-1].price
            last_price = await asy_price_float_ti(info)
            return last_price
        else:
            return None

last_prices = {}
def get_fures_instrument():
    with Client(TOKEN) as client:
        info =  client.instruments.futures()
        for i in info.instruments:
            future_all_info[i.figi] = i
            # print(f"")
        # print(last_prices)

get_fures_instrument()
print(future_all_info['FUTCNY062400'].lot)
valyuta_dict = {}
valyuta_dict_info = {}
def get_valyuta_instrument():
    with Client(TOKEN) as client:
        info =  client.instruments.currencies()
        # print(info.instruments)
        for i in info.instruments:
            print(i.name,  i.figi)
            valyuta_dict_info[i.figi] = i
get_valyuta_instrument()
#
for i in valyuta_dict_info:
    valyuta_dict[valyuta_dict_info[i].ticker] = i
print(valyuta_dict)






#функция запроса стакана по фьючерсам
async def get_orderbook_fut_ti(tiker, bid_ask, step_in_orderbook=0):
    figi = futures[tiker]
    async with AsyncClient(TOKEN) as client:
        while True:
            ordebook = await client.market_data.get_order_book(
                figi=figi,
                depth=50
            )
            if bid_ask == 'ask': price = ordebook.asks[step_in_orderbook].price
            if bid_ask == 'bid': price = ordebook.bids[step_in_orderbook].price
            price_float = await asy_price_float_ti(price)
            if price_float:
                return price_float
            else:
                return None



def get_orderbook_ti(symbol, bid_ask, step_in_orderbook):
    with Client(TOKEN) as client:
        info = Info_figi.info[symbol]
        figi = Info_figi.tiker_figi[symbol]
        summ = '45000'
        ordebook = client.market_data.get_order_book(
            figi=figi,
            depth=50
        )
        if bid_ask == 'ask': price = ordebook.asks[step_in_orderbook].price
        if bid_ask == 'bid': price =  ordebook.bids[step_in_orderbook].price
        price_float = price_float_ti(price)
        lot = info['lot']

        lots = int(int(summ) // (lot * price_float))

        print(lots)
        # return price_float_ti(price)


async def get_last_prices_dict():
    async with AsyncClient(TOKEN) as client:
        resp = await client.market_data.get_last_prices(
            figi=[futures[i] for i in futures] + [i for i in Info_figi.figi_tiker] + [valyuta_dict[i] for i in valyuta_dict])
        for i in resp.last_prices:
            last_prices[i.figi] = await asy_price_float_ti(i.price)


async def arbtrage_future_akcii():
    message = []
    for i in future_all_info:
        if future_all_info[i].expiration_date.date().month == 6 and future_all_info[i].expiration_date.date().year == 2024 and future_all_info[i].basic_asset in Info_figi.tiker_figi:
            if last_prices.get(i, None) != None:
                lots = math.floor(future_all_info[i].basic_asset_size.units)
                price_fut = last_prices.get(i, None)
                price_akc = last_prices.get(Info_figi.tiker_figi[future_all_info[i].basic_asset], None)
                sprav_price_fut = await sprav_price_future(price_akc, future_all_info[i].expiration_date.date(), future_all_info[i].basic_asset_size.units)
                percent_fut_ot_sprav_price = await asy_get_percent(sprav_price_fut, price_fut)
                if percent_fut_ot_sprav_price >= 0.5 or percent_fut_ot_sprav_price <= -0.5:
                    text = f"       Long • ${future_all_info[i].name[0:9]} - 1 lot\n       Short • ${future_all_info[i].basic_asset} - {lots} lot" if percent_fut_ot_sprav_price < 0 else f"      Long • ${future_all_info[i].basic_asset} - {lots}1 lot\n      Short • ${future_all_info[i].name[0:9]} - 1 lot"
                    rez = f"🔸 ${future_all_info[i].name[0:9]}•{price_fut}({sprav_price_fut})" \
                          f"  {percent_fut_ot_sprav_price}%\n{text}"
                    message.append(rez)

        return '\n'.join(message)
            # print(di[i].expiration_date.date().month)
        # print(len(g))
        # info = client.instruments.currencies(
        #     instrument_status=InstrumentStatus(1)
        #     # id_type=InstrumentIdType(1),
        #     # id=figi
        # )
        # yty = info.instrument.expiration_date.date() - datetime.now().date()
        # print(yty.days/100)
        # t = {}
        # for i in info.instruments:
        #     # print(i) if i.ticker == 'CNYRUB_TOM' else None
        #     print(f"{i.ticker}:{i.figi}")
        #     t[i.ticker] = i.figi

        #     if i.exchange != 'spb_close' and i.api_trade_available_flag and i.buy_available_flag and i.otc_flag == False and i.for_qual_investor_flag == False:# ['MOEX_EVENING_WEEKEND', 'MOEX', 'MOEX_WEEKEND']:
        #         # t.append(i.ticker)
        #         # risk = price_float_ti(i.dlong)
        #         # di[i.figi] = 1 / risk if risk != 0 else risk
        #         t.append(i.figi)
        # return t




moscow_tz = timezone('Europe/Moscow')

async def get_price_open(symbol):
    current_time = datetime.now(moscow_tz)
    start_time = current_time.replace(hour=10, minute=0, second=0, microsecond=0)
    if current_time < start_time:  # если текущее время меньше 10 утра
        start_time -= timedelta(days=1)  # берем 10 утра предыдущего дня

    async with AsyncClient(TOKEN) as client:
        figi = Info_figi.tiker_figi.get(symbol, None)
        try:
            info = await client.market_data.get_candles(
                figi=figi,
                from_=start_time,
                to=current_time,
                interval=CandleInterval.CANDLE_INTERVAL_1_MIN
            )
            print(f"PPPPPPP - {price_float_ti(info.candles[0].open)}")
            return price_float_ti(info.candles[0].open)
        except:
            return 0.1

async def get_last_pr(figi):
    async with AsyncClient(TOKEN) as client:
        price = await client.market_data.get_order_book(figi=figi, depth=10)
        if price and price.bids and len(price.bids) > 0:
            return await asy_price_float_ti(price.bids[0].price)
        else:
            return None



async def get_sandels_hour(symbol):
    async with AsyncClient(TOKEN) as client:
        figi = Info_figi.tiker_figi.get(symbol, None)
        moscow_tz = timezone('Europe/Moscow')
        info = await client.market_data.get_candles(
            figi=figi,
            from_=datetime.now(moscow_tz) - timedelta(days=7),
            to=datetime.now(moscow_tz),
            interval=CandleInterval.CANDLE_INTERVAL_HOUR,
        )
        all_light = []
        all_low = []
        list_vwap = []
        all_volume = 0
        all_price_volume = 0
        date_dey = info.candles[0].time.day
        count = 0
        las_price = await get_last_pr(figi)
        last_vwap = 0
        for i in info.candles:
            low = price_float_ti(i.low)
            hight = price_float_ti(i.high)
            close = price_float_ti(i.close)
            open = price_float_ti(i.open)
            evereng_price = round((hight + low + close) / 3, 4)
            if date_dey is not  i.time.day:
                date_dey = i.time.day
                all_volume = 0
                all_price_volume = 0
            all_volume += i.volume
            eeee = round(i.volume * evereng_price, 1)
            all_price_volume += eeee
            vwap = round(all_price_volume / all_volume, 4)
            last_vwap = vwap
            # list_vwap.append(get_percent(vwap, hight),vwap, get_percent(vwap, low)))
            all_light.append(get_percent(vwap, hight))
            all_low.append(get_percent(vwap, low))
            # print(all_light)
            # print(all_low)
        print(las_price)
        print(last_vwap)
        vwap_real = get_percent(last_vwap, las_price)
        if vwap_real != None:
            vwap_histori = max(all_light) if vwap_real > 0 else min(all_low)
            return vwap_real, vwap_histori
        else:
        # return {'night': max(all_light), 'low' : min(all_low), 'real' : real}
            return 0, 0
        # print(all_price_volume)

# get_sandels_hour('GTRK')
#получение  последних цен всех  акций
async def get_last_price_all_tiker():
    async with AsyncClient(TOKEN) as client:
        info = await client.market_data.get_last_prices(figi=[i for i in Info_figi.figi_ti])
        last_price_all = {Info_figi.figi_tiker.get(i.figi) : price_float_ti(i.price) for i in info.last_prices}
        return last_price_all


#получение цен закрытия всех акций

#функция опредеоения на сколько  цена
async def calculate_percentage(price_zacr, price_real):
    if price_real is not None and price_zacr is not None and price_real != 0:
        percentage_difference = ((price_real - price_zacr) / price_zacr) * 100
        return round(percentage_difference, 2)
    else:
        return 0


def get_sandels_day(symbol, day=366):
    with Client(TOKEN) as client:
        current_time = datetime.now(moscow_tz)
        start_time = current_time.replace(hour=10, minute=0, second=0, microsecond=0)
        if current_time < start_time:  # если текущее время меньше 10 утра
            start_time -= timedelta(days=1)  # берем 10 утра предыдущего дня
        figi = Info_figi.tiker_figi.get(symbol, None)

        info = client.market_data.get_candles(
            figi=figi,
            from_=now() - timedelta(minutes=1),
            to=now(),
            interval=CandleInterval.CANDLE_INTERVAL_HOUR
        )
        all_high = []
        all_low = []
        print(info.candles[-1].time.date(), info.candles[-1].time.hour)
        print(now().date(), now().time().hour)

        print(info.candles[-1])
        # for i in info.candles:
        #     low = price_float_ti(i.low)
        #     hight = price_float_ti(i.high)
        #     close = price_float_ti(i.close)
        #     open = price_float_ti(i.open)
        #     evereng_price = round((hight + low + close) / 3, 4)
        #     eeee = round(i.volume * evereng_price, 1)
        #     all_high.append(get_percent(evereng_price, hight))
        #     all_low.append(get_percent(evereng_price, low))
        # return {f"day - {day}": {'night': max(all_high), 'low': min(all_low)}}

# get_sandels_day('SBER')

# print(datetime.now().time())
# @decorator_speed
def get_all_sandels(symbol, day=366):
    with Client(TOKEN) as client:
        all_light = []
        all_low = []
        list_vwap = []
        all_volume = 0
        all_price_volume = 0
        # date_dey = i.candles[0].time.day
        count = 0
        figi = valuta_fut[symbol].get('figi')
        moscow_tz = timezone('Europe/Moscow')
        rez = {}
        for i in client.get_all_candles(
            figi=figi,
            from_=now() - timedelta(days=1),
            interval=CandleInterval.CANDLE_INTERVAL_5_MIN
            ):
            low = price_float_ti(i.low)
            hight = price_float_ti(i.high)
            close = price_float_ti(i.close)
            open = price_float_ti(i.open)
            evereng_price = round((hight + low + close) / 3, 4)
            rez[f"{i.time.year}.{i.time.month}.{i.time.day}.{i.time.hour}.{i.time.minute}"] = {'low' : low, 'hight' : hight, 'open' : open , 'close' : close}
        return rez
            # if date_dey is not i.time.day:
            #     date_dey = i.time.day
            #     all_volume = 0
            #     all_price_volume = 0
            # all_volume += i.volume
            # eeee = round(i.volume * evereng_price, 1)
            # all_price_volume += eeee
            # vwap = round(all_price_volume / all_volume, 4)
            # # list_vwap.append(get_percent(vwap, hight),vwap, get_percent(vwap, low)))
            # all_light.append(get_percent(vwap, hight))
            # all_low.append(get_percent(vwap, low))
            # return {'night': max(all_light), 'low': min(all_low)}
def corilaciya(symbol1, symbol2):
    si_12 = get_all_sandels(symbol1)
    si_3 = get_all_sandels(symbol2)
    return [si_3[i]['close'] - si_12[i]['close'] for i in si_3]
# rez = corilaciya('SiZ3', 'SiH4')
# print(max(rez), min(rez))
# print(sum(rez)/len(rez))
# print(len(rez))
# print()

# get_sandels_day('FLOT')
def get_lenta(symbol):
    with Client(TOKEN) as client:
        figi = Info_figi.tiker_figi[symbol]
        info = client.market_data.get_last_trades(
            figi=figi,
            from_=now() - timedelta(minutes=1),
            to=now()
            )

        print(f"{info.trades[-1].time.hour:02d}:{info.trades[-1].time.minute:02d}:{info.trades[-1].time.second:02d} {price_float_ti(info.trades[-1].price)} ")







