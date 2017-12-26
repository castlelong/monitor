#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "longyucen"
# Date: 2017/12/8
import time
import urllib.request
import json
import os
import sys
import logging
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
from conf import dbconfig
from conf import mysql_conn

logging.basicConfig(filename=base_dir + 'merchant.log', level=logging.INFO, \
                    format='%(asctime)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S')

config = dbconfig.monitor_config()


def insert_merch_all():
    """

    :return: 返回数据操作是否成功
    """
    while True:
        # fp = urllib.request.urlopen("http://10.200.201.69:16901/posp-route/metricsService.do")
        fp = urllib.request.urlopen("http://172.19.24.136:9095/merchantroute/metricsService/getMercStat")
        data_bytes = fp.read()
        data_str = data_bytes.decode("utf-8")
        data = json.loads(data_str)
        cardinfo_data = data['cardinfo']['ALL']
        zxposp_data = data['zx-posp']['ALL']
        logging.info('cardinfo:%s' % cardinfo_data)
        logging.info('zxposp:%s' % zxposp_data)
        insert_card_sql = """insert into mercht.mercht_all (disctTrdamt,totalTrdamt,rate,channel)\
                          VALUES ('%s','%s','%s','%s')""" \
                          % (cardinfo_data['disctTrdamt'], cardinfo_data['totalTrdamt'], cardinfo_data['rate'], 'cardinfo')
        insert_zx_sql = """insert into mercht.mercht_all (disctTrdamt,totalTrdamt,rate,channel)\
                          VALUES ('%s','%s','%s','%s')""" \
                        % (
                            zxposp_data['disctTrdamt'], zxposp_data['totalTrdamt'], zxposp_data['rate'], 'zx-posp')
        cardinfo_conn = mysql_conn.DbConnect(config, insert_card_sql, 'cardinfo_data')
        re_cardinfo = cardinfo_conn.insert()
        logging.info('cardinfo update data: %s' % re_cardinfo)
        zx_conn = mysql_conn.DbConnect(config, insert_zx_sql, 'zx')
        re_zx = zx_conn.insert()
        logging.info('zx update data:%s' % re_zx)
        time.sleep(900)
