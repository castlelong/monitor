#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "longyucen"
# Date: 2017/12/4

import pymysql
import contextlib


@contextlib.contextmanager
def conn_monitor(host='10.200.201.101', port=3306, user='root', passwd='123456', charset='utf8'):
    db = pymysql.connect(host=host, port=port, user=user, passwd=passwd, charset=charset)
    cur = db.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        yield cur
    finally:
        db.commit()
        cur.close()
        db.close()


def insert_trade(statment):
    with conn_monitor() as trade:
        trade.execute(statment)
