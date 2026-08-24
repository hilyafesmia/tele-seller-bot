"""Run this once locally to generate a SESSION_STRING for your account."""
from pyrogram import Client
import os

api_id = input("Enter API_ID: ").strip()
api_hash = input("Enter API_HASH: ").strip()

with Client("temp_session", api_id=int(api_id), api_hash=api_hash) as app:
    print("\nYour SESSION_STRING (save this as an env var):\n")
    print(app.export_session_string())
