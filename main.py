from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import asyncio
import os
import sqlite3

conn = sqlite3.connect("groups.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS groups (
    id INTEGER PRIMARY KEY
)
""")
conn.commit()
TOKEN = os.getenv("BOT_TOKEN")

# GROUPS = set()

async def main_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Guruhni saqlash
    # Guruhni saqlash
    if update.message:
        chat = update.message.chat

        if chat.type in ["group", "supergroup"]:
            cursor.execute("SELECT id FROM groups WHERE id=?", (chat.id,))
            result = cursor.fetchone()

            if not result:
                cursor.execute("INSERT INTO groups (id) VALUES (?)", (chat.id,))
                conn.commit()
                print("BAZAGA SAQLANDI:", chat.id)

    # Kanal post
    if update.channel_post:
        msg = update.channel_post
        print("POST KELDI")

        cursor.execute("SELECT id FROM groups")
        groups = cursor.fetchall()

        for group in groups:
            group_id = group[0]

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
                # 🔥 agar group ishlamasa o‘chiramiz
                cursor.execute("DELETE FROM groups WHERE id=?", (group_id,))
                conn.commit()
                print("O‘CHIRILDI:", group_id)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.ALL, main_handler))

print("Bot ishga tushdi...")
app.run_polling()

import atexit

def close_db():
    conn.close()

atexit.register(close_db)
