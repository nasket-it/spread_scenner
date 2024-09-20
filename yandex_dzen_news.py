# import requests
# from bs4 import BeautifulSoup
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
# }
# html = requests.get('https://www.kommersant.ru/rubric/4?from=burger', headers=headers).text
# soup = BeautifulSoup(html, 'html.parser')
# # print(soup)
# # Поиск элемента по атрибуту data-tes
# price = soup.find_all('span', class_='vam')
# for i in price:
#     print(i.text)
# print(price)
