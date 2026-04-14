# Copyright (c) 2025 devgagan : https://github.com/devgaganin.  

import asyncio
import sys
from telethon import TelegramClient
from config import API_ID, API_HASH, BOT_TOKEN, STRING
from pyrogram import Client

# Fix event loop for pyrogram
if sys.version_info >= (3, 10):
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

# Initialize clients
client = TelegramClient("telethonbot", API_ID, API_HASH)
app = Client("pyrogrambot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
userbot = Client("4gbbot", api_id=API_ID, api_hash=API_HASH, session_string=STRING) if STRING else None

async def start_client():
    """Start all clients"""
    if not client.is_connected():
        await client.start(bot_token=BOT_TOKEN)
        print("✅ Telethon client started")
    
    if STRING and userbot:
        try:
            await userbot.start()
            print("✅ Userbot started")
        except Exception as e:
            print(f"⚠️ Userbot error: {e}")
    
    await app.start()
    print("✅ Pyrogram client started")
    return client, app, userbot

async def stop_client():
    """Stop all clients gracefully"""
    print("\n🛑 Stopping all clients...")
    
    # Stop Pyrogram first
    try:
        if app and app.is_connected:
            await app.stop()
            print("✅ Pyrogram stopped")
    except Exception as e:
        print(f"⚠️ Pyrogram stop error: {e}")
    
    # Stop Userbot
    if STRING and userbot:
        try:
            if userbot.is_connected:
                await userbot.stop()
                print("✅ Userbot stopped")
        except Exception as e:
            print(f"⚠️ Userbot stop error: {e}")
    
    # Stop Telethon last
    try:
        if client and client.is_connected():
            await client.disconnect()
            print("✅ Telethon stopped")
    except Exception as e:
        print(f"⚠️ Telethon stop error: {e}")
    
    print("✅ All clients stopped")
