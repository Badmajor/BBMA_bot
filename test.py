import asyncio

from util.bot_functions import catch_signal, get_arg_list

cycle_list = [asyncio.ensure_future(catch_signal(i)) for i in get_arg_list()]

event_loop = asyncio.get_event_loop()

event_loop.run_until_complete(asyncio.gather(*cycle_list))