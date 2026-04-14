# Copyright (c) 2025 devgagan : https://github.com/devgaganin.  
# Licensed under the GNU General Public License v3.0.  
# See LICENSE file in the repository root for full license text.

from telethon import TelegramClient
from config import API_ID, API_HASH, BOT_TOKEN, STRING
from pyrogram import Client
import sys
import asyncio

client = TelegramClient("telethonbot", API_ID, API_HASH)
app = Client("pyrogrambot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
userbot = Client("4gbbot", api_id=API_ID, api_hash=API_HASH, session_string=STRING)

async def start_client():
    if not client.is_connected():
        await client.start(bot_token=BOT_TOKEN)
        print("SpyLib started...")
    if STRING:
        try:
            await userbot.start()
            print("Userbot started...")
        except Exception as e:
            print(f"Hey honey!! check your premium string session, it may be invalid of expire {e}")
            sys.exit(1)
    await app.start()
    print("Pyro App Started...")
    return client, app, userbot

# ✅ এই ফাংশনটি যোগ করুন (নিচের কোড)
async def stop_client():
    """Gracefully stop all clients"""
    print("Stopping all clients...")
    
    # Stop Telethon client
    try:
        if client and client.is_connected():
            await client.disconnect()
            print("Telethon client stopped")
    except Exception as e:
        print(f"Error stopping Telethon client: {e}")
    
    # Stop Pyrogram app
    try:
        if app and app.is_connected:
            await app.stop()
            print("Pyrogram app stopped")
    except Exception as e:
        print(f"Error stopping Pyrogram app: {e}")
    
    # Stop Userbot
    if STRING:
        try:
            if userbot and userbot.is_connected:
                await userbot.stop()
                print("Userbot stopped")
        except Exception as e:
            print(f"Error stopping userbot: {e}")
    
    print("All clients stopped successfully!")
