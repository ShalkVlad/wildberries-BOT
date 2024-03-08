import asyncio
import logging
from aiogram import types
from aiogram.client.session import aiohttp
from BD import RequestHistory, session, get_data
from bot import subscriptions, bot
from keyboards import subscribe


async def fetch_product_info(article: str):
    try:
        logging.info(f"Fetching product info for article: {article}")  # Журналирование артикула товара
        url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={article}"
        async with aiohttp.ClientSession() as Session:
            async with Session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    quantities = [stock["qty"] for size in data["data"]["products"][0]["sizes"] for stock in
                                  size["stocks"]]
                    product_info = {
                        "name": data["data"]["products"][0]["name"],
                        "article": article,
                        "price": data["data"]["products"][0]["priceU"],
                        "rating": data["data"]["products"][0]["rating"],
                        "quantity": sum(quantities),
                        "quantity_all_warehouses": sum(quantities)
                    }
                    return product_info
                else:
                    logging.error(f"Error fetching product info. Status code: {response.status}")
    except Exception as e:
        logging.error(f"Error fetching product info: {e}")
    return None


def format_product_info(product_info: dict):
    # Преобразование цены к формату без лишних нулей
    price = "{:.2f}".format(float(product_info['price']) / 100)
    return f"Название: {product_info['name']}\n" \
           f"Артикул: {product_info['article']}\n" \
           f"Цена: {price} руб.\n" \
           f"Рейтинг: {product_info['rating']}\n" \
           f"Количество: {product_info['quantity']}"


async def process_article_step(message: types.Message):
    article = message.text
    product_info = await fetch_product_info(article)
    if product_info:
        await message.answer(format_product_info(product_info))
        await message.answer("Хотите подписаться на уведомления о данном товаре?", reply_markup=subscribe)
        # Сохранение истории запроса в базе данных
        new_request = RequestHistory(user_id=message.from_user.id, article=article)
        session.add(new_request)
        session.commit()
    else:
        await message.answer("Товар с таким артикулом не найден.")


async def subscribe_product(chat_id: int, article: str):
    while True:
        product_info = await fetch_product_info(article)
        if product_info:
            await bot.send_message(chat_id=chat_id, text=format_product_info(product_info))
        await asyncio.sleep(300)  # Отправлять уведомление каждые 5 минут


async def subscribe_callback(query: types.CallbackQuery):
    chat_id = query.from_user.id
    article = query.data.split("_")[1]
    subscriptions[chat_id] = asyncio.create_task(subscribe_product(chat_id, article))
    await query.answer("Вы подписались на уведомления")


async def stop_notifications(message: types.Message):
    chat_id = message.from_user.id
    if chat_id in subscriptions:
        subscriptions[chat_id].cancel()
        del subscriptions[chat_id]
        await message.answer("Уведомления остановлены")
    else:
        await message.answer("У вас нет активных уведомлений")


async def get_info_from_db(message: types.Message):
    print("Fetching data from database...")  # Отладочное сообщение
    data = get_data()
    print("Data from database:", data)  # Отладочное сообщение
    if data:
        for entry in data:
            await message.answer(entry)
    else:
        await message.answer("База данных пуста")
