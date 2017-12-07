#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "longyucen"
# Date: 2017/7/19
# 错误清单导入模块

from xlrd import open_workbook
import pymysql
import contextlib

@contextlib.contextmanager
def mysql(host='10.200.201.101', port=3306, user='root', passwd='123456', db='tdcode', charset='utf8'):
    db = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
    cur = db.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        yield cur
    finally:
        db.commit()
        cur.close()
        db.close()

data = open_workbook('qd-1.xlsx')
table = data.sheets()[0]
data_list = []
nrows = table.nrows
for rownum in range((table.nrows)):
    if rownum == 0:
        pass
    else:
        key = table.row_values(rownum)[0]
        describe = table.row_values(rownum)[1]
        if table.row_values(rownum)[2]:
            one_hour = int(table.row_values(rownum)[2])
        else:
            one_hour = 0
        if table.row_values(rownum)[3]:
            two_min = int(table.row_values(rownum)[3])
        else:
            two_min = 0
        with mysql() as key_list:
            sql = "select 1 from td_monitor_list where td_monitor_list.`describe` = %s " \
                  "and td_monitor_list.`key` = %s"
            key_list.execute(sql, (describe, key))
            result = key_list.fetchone()
            print(result)
            if result:
                pass
            else:
                print('ok')
                with mysql() as cur:
                    cur.execute(
                        "INSERT INTO td_monitor_list (`key`, `describe`, `one_hour`, `two_min`)"
                        "VALUES(%s, %s, %s, %s)", (key, describe, one_hour, two_min))