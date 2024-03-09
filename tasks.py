import asyncio
import logging

from aiogram.client.session import aiohttp
from celery import Celery

from BD import RequestHistory, session
from utils import bot, subscriptions

app = Celery('tasks', broker='pyamqp://guest@localhost//')


@app.task
async def send_notification(chat_id: int, product_info: dict):
    message_text = format_inf(product_info)
    await bot.send_message(chat_id=chat_id, text=message_text)


async def fetch(article_inf: str):
    try:
        logging.info(f"Fetching product info for article: {article_inf}")
        url = f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={article_inf}"
        async with aiohttp.ClientSession() as Session:
            async with Session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    quantities = [stock["qty"] for size in data["data"]["products"][0]["sizes"] for stock in
                                  size["stocks"]]
                    product_info = {
                        "name": data["data"]["products"][0]["name"],
                        "article": article_inf,
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


@app.task
async def fetch_product(chat_id: int, article: str):
    product_info = await fetch(article)
    if product_info:
        await send_notification.delay(chat_id, product_info)


def format_inf(product_info: dict):
    price = "{:.2f}".format(float(product_info['price']) / 100)
    return f"Название: {product_info['name']}\n" \
           f"Артикул: {product_info['article']}\n" \
           f"Цена: {price} руб.\n" \
           f"Рейтинг: {product_info['rating']}\n" \
           f"Количество: {product_info['quantity']}"\
            f"Количество всего: {product_info['quantity_all_warehouses']}"



async def notification(chat_id: int):
    while chat_id in subscriptions:
        try:
            request = session.query(RequestHistory).filter(RequestHistory.user_id == chat_id).order_by(
                RequestHistory.id.desc()).first()
            if request:
                article = request.article
                product_info = await fetch(article)
                if product_info:
                    message_text = format_inf(product_info)
                    await bot.send_message(chat_id=chat_id, text=message_text)
                else:
                    await bot.send_message(chat_id=chat_id,
                                           text="Ошибка при получении информации о товаре. Попробуйте позже.")
            else:
                await bot.send_message(chat_id=chat_id,
                                       text="Нет информации о товаре для подписки. Пожалуйста, отправьте артикул "
                                            "товара снова.")
        except Exception as e:
            logging.error(f"Error sending notification: {e}")
        await asyncio.sleep(300)


@app.task
async def stop_notifications(chat_id: int):
    # Остановка отправки уведомлений для пользователя
    subscriptions.pop(chat_id, None)
    await bot.send_message(chat_id=chat_id, text="Уведомления остановлены")


@app.task
async def start_notifications(chat_id: int):
    # Начало отправки уведомлений для пользователя
    subscriptions[chat_id] = True
    await bot.send_message(chat_id=chat_id, text="Вы подписались на уведомления")
