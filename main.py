from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import asyncio
import os

TOKEN = os.getenv("BOT_TOKEN")  # 🔥 MUHIM

GROUPS = set()

async def main_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # 🔥 Guruhni saqlash
    if update.message:
        chat = update.message.chat

        if chat.type in ["group", "supergroup"]:
            if chat.id not in GROUPS:
                GROUPS.add(chat.id)
                print("SAQLANDI:", chat.id)

    # 🔥 Kanal postni forward qilish
    if update.channel_post:
        msg = update.channel_post
        print("POST KELDI")

        for group_id in GROUPS:
            try:
                await context.bot.forward_message(
                    chat_id=group_id,
                    from_chat_id=msg.chat_id,
                    message_id=msg.message_id
                )
                print("YUBORILDI:", group_id)
                await asyncio.sleep(1)
            except Exception as e:
                print("XATO:", e)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, main_handler))

print("Bot ishga tushdi...")
app.run_polling()