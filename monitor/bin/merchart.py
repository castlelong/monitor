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
# print(base_dir)
# exit()
sys.path.append(base_dir)
from bin import insert_conn


def insert_merch_all():
    while True:
        # fp = urllib.request.urlopen("http://10.200.201.69:16901/posp-route/metricsService.do")
        fp = urllib.request.urlopen("http://172.19.24.136:9095/merchantroute/metricsService/getMercStat")
        data_bytes = fp.read()
        data_str = data_bytes.decode("utf-8")
        data = json.loads(data_str)
        cardinfo_data = data['cardinfo']['ALL']
        zxposp_data = data['zx-posp']['ALL']
        insert_card_sql = """insert into mercht.mercht_all (disctTrdamt,totalTrdamt,rate,channel)\
                          VALUES ('%s','%s','%s','%s')""" \
                          % (cardinfo_data['disctTrdamt'], cardinfo_data['totalTrdamt'],cardinfo_data['rate'], 'cardinfo')
        insert_zx_sql = """insert into mercht.mercht_all (disctTrdamt,totalTrdamt,rate,channel)\
                          VALUES ('%s','%s','%s','%s')""" \
                        % (
                            zxposp_data['disctTrdamt'], zxposp_data['totalTrdamt'], zxposp_data['rate'], 'zx-posp')
        insert_conn.insert_trade(insert_card_sql)
        insert_conn.insert_trade(insert_zx_sql)
        time.sleep(900)


insert_merch_all()