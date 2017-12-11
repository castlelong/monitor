#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "longyucen"
# Date: 2017/12/5
"""
代付模块监控
"""
import sys
import os
import time
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(base_dir)
sys.path.append(base_dir)
from bin import conn
from bin import falcon


def run():
    """
    2分钟查询失败笔数
    :return:
    """
    start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    start_time = int(time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M:%S')))
    while True:
        time.sleep(120)
        end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        end_time = int(time.mktime(time.strptime(end_time, '%Y-%m-%d %H:%M:%S')))
        sql = """select count(*) from  posp_route.t_trade_flow where unix_timestamp(t_trade_flow.TRADE_TIME)> %s \
               and unix_timestamp(t_trade_flow.TRADE_TIME)< %s and  state='2'""" % (start_time, end_time)
        # print(sql)
        # exit()
        result = conn.f_trade(sql)
        falcon.df('failed', result[0])
        start_time = end_time
        # print('td_df')

# run()

