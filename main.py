import threading
import time

from data.const import symbol_tuple, tf_tuple, tf_dict
from util.bot_functions import catch_signal

threads = []
arg_list = []

for s in symbol_tuple:
    for t in tf_tuple:
        arg_list.append((s, t))

if __name__ == '__main__':
    for i in arg_list:
        t = thread = threading.Thread(name=f'{i[0]+str(i[1])}', target=catch_signal, args=(i, ))
        threads.append(t)
        t.start()
    print(threads)
