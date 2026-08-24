import asyncio
import random
import re
import os
import logging
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from pyrogram import Client, filters
from pyrogram.types import Message

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION_STRING = os.environ["SESSION_STRING"]

CHANNEL_ID = int(os.environ["CHANNEL_ID"])

REPLY_TEMPLATE = "Check out our catalogue at @bonfireglowdumps ˙⋆✮  specialize in jkt / food / travel / luxury pics ˙⋆✮ all pics 1x sell ˙⋆✮  all taken by ip 14 pro / 15 pro / 17 pro ˙⋆✮  hmu @bonfireglow as seller"


def is_luxury_request(text: str) -> bool:
    if not text:
        return False
    # Check for negative prefixes inline (lookbehind has fixed-width limit)
    for match in re.finditer(r"\b(lux(?:ury)?|fancy)\b", text, re.IGNORECASE):
        before = text[: match.start()].rstrip()
        last_word = before.split()[-1].lower() if before.split() else ""
        if last_word in ("no", "non", "jangan"):
            continue
        return True
    return False


app = Client("seller_bot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)


@app.on_message()
async def debug_all(client: Client, message: Message):
    logging.info(f"[DEBUG-ALL] chat_id={message.chat.id} | signature='{message.author_signature}' | text='{(message.text or '')[:60]}'")


@app.on_message(filters.channel)
async def debug_channel(client: Client, message: Message):
    logging.info(f"[DEBUG-CHANNEL] chat_id={message.chat.id} | signature='{message.author_signature}' | text='{(message.text or '')[:60]}'")


@app.on_message(filters.group)
async def debug_group(client: Client, message: Message):
    logging.info(f"[DEBUG-GROUP] chat_id={message.chat.id} | text='{(message.text or '')[:60]}'")


@app.on_message(filters.chat(CHANNEL_ID) & filters.text)
async def handle_wtb_post(client: Client, message: Message):
    signature = (message.author_signature or "").lower()
    logging.info(f"New message | signature='{signature}' | text='{message.text[:80]}'")

    if "wtb" not in signature:
        logging.info("Skipped: signature does not contain 'wtb'")
        return

    if not is_luxury_request(message.text):
        logging.info("Skipped: no luxury keyword matched")
        return

    delay = random.randint(65, 300)
    logging.info(f"Replying in {delay}s...")
    await asyncio.sleep(delay)
    try:
        await message.reply(REPLY_TEMPLATE)
        logging.info("Reply sent.")
    except Exception as e:
        logging.error(f"Failed to reply: {e}")


def start_health_server():
    port = int(os.environ.get("PORT", 8080))

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")

        def log_message(self, *args):
            pass

    HTTPServer(("", port), Handler).serve_forever()


if __name__ == "__main__":
    threading.Thread(target=start_health_server, daemon=True).start()
    app.run()
