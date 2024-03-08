import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from keyboards import main_menu
from dotenv import load_dotenv

load_dotenv()

subscriptions = {}

# Установка уровня логирования
logging.basicConfig(level=logging.INFO)

# Устанавливаем токен вашего бота
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Создаем экземпляр бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Обработчик команды /start
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Выберите действие из меню:", reply_markup=main_menu)


# Обработчик ввода артикула товара
@dp.message()
async def process_article_step_wrapper(message: types.Message):
    if message.text == "Остановить уведомления":
        from User import stop_notifications
        await stop_notifications(message)
    elif message.text == "Получить информацию из БД":
        print("Button pressed:", message.text)
        from User import get_info_from_db
        await get_info_from_db(message)
    elif message.text == "Получить информацию по товару":
        print("Button pressed:", message.text)
        await message.answer("Введите артикул товара с Wildberries:")
    else:
        article = message.text
        if article.isdigit():  # Проверка, является ли введенный текст числом (артикулом)
            from User import process_article_step
            await process_article_step(message)
        else:
            await message.answer("Введите корректный артикул товара с Wildberries.")


# Обновите функцию subscribe_callback
@dp.callback_query(lambda query: query.data.startswith("subscribe"))
async def subscribe_callback_wrapper(query: types.CallbackQuery):
    from User import subscribe_callback
    await subscribe_callback(query)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
