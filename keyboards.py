from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Получить информацию по товару"),
            KeyboardButton(text="Остановить уведомления"),
            KeyboardButton(text="Получить информацию из БД")
        ]
    ],
    resize_keyboard=True
)

subscribe = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Подписаться", callback_data="subscribe")]
    ]
)
