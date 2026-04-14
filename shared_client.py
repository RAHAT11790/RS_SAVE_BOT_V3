# Copyright (c) 2025 devgagan : https://github.com/devgaganin.  

import asyncio
import sys
from telethon import TelegramClient
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN, STRING

# Fix event loop
if sys.version_info >= (3, 10):
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

# ⚠️ গুরুত্বপূর্ণ: 'client' নামে Telethon ক্লায়েন্ট রাখতে হবে (প্লাগিনগুলো এটা চায়)
client = TelegramClient("telethonbot", API_ID, API_HASH)
app = Client("pyrogrambot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
userbot = Client("4gbbot", api_id=API_ID, api_hash=API_HASH, session_string=STRING) if STRING else None

async def start_client():
    """Start all clients"""
    
    # Start Telethon (প্লাগিনগুলোর জন্য দরকার)
    try:
        if not client.is_connected():
            await client.start(bot_token=BOT_TOKEN)
            print("✅ Telethon client started")
    except Exception as e:
        print(f"⚠️ Telethon error: {e}")
    
    # Start Pyrogram
    try:
        await app.start()
        print("✅ Pyrogram client started")
    except Exception as e:
        print(f"⚠️ Pyrogram error: {e}")
    
    # Start Userbot
    if STRING and userbot:
        try:
            await userbot.start()
            print("✅ Userbot started")
        except Exception as e:
            print(f"⚠️ Userbot error: {e}")
    
    return client, app, userbot

async def stop_client():
    """Stop all clients"""
    print("\n🛑 Stopping clients...")
    
    if STRING and userbot:
        try:
            await userbot.stop()
            print("✅ Userbot stopped")
        except Exception as e:
            pass
    
    try:
        await app.stop()
        print("✅ Pyrogram stopped")
    except Exception as e:
        pass
    
    try:
        if client and client.is_connected():
            await client.disconnect()
            print("✅ Telethon stopped")
    except Exception as e:
        passpass
