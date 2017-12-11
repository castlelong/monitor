#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "longyucen"
# Date: 2017/12/11

import time
import os
import sys
import requests
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
from bin import conn
from bin import falcon


def run():
    while True:
        sql = """select w_name,w_path from monitor.w_monitor"""
        re_sql = conn.conn(sql)
        key_list = []
        for key in re_sql:
            key_list.append(key)
        for value in key_list:
            app = value[0]
            path = value[1]
            code = requests.get(path).status_code
            if code == 200:
                falcon.w_monitor(app, 0)
            else:
                falcon.w_monitor(app, 1)
    time(600)

