# Copyright (c) 2025 devgagan : https://github.com/devgaganin.  
# Licensed under the GNU General Public License v3.0.  
# See LICENSE file in the repository root for full license text.

import asyncio
from shared_client import start_client, stop_client
import importlib
import os
import sys
import signal
import threading
import shutil

async def load_and_run_plugins():
    """Load and run all plugins"""
    await start_client()
    plugin_dir = "plugins"
    if os.path.exists(plugin_dir):
        # 🔥 ক্যাশ পরিষ্কার করুন
        for root, dirs, files in os.walk(plugin_dir):
            if "__pycache__" in dirs:
                pycache_path = os.path.join(root, "__pycache__")
                shutil.rmtree(pycache_path, ignore_errors=True)
                print(f"✅ Cleared cache: {pycache_path}")
        
        # শুধু .py ফাইল লোড করুন
        plugins = [f[:-3] for f in os.listdir(plugin_dir) 
                  if f.endswith(".py") and f != "__init__.py" and f != "pay.py"]
        
        for plugin in plugins:
            try:
                # পুরনো মডিউল আনলোড করুন
                if f"plugins.{plugin}" in sys.modules:
                    del sys.modules[f"plugins.{plugin}"]
                
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
    
    await stop_client()
    loop = asyncio.get_event_loop()
    loop.stop()

async def main():
    """Main function"""
    await load_and_run_plugins()
    print("🤖 Bot is running...")
    while True:
        await asyncio.sleep(1)

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    signal_name = signal.Signals(signum).name
    print(f"\n📡 Received signal: {signal_name}")
    loop = asyncio.get_event_loop()
    if loop.is_running():
        asyncio.create_task(shutdown(signal_name))
    else:
        loop.run_until_complete(shutdown(signal_name))

def run_flask():
    """Flask app চালানোর জন্য আলাদা থ্রেড"""
    os.system("python app.py")

if __name__ == "__main__":
    # Flask ব্যাকগ্রাউন্ডে চালান
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    print("🌐 Flask router started on port 10000")
    
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
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
            loop.run_until_complete(asyncio.sleep(0.3))
            loop.close()
            print("✅ Event loop closed successfully")
        except Exception as e:
            print(f"⚠️ Cleanup error: {e}")
