import asyncio
import logging
import tracemalloc

from loader import dp, bot


import handlers

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    watch_mt5()
    dp.run_polling(bot)
