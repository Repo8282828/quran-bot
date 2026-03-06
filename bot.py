import random
import requests
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8707181938:AAF7d5i5NuRGAXIo_IHFVTmYTeeDHMBXGb0"

DEFAULT_INTERVAL = 5 * 3600
chat_intervals = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """بوت الذِكْـر 🌹

كل فترة زمنيه بترسل آيه .
لتخصيص البث استخدم /set

المـطور @wwc7r .
"""

    chat_id = update.effective_chat.id
    chat_intervals[chat_id] = DEFAULT_INTERVAL

    await update.message.reply_text(text)

async def set_interval(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [
        [InlineKeyboardButton("1 ساعة", callback_data="1")],
        [InlineKeyboardButton("2 ساعة", callback_data="2")],
        [InlineKeyboardButton("4 ساعة", callback_data="4")],
        [InlineKeyboardButton("6 ساعة", callback_data="6")],
        [InlineKeyboardButton("8 ساعة", callback_data="8")],
        [InlineKeyboardButton("12 ساعة", callback_data="12")],
        [InlineKeyboardButton("24 ساعة", callback_data="24")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "ارسل كم ساعة ينتظر البوت بين كل رسالة وأخرى:",
        reply_markup=reply_markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    hours = int(query.data)
    chat_id = query.message.chat_id

    chat_intervals[chat_id] = hours * 3600

    await query.edit_message_text(f"تم ضبط الوقت كل {hours} ساعة ✅")

def get_random_ayah():

    ayah = random.randint(1, 6236)

    url = f"http://api.alquran.cloud/v1/ayah/{ayah}/ar"

    res = requests.get(url).json()

    return res["data"]["text"]

async def send_ayahs(app):

    while True:

        for chat_id in chat_intervals:

            ayah = get_random_ayah()

            try:
                await app.bot.send_message(chat_id, ayah)
            except:
                pass

        await asyncio.sleep(3600)

async def main():

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("set", set_interval))
    app.add_handler(CallbackQueryHandler(button))

    asyncio.create_task(send_ayahs(app))

    await app.run_polling()

asyncio.run(main())
