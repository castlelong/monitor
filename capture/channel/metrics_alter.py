#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "longyucen"
# Date: 2017/7/20

import contextlib
import pymysql
import time
import datetime


@contextlib.contextmanager
def mysql(host='127.0.0.1', port=3306, user='root', passwd='123456', db='test', charset='utf8'):
    db = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
    cur = db.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        yield cur
    finally:
        db.commit()
        cur.close()
        db.close()


now = datetime.datetime.now()
date_fi = now + datetime.timedelta(minutes=-15)
date_fi = date_fi.strftime("%Y-%m-%d %H:%M:%S")
date_ho = now + datetime.timedelta(minutes=-60)
date_ho = date_ho.strftime("%Y-%m-%d %H:%M:%S")
with mysql() as cur_fi:
    sql = "select  test.error_type.type_name, test.error_type.type_count" \
          " from test.error_type WHERE insert_date > %s"
    cur_fi.execute(sql, date_fi)
with mysql() as cur_ho:
    sql = "select  test.error_type.type_name, test.error_type.type_count" \
          " from test.error_type WHERE insert_date > %s"
    cur_ho.execute(sql, date_ho)