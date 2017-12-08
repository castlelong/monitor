#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "longyucen"
# Date: 2017/11/27
import os
import sys
import threading
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(base_dir)
sys.path.append(base_dir)

from bin import td_merics
from bin import td_df
from bin import merchart


threads = []
t1 = threading.Thread(target=td_merics.run, args=())
threads.append(t1)
t2 = threading.Thread(target=td_df.run, args=())
threads.append(t2)
t3 = threading.Thread(target=merchart.insert_merch_all, args=())
threads.append(t3)


if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()


