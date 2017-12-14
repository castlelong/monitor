#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "longyucen"
# Date: 2017/6/19

import time
import urllib.request
import json
import os
import sys
import logging

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)


from conf import mysql_conn
from conf import dbconfig
logging.basicConfig(filename=base_dir + '/logs/draw_monitor.log', level=logging.INFO, \
                    format='%(asctime)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S')


def key_list():
    """
    消费清单
    :return: 清单返回
    """
    try:
        sql = "select key_name,list_id from tdcode.td_draw_kye_list"
        config = dbconfig.monitor_config()
        # print(config)
        conn = mysql_conn.DbConnect(config, sql, '清单查询')
        result = conn.select()
        name_list = []
        name_id =[]
        for k in result:
            name_list.append(k[0])
            name_id.append(k[1])
        name_result = dict(zip(name_list, name_id))
        # print(name_result)
        return name_result
    except Exception as error:
        logging.exception('draw_metrics select key_list:', error)


def mysql_insert_data(xf_type, key_id, insert_time):
    """
    数据库插入数据
    :param xf_type: 消费类型数据
    :return: 无返回值
    """
    try:
        insert_data_sql = "insert into tdcode.td_draw_data (insert_date, oneMinuteRate, fiveMinuteRate, fifteenMinuteRate, meanRate,count_data,xf_name_id)\
               VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
              (insert_time, xf_type['oneMinuteRate'], xf_type['fiveMinuteRate'], xf_type['fifteenMinuteRate'],\
                 xf_type['meanRate'], xf_type['count'], key_id)
        # print(insert_data_sql)
        # logging.info('消费类型数据:%s,消费类型ID：%s' % (xf_type, key_id))
        # print('insert_data:%s', insert_data_sql)
        config = dbconfig.monitor_config()
        conn = mysql_conn.DbConnect(config, insert_data_sql, 'draw_metrics_data')
        conn.insert()
    except Exception as error:
        logging.exception('insert draw_metrics data:', error)


def run():
    xf_list = key_list()
    while True:
        try:
            fp = urllib.request.urlopen("http://172.19.24.139:16901/posp-route/metricsService.do?type=2")
            data_bytes = fp.read()
            # logging.info('数据长度：%s', len(data_bytes))
            if len(data_bytes) > 0:
                data_str = data_bytes.decode("utf-8")
                data = json.loads(data_str)
                for xf_name in xf_list:
                    if xf_name in data.keys():
                        logging.info('消费类型：%s' % xf_name)
                        xf_data = data[xf_name]
                        xf_id = xf_list[xf_name]
                        mysql_insert_data(xf_data, xf_id, data['nowTime'])
                time.sleep(600)
            else:
                time.sleep(600)
                continue
        except Exception as error:
            logging.exception("draw_metrics error:", error)
