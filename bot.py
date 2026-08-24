import asyncio
import random
import re
import os
from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION_STRING = os.environ["SESSION_STRING"]

CHANNEL_ID = -1001525948158

REPLY_TEMPLATE = "Hi! I have what you're looking for — DM me for details."

# Matches lux/luxury/fancy but NOT when preceded by no/non/jangan (with optional space)
KEYWORD_PATTERN = re.compile(
    r"(?<!\b(?:no|non|jangan)\s)\b(lux(?:ury)?|fancy)\b",
    re.IGNORECASE,
)


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


@app.on_message(filters.chat(CHANNEL_ID) & filters.text)
async def handle_wtb_post(client: Client, message: Message):
    signature = (message.author_signature or "").lower()
    if "wtb" not in signature:
        return

    if not is_luxury_request(message.text):
        return

    delay = random.randint(5, 30)
    await asyncio.sleep(delay)
    await message.reply(REPLY_TEMPLATE)


if __name__ == "__main__":
    app.run()
