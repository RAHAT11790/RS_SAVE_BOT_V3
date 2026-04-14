# Copyright (c) 2025 devgagan : https://github.com/devgaganin.  

import asyncio
from shared_client import start_client, stop_client
import importlib
import os
import sys
import signal
import threading

async def load_and_run_plugins():
    """Load and run all plugins"""
    print("🔄 Starting clients...")
    result = await start_client()
    if result[0] is None:
        print("❌ Failed to start clients. Exiting...")
        sys.exit(1)
    print("✅ Clients started successfully!")
    
    plugin_dir = "plugins"
    if os.path.exists(plugin_dir):
        plugins = [f[:-3] for f in os.listdir(plugin_dir) 
                  if f.endswith(".py") and f != "__init__.py" and f != "pay.py"]
        
        for plugin in plugins:
            try:
                if f"plugins.{plugin}" in sys.modules:
                    del sys.modules[f"plugins.{plugin}"]
                module = importlib.import_module(f"plugins.{plugin}")
                if hasattr(module, f"run_{plugin}_plugin"):
                    print(f"▶️ Running {plugin} plugin...")
                    await getattr(module, f"run_{plugin}_plugin")()
            except Exception as e:
                print(f"⚠️ Plugin {plugin} error: {e}")

async def shutdown(signal_name=None):
    print(f"\n⚠️ {signal_name or 'Shutdown'} received")
    await stop_client()
    loop = asyncio.get_event_loop()
    loop.stop()

async def main():
    await load_and_run_plugins()
    print("🤖 Bot is running!")
    while True:
        await asyncio.sleep(5)

def signal_handler(signum, frame):
    signal_name = signal.Signals(signum).name
    loop = asyncio.get_event_loop()
    if loop.is_running():
        asyncio.create_task(shutdown(signal_name))
    else:
        loop.run_until_complete(shutdown(signal_name))

def run_flask():
    os.system("python app.py")

async def start_flask_and_bot():
    """Start Flask and then the bot"""
    # Start Flask in background
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    print("🌐 Flask started on port 10000")
    
    # Give Flask time to start
    await asyncio.sleep(2)
    
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Run main bot
    await main()

if __name__ == "__main__":
    print("🚀 Starting Bot...")
    print("=" * 40)
    
    # Create new event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        loop.run_until_complete(start_flask_and_bot())
    except KeyboardInterrupt:
        print("\n👋 Keyboard interrupt received")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)
    finally:
        try:
            loop.run_until_complete(asyncio.sleep(0.5))
            loop.close()
            print("✅ Event loop closed")
        except Exception as e:
            print(f"⚠️ Cleanup error: {e}")
