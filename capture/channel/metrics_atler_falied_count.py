#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "longyucen"
# Date: 2017/6/29
import pymysql
import contextlib
import time
import datetime

# 定义上下文管理器，连接后自动关闭连接


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


with mysql() as count_failed:
    while True:
        for i in range(2):
            result_list = []
            now = datetime.datetime.now()
            date = now + datetime.timedelta(seconds=-10)
            date = date.strftime("%Y-%m-%d %H:%M:%S")
            count_failed.execute("select ifnull(sum(count.failed),0) as failed from count "
                                 "where insert_data > %s", (date))
            failed_result = count_failed.fetchone()
            result_list.append(failed_result['failed'])
            print(failed_result['failed'])
            if failed_result['failed'] == 0:
                print(0)
            elif failed_result['failed'] >= 10:
                print(1)
            time.sleep(10)
        count_data = result_list[0] + result_list[1]
        print(count_data)
        print(result_list)
        if count_data == 0:
            print(0)
        # 为2表示20秒类出现的错误数
        elif count_data >= 10:
            print(2)
        time.sleep(10)

