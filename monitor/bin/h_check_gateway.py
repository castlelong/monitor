#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "longyucen"
# Date: 2017/12/11

"""
1、注册数的统计
2、登陆数的统计
"""


import os
import sys
import logging
import time
import traceback
base_dir = os.path.dirname((os.path.dirname(os.path.abspath(__file__))))
sys.path.append(base_dir)
# print(base_dir)
from bin import conn
from bin import insert_conn

logging.basicConfig(filename=base_dir + '/logs/c_gateway.log', level=logging.INFO, format='%(asctime)s %(message)s', \
                    datefmt='%Y/%m/%d %H:%M:%S')


def run():
    """
    统计10分钟内注册数
    统计10分钟内登陆数
    :return:
    re_reg 返回10分钟类注册数量
    re_login 返回10分钟登陆数量
    """
    start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    start_time = int(time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M:%S')))
    try:
        while True:
            time.sleep(600)
            end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            end_time = int(time.mktime(time.strptime(end_time, '%Y-%m-%d %H:%M:%S')))
            sql_reg = """SELECT count(*) from leacrm.lyj_member_info a
        where unix_timestamp(a.CREAT_TIME) >'%s' and unix_timestamp(a.CREAT_TIME)<'%s';""" % (start_time, end_time)
            sql_loggin = """SELECT count(*) from leacrm.member_extend_info a
            where unix_timestamp(a.login_time) >'%s' and unix_timestamp(a.login_time)< '%s'""" % (start_time, end_time)
            re_reg = conn.f_trade(sql_reg)
            re_login = conn.f_trade(sql_loggin)
            insert_sql = """insert into monitor.c_gateway (reg,login) VALUES ('%s','%s')""" % (re_reg[0], re_login[0])
            # print(insert_sql)
            insert_conn.insert_trade(insert_sql)
            logging.info('注册数：%s,登陆数：%s' % (re_reg, re_login))
            start_time = end_time
    except:
        logging.exception("Exception Logged")




