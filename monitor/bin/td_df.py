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
import logging
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(base_dir)
sys.path.append(base_dir)
from bin import falcon_oop
from conf import dbconfig
from conf import mysql_conn
logging.basicConfig(filename=base_dir + '/logs/df.log', level=logging.INFO,\
                    format='%(asctime)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S')


def mysql(sql):
    pro_config = dbconfig.al_pro_config()
    al_conn = mysql_conn.DbConnect(pro_config, sql, '代付模块')
    re = al_conn.select()
    return re


def run():
    """
    2分钟查询失败笔数
    :return:
    """
    id_sql = 'select max(id) from  posp_route.t_trade_flow'
    result = mysql(id_sql)
    start_id = result[0][0]
    # print(start_id)
    while True:
        try:
            time.sleep(120)
            result = mysql(id_sql)
            end_id = result[0][0]
            # print(end_id)
            sql = """select count(*) from  posp_route.t_trade_flow where id>= %s \
                   and id<= %s and  state='2'""" % (start_id, end_id)
            result = mysql(sql)
            logging.info('代付失败数量：%s' % result[0][0])
            update = falcon_oop.FalconMain("DF", "DFfailed", result[0][0], 60, "DF Error Type")
            re_update = update.td()
            logging.info("代付失败数据上传Falcon：%s" % re_update)
            start_id = end_id
        except Exception as e:
            logging.error('代付失败数量查询错误：%s' % e)
        # print('td_df')
#
#
# run()

