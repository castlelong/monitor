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

from bin import td_merics_oop
from bin import td_df
from bin import merchart
from bin import h_check_gateway
from bin import web_monitor
from capture import draw_metrics
from bin import auth_check


threads = []
t1 = threading.Thread(target=td_merics_oop.run, args=())
threads.append(t1)
t2 = threading.Thread(target=td_df.run, args=())
threads.append(t2)
t3 = threading.Thread(target=merchart.insert_merch_all, args=())
threads.append(t3)
t4 = threading.Thread(target=h_check_gateway.run, args=())
threads.append(t4)
t5 = threading.Thread(target=web_monitor.run, args=())
threads.append(t5)
t6 = threading.Thread(target=draw_metrics.run, args=())
threads.append(t6)
t7 = threading.Thread(target=auth_check.run, args=())
threads.append(t7)

if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()
