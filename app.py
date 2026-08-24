import threading
import asyncio
import random
import re
import os
import gradio as gr
from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION_STRING = os.environ["SESSION_STRING"]

CHANNEL_ID = -1001525948158
REPLY_TEMPLATE = "Hi! I have what you're looking for — DM me for details."

app = Client("seller_bot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)


def is_luxury_request(text: str) -> bool:
    if not text:
        return False
    for match in re.finditer(r"\b(lux(?:ury)?|fancy)\b", text, re.IGNORECASE):
        before = text[: match.start()].rstrip()
        last_word = before.split()[-1].lower() if before.split() else ""
        if last_word in ("no", "non", "jangan"):
            continue
        return True
    return False


@app.on_message(filters.chat(CHANNEL_ID) & filters.text)
async def handle_wtb_post(client: Client, message: Message):
    signature = (message.author_signature or "").lower()
    if "wtb" not in signature:
        return
    if not is_luxury_request(message.text):
        return
    await asyncio.sleep(random.randint(5, 30))
    await message.reply(REPLY_TEMPLATE)


def run_bot():
    app.run()


thread = threading.Thread(target=run_bot, daemon=True)
thread.start()


def status():
    return "Bot is running."


demo = gr.Interface(fn=status, inputs=[], outputs="text", title="Seller Bot")
demo.launch()
