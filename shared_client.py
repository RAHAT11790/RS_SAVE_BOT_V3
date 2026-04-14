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

# ক্লায়েন্ট - এখানে client নামে ভেরিয়েবল থাকতে হবে
client = TelegramClient("telethonbot", API_ID, API_HASH)
app = Client("pyrogrambot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
userbot = Client("4gbbot", api_id=API_ID, api_hash=API_HASH, session_string=STRING) if STRING else None

async def start_client():
    """Start all clients"""
    
    # Start Telethon
    try:
        if not client.is_connected():
            await client.start(bot_token=BOT_TOKEN)
            print("✅ Telethon started")
    except Exception as e:
        print(f"⚠️ Telethon: {e}")
    
    # Start Pyrogram
    try:
        await app.start()
        print("✅ Pyrogram started")
    except Exception as e:
        print(f"⚠️ Pyrogram: {e}")
    
    # Start Userbot
    if STRING and userbot:
        try:
            await userbot.start()
            print("✅ Userbot started")
        except Exception as e:
            print(f"⚠️ Userbot: {e}")
    
    return client, app, userbot

async def stop_client():
    """Stop all clients"""
    print("\n🛑 Stopping...")
    
    if STRING and userbot:
        try:
            await userbot.stop()
        except:
            pass
    
    try:
        await app.stop()
    except:
        pass
    
    try:
        if client and client.is_connected():
            await client.disconnect()
    except:
        pass
    
    print("✅ Stopped")

# 🔥 এই লাইনগুলো গুরুত্বপূর্ণ - প্লাগিন যাতে ইম্পোর্ট করতে পারে
__all__ = ['client', 'app', 'userbot', 'start_client', 'stop_client']
