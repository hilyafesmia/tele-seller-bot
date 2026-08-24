# Tele Seller Bot

A Telegram userbot that monitors the BASE WTB discussion group and automatically replies to luxury-related WTB posts.

## How it works

- Watches the `@basewtb` channel discussion group for new posts
- Only replies to posts where the author signature contains `"wtb"`
- Only replies if the post contains keywords: `lux`, `luxury`, or `fancy`
- Skips posts where those keywords are preceded by `no`, `non`, or `jangan`
- Waits a random 5–30 seconds before replying to appear human
- Runs on your secondary Telegram account (no BOT badge)

## Setup

### 1. Get Telegram API credentials

1. Log in to [my.telegram.org](https://my.telegram.org) using your **secondary** Telegram account
2. Go to **API development tools**
3. Create a new application (name and description can be anything)
4. Save your `API_ID` and `API_HASH`

### 2. Generate a session string

Run this once on your local machine:

```bash
pip install pyrogram tgcrypto
python generate_session.py
```

Enter your `API_ID` and `API_HASH` when prompted. It will send a login code to your secondary Telegram account. After logging in, it prints a `SESSION_STRING` — copy and save it somewhere safe.

### 3. Customize the reply

Open `bot.py` and edit line 13:

```python
REPLY_TEMPLATE = "Hi! I have what you're looking for — DM me for details."
```

Replace it with your actual seller message.

### 4. Deploy to Koyeb (free)

1. Push this repository to GitHub
2. Sign up at [koyeb.com](https://koyeb.com)
3. Create a new app → select your GitHub repo
4. Set the **run command** to: `python bot.py`
5. Add the following environment variables:

| Variable | Value |
|---|---|
| `API_ID` | your API ID from my.telegram.org |
| `API_HASH` | your API hash from my.telegram.org |
| `SESSION_STRING` | the string from step 2 |

6. Deploy — the bot starts running automatically.

## Keyword logic

| Message | Replies? |
|---|---|
| "WTB lux bag" | Yes |
| "WTB luxury watch" | Yes |
| "WTB fancy shoes" | Yes |
| "WTB non lux item" | No |
| "WTB no luxury" | No |
| "WTB jangan lux" | No |

## Files

| File | Purpose |
|---|---|
| `bot.py` | Main bot — runs continuously on Koyeb |
| `generate_session.py` | One-time script to generate your session string |
| `requirements.txt` | Python dependencies |

## Notes

- Never share your `SESSION_STRING` — it gives full access to your Telegram account
- The bot uses your secondary account so your main account is not at risk
- If the bot gets banned from the group, your main account is unaffected
