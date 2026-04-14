# Copyright (c) 2025 devgagan : https://github.com/devgaganin.  
# Licensed under the GNU General Public License v3.0.  

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
    await start_client()
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
    """Graceful shutdown"""
    print(f"\n⚠️ {signal_name or 'Shutdown'} signal received")
    print("🛑 Initiating graceful shutdown...")
    await stop_client()
    print("✅ Shutdown complete")
    loop = asyncio.get_event_loop()
    loop.stop()

async def main():
    """Main function"""
    await load_and_run_plugins()
    print("🤖 Bot is running!")
    while True:
        await asyncio.sleep(5)

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    signal_name = signal.Signals(signum).name
    print(f"\n📡 Received signal: {signal_name}")
    asyncio.create_task(shutdown(signal_name))

def run_flask():
    """Run Flask app in separate thread"""
    os.system("python app.py")

if __name__ == "__main__":
    # Start Flask
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    print("🌐 Flask router started on port 10000")
    
    # Wait for Flask to start
    asyncio.run(asyncio.sleep(2))
    
    # Signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    print("🚀 Starting SpyBot...")
    print("=" * 40)
    
    try:
        loop.run_until_complete(main())
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
