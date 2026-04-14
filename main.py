# Copyright (c) 2025 devgagan : https://github.com/devgaganin.  
# Licensed under the GNU General Public License v3.0.  
# See LICENSE file in the repository root for full license text.

import asyncio
from shared_client import start_client, stop_client
import importlib
import os
import sys
import signal

async def load_and_run_plugins():
    await start_client()
    plugin_dir = "plugins"
    plugins = [f[:-3] for f in os.listdir(plugin_dir) if f.endswith(".py") and f != "__init__.py"]

    for plugin in plugins:
        module = importlib.import_module(f"plugins.{plugin}")
        if hasattr(module, f"run_{plugin}_plugin"):
            print(f"Running {plugin} plugin...")
            await getattr(module, f"run_{plugin}_plugin")()  

async def shutdown(signal_name=None):
    """Gracefully shutdown the bot"""
    print(f"\n{signal_name} received. Shutting down gracefully...")
    
    # Stop the client
    try:
        await stop_client()
        print("Client stopped successfully")
    except Exception as e:
        print(f"Error stopping client: {e}")
    
    # Cancel all pending tasks
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    print(f"Cancelling {len(tasks)} pending tasks...")
    
    for task in tasks:
        task.cancel()
    
    # Wait for all tasks to complete cancellation
    await asyncio.gather(*tasks, return_exceptions=True)
    print("All tasks cancelled")
    
    # Stop the event loop
    loop = asyncio.get_event_loop()
    loop.stop()

async def main():
    await load_and_run_plugins()
    while True:
        await asyncio.sleep(1)

def handle_shutdown(signum, frame):
    """Handle shutdown signals"""
    signal_name = signal.Signals(signum).name
    print(f"\nReceived signal: {signal_name}")
    
    # Create task for shutdown
    loop = asyncio.get_event_loop()
    if loop.is_running():
        loop.create_task(shutdown(signal_name))
    else:
        loop.run_until_complete(shutdown(signal_name))

if __name__ == "__main__":
    # Register signal handlers
    signal.signal(signal.SIGINT, handle_shutdown)   # Ctrl+C
    signal.signal(signal.SIGTERM, handle_shutdown)  # Termination signal (Render uses this)
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    print("Starting clients ...")
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("KeyboardInterrupt received")
    except asyncio.CancelledError:
        print("Tasks cancelled")
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)
    finally:
        try:
            # Give some time for cleanup
            loop.run_until_complete(asyncio.sleep(0.5))
            loop.close()
            print("Event loop closed")
        except Exception as e:
            print(f"Error closing loop: {e}")
