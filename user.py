import asyncio

from aiogram import types

from BD import RequestHistory, session
from keyboards import subscribe
from tasks import fetch, format_inf, stop_notifications, notification
from utils import subscriptions


async def stop(message: types.Message):
    chat_id = message.from_user.id
    if chat_id in subscriptions:
        subscriptions.pop(chat_id, None)
        await message.answer("Уведомления остановлены")
        await stop_notifications(chat_id)
    else:
        await message.answer("У вас нет активных уведомлений")


async def process_article(message: types.Message):
    article = message.text
    product_info = await fetch(article)
    if product_info:
        message_text = format_inf(product_info)
        await message.answer(message_text)
        await message.answer("Хотите подписаться на уведомления о данном товаре?", reply_markup=subscribe)
        new_request = RequestHistory(user_id=message.from_user.id, article=article)
        session.add(new_request)
        session.commit()
    else:
        await message.answer("Товар с таким артикулом не найден.")


async def callback(query: types.CallbackQuery):
    chat_id = query.message.chat.id
    if chat_id in subscriptions:
        subscriptions.pop(chat_id, None)
        await query.answer("Вы прекратили уведомления")
    else:
        subscriptions[chat_id] = True
        await query.answer("Вы подписались на уведомления")
        await asyncio.create_task(notification(chat_id))


async def get_info(message: types.Message):
    print("Fetching data from database...")
    requests = session.query(RequestHistory).filter(RequestHistory.user_id == message.from_user.id).order_by(
        RequestHistory.id.desc()).limit(5).all()
    if requests:
        for request in requests:
            article = request.article
            product_info = await fetch(article)
            if product_info:
                await message.answer(format_inf(product_info))
    else:
        await message.answer("Нет информации о запрошенном товаре.")
