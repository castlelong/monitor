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

# 执行查询10分钟交易成功率统计
while True:
    # 获取比当前时间小的时间
    now = datetime.datetime.now()
    date = now + datetime.timedelta(minutes=-10)
    date = date.strftime("%Y-%m-%d %H:%M:%S")
    # 求统计成功率
    with mysql() as count_fif:
        count_fif.execute("select ifnull(sum(count.success),0) as success, "
                          "ifnull(sum(count.failed),0) as failed from count "
                          "where insert_data > %s", (date))
        result = count_fif.fetchone()
        print(result['success'], result['failed'])
        count = result['success'] + result['failed']
        # 统计成功率,1表示失败 0表示成功
        # 若无失败和成功数据表示无错误
        # 若成功失败数据和小于100则不报错
        if result['success'] == 0 and result['failed'] == 0:
            print(0)
        else:
            pre_count = float('%.4f' % (result['success'] / count))
            print(pre_count)
            # 如果成功率达到100%且成功笔数大于10，则触发报警
            if pre_count == 1.0 and result['success'] >= 10:
                print(1)
            # 成功率小于90%报警
            elif pre_count < 0.9 and count >= 100:
                print(1)
            else:
                print(0)
    time.sleep(600)




