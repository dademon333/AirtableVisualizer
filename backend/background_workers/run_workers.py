import asyncio
import signal
import threading

from .cache_updater import CacheUpdater
from .database_backuper import DatabaseBackuper


async def run_workers():
    threading.Thread(
        target=asyncio.run,
        args=(CacheUpdater.init(),),
        daemon=True
    ).start()
    threading.Thread(target=DatabaseBackuper.init, daemon=True).start()

    signal.signal(signal.SIGTERM, lambda: ...)
    signal.pause()


asyncio.run(run_workers())
