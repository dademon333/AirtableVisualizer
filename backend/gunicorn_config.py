import asyncio
import threading

import psutil

from airtable.synchronizer import airtable_synchronizer
from config import Config


def when_ready(_):
    """Запускает глобальных background worker`ов

    Они синхронизируют базу с airtable, кэшируют данные и тд
    Должны находиться в master процессе
    """
    threading.Thread(target=asyncio.run, args=(airtable_synchronizer(),), daemon=True).start()


worker_class = 'uvicorn.workers.UvicornWorker'
raw_env = ['PYTHONUNBUFFERED=1']

if Config.DEBUG:
    certfile = './ssl/certificate.pem'
    keyfile = './ssl/key.pem'
    bind = '0.0.0.0:443'
    workers = 1
else:
    bind = 'localhost:8000'
    workers = psutil.cpu_count(logical=False) * 2 + 1
