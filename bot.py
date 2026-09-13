import logging
import random
import json

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)

# 1. Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 2. Токен бота (замените на ваш реальный)
BOT_TOKEN = "TOKEN"

# 3. Загрузка вопросов и заданий
with open('data.json', encoding='utf-8') as f:
    data = json.load(f)


# 4. Формирование клавиатуры
def get_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🎤 Правда", callback_data="truth"),
            InlineKeyboardButton("🏃 Действие", callback_data="dare"),
        ],
        [InlineKeyboardButton("🔒 Доп. Категории", callback_data="extra")],
    ]
    return InlineKeyboardMarkup(keyboard)


# 5. Обработчики
def register_handlers(app):
    async def start(update, context):
        await update.message.reply_text(
            "🎉 Добро пожаловать в игру 'Правда или Действие'! Выберите опцию:",
            reply_markup=get_keyboard()
        )

    async def button_handler(update, context):
        query = update.callback_query
        await query.answer()
        cmd = query.data
        if cmd in ("truth", "dare"):
            pool = data[cmd]["default"].copy()
            if not pool:
                text = "⚠️ Список пуст."
            else:
                prefix = "❓" if cmd == "truth" else "🎯"
                text = f"{prefix} {random.choice(pool)}"
            await query.edit_message_text(text, reply_markup=get_keyboard())
        elif cmd == "extra":
            text = "🔒 Функция 'Доп. Категории' доступна в будущих версиях!"
            await query.edit_message_text(text, reply_markup=get_keyboard())

    async def echo(update, context):
        await update.message.reply_text(
            "Пожалуйста, используйте кнопки меню ниже.",
            reply_markup=get_keyboard()
        )

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))


# 6. Запуск бота
if __name__ == '__main__':

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    register_handlers(app)

    logger.info("Бот запущен")
    app.run_polling()
