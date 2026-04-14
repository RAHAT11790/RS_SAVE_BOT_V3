# Copyright (c) 2025 devgagan : https://github.com/devgaganin.  

import asyncio
import sys
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN, STRING

# Fix event loop
if sys.version_info >= (3, 10):
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

# শুধু Pyrogram ক্লায়েন্ট
app = Client("pyrogrambot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
userbot = Client("4gbbot", api_id=API_ID, api_hash=API_HASH, session_string=STRING) if STRING else None

async def start_client():
    """Start Pyrogram clients"""
    try:
        await app.start()
        print("✅ Pyrogram client started")
    except Exception as e:
        print(f"❌ Pyrogram start error: {e}")
        return None, None
    
    if STRING and userbot:
        try:
            await userbot.start()
            print("✅ Userbot started")
        except Exception as e:
            print(f"⚠️ Userbot error: {e}")
    
    return app, userbot

async def stop_client():
    """Stop clients gracefully"""
    print("\n🛑 Stopping clients...")
    
    if STRING and userbot:
        try:
            await userbot.stop()
            print("✅ Userbot stopped")
        except Exception as e:
            print(f"⚠️ Userbot stop error: {e}")
    
    try:
        await app.stop()
        print("✅ Pyrogram stopped")
    except Exception as e:
        print(f"⚠️ Pyrogram stop error: {e}")
    
    print("✅ All clients stopped")
