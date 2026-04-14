# Copyright (c) 2025 devgagan : https://github.com/devgaganin.  
# Licensed under the GNU General Public License v3.0.  
# See LICENSE file in the repository root for full license text.

from telethon import TelegramClient
from config import API_ID, API_HASH, BOT_TOKEN, STRING
from pyrogram import Client
import sys
import asyncio

# গ্লোবাল ভেরিয়েবল
client = TelegramClient("telethonbot", API_ID, API_HASH)
app = Client("pyrogrambot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
userbot = Client("4gbbot", api_id=API_ID, api_hash=API_HASH, session_string=STRING)

async def start_client():
    """Start all clients"""
    if not client.is_connected():
        await client.start(bot_token=BOT_TOKEN)
        print("✅ Telethon client started...")
    
    if STRING:
        try:
            await userbot.start()
            print("✅ Userbot started...")
        except Exception as e:
            print(f"⚠️ Userbot start failed: {e}")
    
    await app.start()
    print("✅ Pyrogram client started...")
    return client, app, userbot

async def stop_client():
    """Gracefully stop all clients - FIXED VERSION"""
    print("\n🛑 Stopping all clients gracefully...")
    
    # 1. Stop Pyrogram first
    try:
        if app and hasattr(app, 'is_connected') and app.is_connected:
            await app.stop()
            print("✅ Pyrogram stopped")
    except Exception as e:
        print(f"⚠️ Pyrogram stop error: {e}")
    
    # 2. Stop Userbot
    if STRING:
        try:
            if userbot and hasattr(userbot, 'is_connected') and userbot.is_connected:
                await userbot.stop()
                print("✅ Userbot stopped")
        except Exception as e:
            print(f"⚠️ Userbot stop error: {e}")
    
    # 3. Stop Telethon last (most important)
    try:
        if client and client.is_connected():
            await client.disconnect()
            print("✅ Telethon stopped")
    except Exception as e:
        print(f"⚠️ Telethon stop error: {e}")
    
    # 4. Force cancel all pending tasks
    await asyncio.sleep(0.5)
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    for task in tasks:
        task.cancel()
    
    print("✅ All clients stopped successfully!")
