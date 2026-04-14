# Copyright (c) 2025 devgagan : https://github.com/devgaganin.  
# Licensed under the GNU General Public License v3.0.  
# See LICENSE file in the repository root for full license text.

import asyncio
import sys
from telethon import TelegramClient
from config import API_ID, API_HASH, BOT_TOKEN, STRING
from pyrogram import Client

# Force event loop fix
if sys.version_info >= (3, 10):
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

client = TelegramClient("telethonbot", API_ID, API_HASH)
app = Client("pyrogrambot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
userbot = Client("4gbbot", api_id=API_ID, api_hash=API_HASH, session_string=STRING) if STRING else None

async def start_client():
    if not client.is_connected():
        await client.start(bot_token=BOT_TOKEN)
        print("✅ Telethon client started...")
    
    if STRING and userbot:
        try:
            await userbot.start()
            print("✅ Userbot started...")
        except Exception as e:
            print(f"⚠️ Userbot start failed: {e}")
    
    await app.start()
    print("✅ Pyrogram client started...")
    return client, app, userbot

async def stop_client():
    print("\n🛑 Stopping all clients...")
    
    try:
        if app and app.is_connected:
            await app.stop()
            print("✅ Pyrogram stopped")
    except Exception as e:
        print(f"⚠️ Pyrogram stop error: {e}")
    
    if STRING and userbot:
        try:
            if userbot.is_connected:
                await userbot.stop()
                print("✅ Userbot stopped")
        except Exception as e:
            print(f"⚠️ Userbot stop error: {e}")
    
    try:
        if client and client.is_connected():
            await client.disconnect()
            print("✅ Telethon stopped")
    except Exception as e:
        print(f"⚠️ Telethon stop error: {e}")
    
    print("✅ All clients stopped!")
