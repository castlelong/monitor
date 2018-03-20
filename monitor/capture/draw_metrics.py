#! /usr/bin/env python
# coding: utf-8
# __author__ = "longyucen"
# Date: 2017/6/19
"""
小付的metrics画图程序
"""
import time
import urllib.request
import json
import os
import sys
import logging
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
logger = logging.getLogger('Draw-Metrics')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(base_dir + '/logs/d_metrics.log', encoding="utf-8")
fh = handler
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
from conf import mysql_conn
from conf import dbconfig


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
        name_id = []
        for k in result:
            name_list.append(k[0])
            name_id.append(k[1])
        name_result = dict(zip(name_list, name_id))
        # print(name_result)
        return name_result
    except Exception as error:
        logger.exception('draw_metrics select key_list:', error)


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
        # logger.info('消费类型数据:%s,消费类型ID：%s' % (xf_type, key_id))
        # print('insert_data:%s', insert_data_sql)
        config = dbconfig.monitor_config()
        conn = mysql_conn.DbConnect(config, insert_data_sql, 'draw_metrics_data')
        conn.insert()
    except Exception as error:
        logger.exception('insert draw_metrics data:%s' % error)


def run():
    xf_list = key_list()
    while True:
        try:
            fp = urllib.request.urlopen("http://172.19.24.139:16901/posp-route/metricsService.do?type=2")
            data_bytes = fp.read()
            # logger.info('数据长度：', len(data_bytes))
            if len(data_bytes) > 0:
                data_str = data_bytes.decode("utf-8")
                data = json.loads(data_str)
                for xf_name in xf_list:
                    if xf_name in data.keys():
                        xf_data = data[xf_name]
                        xf_id = xf_list[xf_name]
                        mysql_insert_data(xf_data, xf_id, data['nowTime'])
                        # logger.info("Consumption Type:%s" % xf_name)
                        logger.info("消费类型：%s" % xf_name)
                time.sleep(600)
            else:
                time.sleep(600)
                continue
        except Exception as error:
            logger.exception("draw_metrics error:%s" % error)


run()