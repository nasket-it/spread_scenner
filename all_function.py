import aiohttp
import asyncio
import json
import requests


async def webhook_discord(webhook_url, content, username="The Trading Times"):
    async with aiohttp.ClientSession() as session:
        data = {
            "content": f"📜  •  {content}\n\n---",
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
