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
    while True:
        sql = """select count(*) from  posp_route.t_trade_flow where t_trade_flow.TRADE_TIME>date_sub(sysdate(),interval 2 minute) 
    and state='2'"""
        result = conn.f_trade(sql)
        falcon.df('failed', result[0])
        # print('td_df')
        time.sleep(120)


