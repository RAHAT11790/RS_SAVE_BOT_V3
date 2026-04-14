# Copyright (c) 2025 devgagan : https://github.com/devgaganin.  
# Licensed under the GNU General Public License v3.0.  
# See LICENSE file in the repository root for full license text.

import asyncio
from shared_client import start_client, stop_client
import importlib
import os
import sys
import signal
import threading  # ✅ যোগ করুন

async def load_and_run_plugins():
    """Load and run all plugins"""
    await start_client()
    plugin_dir = "plugins"
    if os.path.exists(plugin_dir):
        plugins = [f[:-3] for f in os.listdir(plugin_dir) 
                  if f.endswith(".py") and f != "__init__.py"]
        
        for plugin in plugins:
            try:
                module = importlib.import_module(f"plugins.{plugin}")
                if hasattr(module, f"run_{plugin}_plugin"):
                    print(f"▶️ Running {plugin} plugin...")
                    await getattr(module, f"run_{plugin}_plugin")()
            except Exception as e:
                print(f"⚠️ Plugin {plugin} error: {e}")

async def shutdown(signal_name=None):
    """Complete graceful shutdown - FIXED"""
    print(f"\n⚠️ {signal_name or 'Shutdown'} signal received")
    print("🛑 Initiating graceful shutdown...")
    
    # Stop all clients
    await stop_client()
    
    # Force stop event loop after cleanup
    loop = asyncio.get_event_loop()
    loop.stop()

async def main():
    """Main function"""
    await load_and_run_plugins()
    print("🤖 Bot is running...")
    
    # Keep running until stopped
    while True:
        await asyncio.sleep(1)

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    signal_name = signal.Signals(signum).name
    print(f"\n📡 Received signal: {signal_name}")
    
    # Create task for shutdown
    loop = asyncio.get_event_loop()
    if loop.is_running():
        asyncio.create_task(shutdown(signal_name))
    else:
        loop.run_until_complete(shutdown(signal_name))

# ✅ Flask চালানোর ফাংশন যোগ করুন (নিচের অংশ)
def run_flask():
    """Flask app চালানোর জন্য আলাদা থ্রেড"""
    os.system("python app.py")

if __name__ == "__main__":
    # ✅ Flask ব্যাকগ্রাউন্ডে চালান
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    print("🌐 Flask router started on port 10000")
    
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)   # Ctrl+C
    signal.signal(signal.SIGTERM, signal_handler)  # Render shutdown
    
    # Create new event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    print("🚀 Starting SpyBot...")
    print("=" * 40)
    
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\n👋 Keyboard interrupt received")
    except asyncio.CancelledError:
        print("⚠️ Tasks cancelled")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)
    finally:
        try:
            # Final cleanup
            loop.run_until_complete(asyncio.sleep(0.3))
            loop.close()
            print("✅ Event loop closed successfully")
        except Exception as e:
            print(f"⚠️ Cleanup error: {e}")
