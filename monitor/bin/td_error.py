#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "longyucen"
# Date: 2017/12/1
import time
import os
import sys
import logging
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(base_dir)
sys.path.append(base_dir)
from bin import conn


def run():
    start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    start_time = int(time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M:%S')))
    while True:
        time.sleep(20)
        end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        end_time = int(time.mktime(time.strptime(end_time, '%Y-%m-%d %H:%M:%S')))
        sql = 'select type_name, type_count , insert_date from td_error_type where unix_timestamp(insert_date)> %s \
               and unix_timestamp(insert_date)< %s' % (start_time, end_time)
        result = conn.td_monitor(sql)
        start_time = end_time


run()
