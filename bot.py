import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# ID администратора (замени на свой)
ADMIN_ID = 6968627549  # Укажи свой Telegram ID

# Словарь для хранения сообщений от пользователей
user_messages = {}

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Привет, {user.first_name}! Че надо?"
    )

# Обработка текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    user_messages[user_id] = update.message.text  # Сохраняем сообщение пользователя

    # Формируем информацию о пользователе
    user_info = (
        f"Имя: {user.first_name}\n"
        f"Фамилия: {user.last_name}\n"
        f"Username: @{user.username}\n"
        f"ID: {user_id}"
    )

    # Уведомляем администратора
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"Сообщение от пользователя:\n{user_info}\n\nТекст:\n{update.message.text}"
    )
    await update.message.reply_text("ща отвечу.")

# Обработка изображений
async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    file_id = update.message.photo[-1].file_id  # Берем самое большое изображение

    # Формируем информацию о пользователе
    user_info = (
        f"Имя: {user.first_name}\n"
        f"Фамилия: {user.last_name}\n"
        f"Username: @{user.username}\n"
        f"ID: {user_id}"
    )

    # Уведомляем администратора
    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=file_id,
        caption=f"Изображение от пользователя:\n{user_info}"
    )
    await update.message.reply_text("ща отвечу.")

# Обработка документов
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    file_id = update.message.document.file_id

    # Формируем информацию о пользователе
    user_info = (
        f"Имя: {user.first_name}\n"
        f"Фамилия: {user.last_name}\n"
        f"Username: @{user.username}\n"
        f"ID: {user_id}"
    )

    # Уведомляем администратора
    await context.bot.send_document(
        chat_id=ADMIN_ID,
        document=file_id,
        caption=f"Документ от пользователя:\n{user_info}"
    )
    await update.message.reply_text("ща отвечу.")

# Ответ администратора пользователю
async def admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        await update.message.reply_text("Вы не администратор.")
        return

    # Формат команды: /reply <user_id> <текст ответа>
    try:
        # Разделяем сообщение на user_id и текст ответа
        _, user_id, *reply_text = update.message.text.split(maxsplit=2)
        user_id = int(user_id)
        reply_text = " ".join(reply_text)

        if user_id in user_messages:
            # Отправляем ответ пользователю
            await context.bot.send_message(chat_id=user_id, text=f"{reply_text}")
            await update.message.reply_text("Ответ отправлен пользователю.")
        else:
            await update.message.reply_text("Пользователь не найден.")
    except (ValueError, IndexError):
        await update.message.reply_text("Ошибка. Используйте формат: /reply <user_id> <текст ответа>")

# Основная функция
def main():
    # Укажи токен своего бота
    application = Application.builder().token("7527905659:AAGbf5G8-AoYHMfjQXjjxvVUddBxHvZPb60").build()

    # Обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("reply", admin_reply))

    # Обработчики сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.PHOTO, handle_image))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()
