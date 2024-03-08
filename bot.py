import asyncio

from aiogram import types
from aiogram.filters import Command

from keyboards import main_menu
from user import callback, stop, get_info, process_article
from utils import bot, dp

dp.callback_query(callback)


@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Выберите действие из меню:", reply_markup=main_menu)


@dp.message()
async def wrapper(message: types.Message):
    if message.text == "Остановить уведомления":
        await stop(message)
    elif message.text == "Получить информацию из БД":
        print("Button pressed:", message.text)
        await get_info(message)
    elif message.text == "Получить информацию по товару":
        print("Button pressed:", message.text)
        await message.answer("Введите артикул товара с Wildberries:")
    else:
        article = message.text
        if article.isdigit():
            await process_article(message)
        else:
            await message.answer("Введите корректный артикул товара с Wildberries.")


@dp.callback_query(lambda query: query.data.startswith("subscribe"))
async def callback_wrapper(query: types.CallbackQuery):
    from user import callback
    await callback(query)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
