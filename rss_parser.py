# from secrete import URL_rss, Flag, Chenal_id, WebhookDiscod
# from all_function import webhook_discord
# import feedparser
# import aiohttp
# import asyncio
#
#
# last_message_news = {}
#
# async def rebrentext_send_discord_telegram(text, bot, func_link_text,
#                                            webhoo1=WebhookDiscod.webhook2,
#                                            webhoo2=WebhookDiscod.webhook1,
#                                            chenal_id1=Chenal_id.trading_times_id):
#     link_text = await func_link_text('The Trade Time')
#     text_discord = text
#     text_telegram = '🔹🔻🔸\n\n' + text
#     text_discord = f"{text_discord}\n\n▫️ The Trading Times"
#     text_telegram = f"{text_telegram}\n\n🅾️ {link_text}"
#     if Flag.vikluchatel_webhook:
#         await webhook_discord(webhoo1, text_discord)
#         await webhook_discord(webhoo2, text_discord)
#     if Flag.knoka_send_post:
#         await bot.send_message(chenal_id1, text_telegram, parse_mode='HTML', disable_web_page_preview=True)
#
#
# async def fetch_rss(session, url):
#     async with session.get(url) as response:
#         content = await response.text()
#         return feedparser.parse(content)
#
#
#
# async def check_rss(rss: str, istochnik: str, bot, func_link_text):#, istochnik: str
#     global last_message_news
#     rss_url = rss
#     async with aiohttp.ClientSession() as session:
#         # if istochnik == 'tass':
#         feed = await fetch_rss(session, rss_url)
#         if istochnik == 'google_alerts':
#             if feed.entries:
#                 list_news = []
#                 len_rss = len(feed.entries)
#                 for i in feed.entries:
#                     category = i.get('category', None)
#                     title = i.get('title', None)
#                     date_publ = i.get('published', None)
#                     summary = i.get('summary', None)
#                     id = i.get('id', None)
#                     link = i.get('link', None).split('//')[2].split('/')
#                     if len(link) >= 3:
#                         link ='www.' +  '/'.join(link[:-1])
#                     else:
#                         link = 'www.' + link[0]
#                     # link_up = link.upper()
#                     if 'blog' in link or 'post' in link:
#                         pass
#                     else:
#                         list_news.append(f"{title} - {link} длина ленты {len_rss}")
#                 return list_news
#         else:
#             category = feed.entries[0].get('category', None)
#             title = feed.entries[0].get('title', None)
#             date_publ = feed.entries[0].get('published', None)
#             summary = feed.entries[0].get('summary', None)
#             id = feed.entries[0].get('id', None)
#             print(last_message_news)
#             if category in ['Экономика и бизнес', 'Экономика']:
#                 if id != last_message_news.get(istochnik, False):
#                     last_message_news[istochnik] = id
#                     text_message = f"{title}\n{summary} -[{istochnik}]" if summary else f"{title} -[{istochnik}]"
#                     await rebrentext_send_discord_telegram(text_message, bot, func_link_text)
#         # elif  istochnik == 'interfaks':
#         #     feed = await fetch_rss(session, rss_url)
#         #     category = feed.entries[0].get('category', None)
#         #     title = feed.entries[0].get('title', None)
#         #     date_publ = feed.entries[0].get('published', None)
#         #     summary = feed.entries[0].get('summary', None)
#         #     id = feed.entries[0].get('id', None)
#         #     print(title, category, date_publ, summary, id )
#             # print(last_message_news)
            # if category == 'Экономика и бизнес':
            #     if id != last_message_news.get(istochnik, False):
            #         last_message_news[istochnik] = id
            #         text_message = f"{title}\n{summary}" if summary else title
            #         await rebrentext_send_discord_telegram(text_message, bot, func_link_text)


