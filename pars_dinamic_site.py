import asyncio
from pyppeteer import launch



dict_fanding = {}

async def parse_site(url):
    url_CNYRUBF = "https://www.moex.com/ru/contract.aspx?code=CNYRUBF"
    url_USDRUBF = "https://www.moex.com/ru/contract.aspx?code=USDRUBF"
    url_EURRUBF = "https://www.moex.com/ru/contract.aspx?code=EURRUBF"
    url_GLDRUBF = "https://www.moex.com/ru/contract.aspx?code=GLDRUBF"
    url_IMOEXF = "https://www.moex.com/ru/contract.aspx?code=IMOEXF&utm_source=www.moex.com&utm_term=IMOEXF"
    list_url = {'USDRUBF' : url_USDRUBF, 'EURRUBF' : url_EURRUBF, 'CNYRUBF' : url_CNYRUBF,
                'GLDRUBF' : url_GLDRUBF, 'IMOEXF' : url_IMOEXF}
    # Запускаем браузер в headless режиме
    browser = await launch(headless=True)
    # Открываем новую страницу
    page = await browser.newPage()
    try:
        # Переходим на нужную страницу с пользовательским таймаутом
        await page.goto(url, timeout=10000)  # Устанавливаем таймаут в 10 секунд
        button = await page.querySelector('a.btn2.btn2-primary')
        if button:
            # Проверяем, совпадает ли текст кнопки с "Согласен"
            button_text = await page.evaluate('(button) => button.textContent', button)
            if "Согласен" in button_text:
                await button.click()
                await asyncio.sleep(3)
                print("Кнопка была найдена и нажата.")
            else:
                print("Найдена кнопка, но текст не совпадает.")
        else:
            print("Кнопка не найдена.")
        for key in list_url.keys():
            await page.goto(list_url[key], timeout=10000)
            await asyncio.sleep(3)
            td_elements = await page.xpath("//td[contains(text(), 'Фандинг, руб.')]/following-sibling::td")
            td_texts = await asyncio.gather(*(page.evaluate('(element) => element.textContent', td) for td in td_elements))
            dict_fanding[key] = round(float(td_texts[0].replace(',', '.')), 5)
            await asyncio.sleep(3)


        print(dict_fanding)
        # await asyncio.sleep(10)
    except Exception as e:
        await browser.close()
        print(f'Произошла ошибка лолололол : {e}')
    finally:
        await browser.close()

