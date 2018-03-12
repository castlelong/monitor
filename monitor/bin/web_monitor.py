#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "longyucen"
# Date: 2017/12/11

import time
import os
import sys
import requests
import logging
import falcon_oop
from conf import dbconfig
from conf import mysql_conn
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

logging.basicConfig(filename=base_dir + '/logs/w_monitor.log', level=logging.INFO,\
                    format='%(asctime)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
config = dbconfig.monitor_config()


def run():
    try:
        while True:
            sql = """select w_name,w_path from monitor.w_monitor"""
            select_sql = mysql_conn.DbConnect(config, sql, "WEB_Monitor")
            re_sql = select_sql.select()
            # print(re_sql)
            for value in re_sql:
                # print(value)
                app = value[0]
                path = value[1]
                code = requests.get(path).status_code
                if code == 200:
                    metric_value = 0
                else:
                    metric_value = 1
                # 调用falcon_oop,取值
                falcon = falcon_oop.FalconMain("WEB_Monitor", app, metric_value, 600, "WEB_Monitor")
                result = falcon.td()
                # print(result)
                logging.info("web_monitor:%s %s" % (app, result))

            time.sleep(600)
    except Exception as e:
        logging.exception('ERROR:', e)


run()