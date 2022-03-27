import asyncio
import logging
import tracemalloc

from loader import dp, bot
from util.bot_functions import watch_mt5

import handlers

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    watch_mt5()
    dp.run_polling(bot)
