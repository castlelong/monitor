#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "longyucen"
# Date: 2017/6/19

import time
import urllib.request
import json
import os
import sys
import conn
import logging

base_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_dir)
logging.basicConfig(filename=base_dir + '/logs/monitor.log', level=logging.INFO, \
                    format='%(asctime)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S')


def key_list():
    """
    消费清单
    :return: 清单返回
    """
    sql = "select key_name,list_id from td_kye_list"
    result = conn.mysql_select(sql)
    name_list = []
    name_id =[]
    for k in result:
        name_list.append(k['key_name'])
        name_id.append(k['list_id'])
    name_result = dict(zip(name_list, name_id))
    return name_result


def mysql_insert_data(xf_type, xf_id):
    """
    数据库插入数据
    :param xf_type: 消费类型
    :return: 无返回值
    """
    insert_data_sql = "insert into tdcode.td_data (insert_date, oneMinuteRate, fiveMinuteRate, fifteenMinuteRate, meanRate,count_data,xf_name_id)\
           VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
          (data['nowTime'], xf_type['oneMinuteRate'], xf_type['fiveMinuteRate'], xf_type['fifteenMinuteRate'],\
             xf_type['meanRate'], xf_type['count'], xf_id)
    logging.info('消费类型数据:%s', xf_type)
    # print('insert_data:%s', insert_data_sql)
    conn.mysql_insert(insert_data_sql)


def mysql_insert_count():
    """
    插入每次成功失败统计数据
    :return:
    """
    insert_count_sql = "insert into tdcode.td_count (insert_date, success,  failed) \
          VALUES('%s', '%s', '%s')" % (data['nowTime'], data['success']['value'], (data['failed']['value']-i))
    logging.info('消费成功数据：%s，失败数据：%stai' % (data['success']['value'], data['failed']['value']))
    # print('insert_count:%s', insert_count_sql)
    conn.mysql_insert(insert_count_sql)


def mysql_insert_error_data():
    """
    插入消费错误统计
    :return:
    """
    # 如果'errorResult'有值，则执行插入
    if data['errorResult']:
        for type_name in data['errorResult']:
            if len(type_name) >= 4:
                continue
            else:
                insert_error_sql = "insert into tdcode.td_error_type(type_name, type_count, insert_date) \
                       VALUES ('%s','%s','%s')" % (type_name, data['errorResult'][type_name], data['nowTime'])
                logging.info('错误类型:%s', type_name)
                # print('insert_error:%s', insert_error_sql)
                conn.mysql_insert(insert_error_sql)
    else:
        pass


xf_list = key_list()
while True:
    # fp = urllib.request.urlopen("http://10.200.201.69:16901/posp-route/metricsService.do")
    fp = urllib.request.urlopen("http://172.19.24.139:16901/posp-route/metricsService.do?type=1")
    data_bytes = fp.read()
    # logging.info('数据长度：%s', len(data_bytes))
    if len(data_bytes) > 0:
        data_str = data_bytes.decode("utf-8")
        data = json.loads(data_str)
        # print(data)
        if data['failed']['value'] == 0 and data['success']['value'] == 0:
            pass
        else:
            for xf_name in xf_list:
                if xf_name in data.keys():
                    if xf_name == 'paidTimer':
                        df_data = data[xf_name]
                        logging.info('代付数据为：%s', df_data)
                    else:
                        xf_data = data[xf_name]
                        xf_id = xf_list[xf_name]
                        mysql_insert_data(xf_data, xf_id)
            mysql_insert_error_data()
            mysql_insert_count()
        # print(data)
        time.sleep(10)
    else:
        time.sleep(10)
        continue


