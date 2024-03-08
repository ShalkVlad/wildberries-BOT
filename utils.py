import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

load_dotenv()

subscriptions = {}

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
