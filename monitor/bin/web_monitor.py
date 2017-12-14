#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "longyucen"
# Date: 2017/12/11

import time
import os
import sys
import requests
import logging
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
from bin import conn
from bin import falcon
logging.basicConfig(filename=base_dir + '/logs/w_monitor.log', level=logging.INFO, \
                    format='%(asctime)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
# print(base_dir + '/logs/w_monitor.log')


def run():
    try:
        while True:
            sql = """select w_name,w_path from monitor.w_monitor"""
            re_sql = conn.w_conn(sql)
            # print(re_sql)
            for value in re_sql:
                # print(value)
                app = value[0]
                path = value[1]
                code = requests.get(path).status_code
                if code == 200:
                    falcon.w_monitor(app, 0)
                else:
                    falcon.w_monitor(app, 1)
            time.sleep(600)
    except:
        logging.exception('ERROR')
