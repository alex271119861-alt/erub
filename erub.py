import os
import logging
import json
from datetime import datetime
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest
from dotenv import load_dotenv

# Загружаем токен из .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))
WEB_APP_URL = "https://alex271119861-alt.github.io/win/"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class WinanceBot:
    def __init__(self):
        custom_request = HTTPXRequest(connect_timeout=30.0, read_timeout=30.0)
        self.app = Application.builder()\
            .token(BOT_TOKEN)\
            .request(custom_request)\
            .get_updates_request(HTTPXRequest(connect_timeout=30.0))\
            .build()

        self.app.add_handler(CommandHandler("start", self.start))
        # Ловим данные из tg.sendData()
        self.app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, self.handle_webapp_data))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        await update.message.reply_text(
            f"👋 Привет, {user.first_name}!\nНажмите кнопку ниже:",
            reply_markup=ReplyKeyboardMarkup(
                [[KeyboardButton("🔑 Войти", web_app=WebAppInfo(url=WEB_APP_URL))]],
                resize_keyboard=True,
            ),
        )

    async def handle_webapp_data(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        raw = update.message.web_app_data.data
        user = update.effective_user
        
        try:
            data = json.loads(raw)
        except:
            data = {"raw": raw}

        # Красиво оформляем сообщение
        text = f"📥 <b>ДАННЫЕ ИЗ MINI APP</b>\n\n"
        text += f"👤 ID: <code>{user.id}</code>\n"
        text += f"👤 Имя: {user.first_name}\n\n"
        
        for key, value in data.items():
            text += f"📌 <b>{key}:</b> <code>{value}</code>\n"

        await self.app.bot.send_message(chat_id=ADMIN_ID, text=text, parse_mode="HTML")
        await update.message.reply_text("✅ Данные получены")

    def run(self):
        print("🚀 БОТ ЗАПУЩЕН")
        self.app.run_polling()

if __name__ == "__main__":
    WinanceBot().run()
