
async def calculate_funding(price_future, price_spot, K1=0.0005, K2=0.0035):
    # Отклонение цен D
    D = price_future - price_spot
    print(f"D - {D}")
    # Допустимое отклонение цен L1
    L1 = K1 * price_spot
    print(f"L1- {L1}")
    # Максимальный Funding L2
    L2 = K2 * price_spot
    print(f"L2 - {L2}")
    # Расчет Funding
    # funding = min(L2, max(-L2, min(-L1, D) + max(L1, D)))
    funding = round(min(L2, max(-L2, min(-L1, D) + max(L1, D))), 5)


    print(f"fanding - {funding}")
    return funding

