#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "longyucen"
# Date: 2017/7/3

import pymysql
import contextlib
import time

# 定义上下文管理器，连接后自动关闭连接


@contextlib.contextmanager
def mysql(host='localhost', port=3306, user='root', passwd='123456', db='test', charset='utf8'):
    db = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
    cur = db.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        yield cur
    finally:
        db.commit()
        cur.close()
        db.close()


with mysql() as count:
    count.execute("select SUM(count.success) as success ,SUM(count.failed) as failed from count "
                  "where insert_data > DATE_ADD(NOW(), INTERVAL -24 HOUR)")
    result = count.fetchone()
    success_rate = float('%.2f' % (result['success'] / (result['success']+result['failed'])))
    date_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(success_rate)
    print(date_now)
    count.execute("insert into day_count (rate, insert_date) "
                  "VALUES (%s, %s)", (success_rate, date_now))


with mysql() as count_type:
    count_type.execute("select type_name,sum(type_count) as count from test.error_type "
                      "where insert_date > DATE_ADD(NOW(), INTERVAL -24 HOUR) GROUP BY type_name")
    type_result = count_type.fetchall()
    print(type_result)
    key_name = []
    key_num = []
    for key in type_result:
        key_name.append(key['type_name'])
        key_num.append(key['count'])
    # 统计列表中的数值
    count_data = 0
    for a in key_num:
        count_data += a
    key_dict =dict(zip(key_name, key_num))
    for key in key_dict:
        count_rate = float("%.2f" % (key_dict[key]/count_data))
        date = time.strftime("%Y-%m-%d", time.localtime())
        count_type.execute("insert into error_count (error_type,count,rate,insert_date)"
                           "VALUES (%s, %s, %s, %s)", (key, key_dict[key], count_rate, date))