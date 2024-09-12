import os
import aiohttp
import asyncio
import json
import requests
from deep_translator import MyMemoryTranslator
from concurrent.futures import ThreadPoolExecutor




translator = MyMemoryTranslator(source="en-GB", target="ru-RU")
def translate_text(text):
    translation = translator.translate(text)
    return translation

async def webhook_discord(webhook_url, content, username="The Trading Times"):
    async with aiohttp.ClientSession() as session:
        data = {
            "content": f"{content}",
            "username": username
        }
        headers = {"Content-Type": "application/json"}

        async with session.post(webhook_url, data=json.dumps(data), headers=headers) as response:
            if response.status == 204:
                print("Message sent successfully.")
            else:
                print(f"Failed to send message. Status code: {response.status}")


url = 'https://discord.com/api/webhooks/1263747088697528360/oEVrj6anDzx0Qzw_qmcUHCFZENhpzFdEY-O4iyc_O-I4GatGie-vq_EP62b3nVEP61VE'
def hhhh():
    headers = {"Content-Type": "application/json"}
    payload = {
        "content": 'test',
        "username": "The Trading Times"#"The Trader's Gazette"
    }

    response = requests.post(url=url, data=json.dumps(payload), headers=headers)

    print(response.status_code)
    print(response.text)


# hhhh()
async def dowload_photo_adn_send(bot, event, text, target_chat):
    await event.download_media(file='photo.jpg')
    # Отправляем фото через Aiogram
    with open('photo.jpg', 'rb') as photo:
        await bot.send_photo(chat_id=target_chat, photo=photo, caption=text)

    # Удаляем фото после отправки
    if os.path.exists('photo.jpg'):
        os.remove('photo.jpg')



async def dowload_photos(event):
    """Функция для загрузки фото"""
    photos = []
    file_paths = []
    if isinstance(event.media, MessageMediaPhoto):
        # Скачиваем каждое фото в байтах и сохраняем в список
        file_path = await event.download_media(file='photo.jpg')
        photos.append(InputMediaPhoto(open(file_path, 'rb')))
        file_paths.append(file_path)  # Добавляем путь к файлу для последующего удаления
    return photos, file_paths