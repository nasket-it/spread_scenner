import asyncio
from scipy.stats import norm
import math





def cumulative_normal(x: float) -> float:
    """Вычисляет кумулятивное распределение стандартного нормального."""
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


async def theoretical_option_price(F: float, strike: float, sigma: float, T: float):
    """
    Вычисляет теоретическую цену опциона call и put по модели Блэка–Шоулза для опционов на фьючерсы.

    Параметры:
      F (float): Текущая цена фьючерсного контракта (базового актива)
      strike (float): Цена исполнения опциона
      sigma (float): Годовая волатильность базового актива (в долях единицы)
      T (float): Время до экспирации опциона (в годах)

    Возвращает:
      dict: Словарь с ключами 'call' и 'put', содержащими теоретические цены опционов.
    """
    if sigma <= 0 or T <= 0:
        # Если волатильность нулевая или время истечения 0 – просто цена intrinsic value.
        call_price = max(F - strike, 0)
    else:
        d1 = (math.log(F / strike) + 0.5 * sigma * sigma * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)
        Nd1 = cumulative_normal(d1)
        Nd2 = cumulative_normal(d2)
        call_price = F * Nd1 - strike * Nd2

    put_price = call_price + strike - F

    return  round(put_price, 3), round(call_price, 3)

# Пример использования:
# asyncio.run(theoretical_option_price(100, 95, 0.2, 0.25))