from dotenv import load_dotenv
from telegram.ext import Application
import os

load_dotenv(dotenv_path="telegram.env")

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

async def send_message(text):
    application = Application.builder().token(BOT_TOKEN).build()
    await application.bot.send_message(chat_id=CHAT_ID, text=text)

async def main():
    await send_message("This is a test message!")


