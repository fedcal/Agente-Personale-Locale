import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
API_URL = os.environ.get("AGENT_API", "http://127.0.0.1:8000/chat")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ciao! Sono ARES (bot). Inviami un messaggio.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    try:
        r = requests.post(API_URL, json={"message": text}, timeout=60)
        r.raise_for_status()
        data = r.json()
        await update.message.reply_text(data.get("response", "Nessuna risposta"))
    except Exception as e:
        logger.exception(e)
        await update.message.reply_text(f"Errore: {e}")

def run_bot():
    if TELEGRAM_TOKEN is None:
        print("Imposta TELEGRAM_TOKEN in env")
        return
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Telegram bot avviato...")
    app.run_polling()
