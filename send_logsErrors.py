import datetime
import sys
import traceback
import asyncio
from secrete import Chenal_id, Flag



async def sendErorsTelegram(bot,id_chenal=Chenal_id.LogsErroors, sec_start=5):
    time_apgrade = datetime.datetime.now()
    # Получение информации об ошибке
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback_details = traceback.format_exception(exc_type, exc_value, exc_traceback)
    title_errors = traceback_details[0]
    file_str_errors = ''.join(traceback_details[1:-1])
    name_errors = traceback_details[-1]
    messageErrorTelegram = f"❗️Время и дата:\n{time_apgrade}\n" \
                           f"🔹Стек вызова:\n{title_errors}\n" \
                           f"📕Где произошла ошибка:\n{file_str_errors}\n" \
                           f"👉Название ошибки:\n{name_errors}\n" \
                           f"🔃Перезаппуск через: {sec_start}"
    if Flag.send_logErrors:
        await asyncio.sleep(2)
        await bot.send_message(id_chenal, messageErrorTelegram)
    else:
        print(messageErrorTelegram)