#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "longyucen"
# Date: 2017/12/4
import os
import sys
import time
import threading
import logging

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

# print(base_dir)

logging.basicConfig(filename=base_dir + '/logs/trade.log', level=logging.INFO, \
                    format = '%(asctime)s %(message)s', datefmt = '%Y/%m/%d %H:%M:%S')
from bin import conn, insert_conn


def success():
    """
    查询所有用户交易的成功笔数
    :return: 
    """
    while True:
        sql_statement = '''SELECT t.total_num,t.succ_num,ROUND(t.succ_num/t.total_num,4) AS succ_percent
        FROM (SELECT SUM(CASE WHEN STATUS='5' THEN 1 ELSE 0 END) AS succ_num,COUNT(*) AS total_num 
        FROM leatrade.trade_order  WHERE  GMT_CREATE>DATE_SUB(NOW(), INTERVAL 60 MINUTE) AND
        GMT_PAY> DATE_SUB(NOW(), INTERVAL 2 MINUTE)) t;'''
        re = conn.f_trade(sql_statement)
        # insert_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # print(re)
        logging.info('SUCCESS:%s', re)
        sql_insert = '''insert into monitor.f_succ (total_num,succ_num,succ_percent) VALUES('%s','%s','%s')'''\
                     % (re[0], re[1], re[2])
        # print(sql_insert)
        insert_conn.insert_trade(sql_insert)
        time.sleep(120)


def trade_fee():
    """
    查询用户手续费
    :return:
    """
    while True:
        sql_statement = '''SELECT t.biz_code,t.amt,t.fee,ROUND(t.fee/t.amt,4) FROM \
(SELECT biz_code,COALESCE(SUM(profit),0) AS fee,COALESCE(SUM(amount),0) AS amt
FROM leatrade.trade_order  WHERE  GMT_CREATE>DATE_SUB(NOW(), INTERVAL 60 MINUTE) AND
GMT_PAY> DATE_SUB(NOW(), INTERVAL 15 MINUTE) AND STATUS=5
GROUP BY biz_code
) t'''
        re = conn.f_trade(sql_statement)
        logging.info('trade_fee:%s', re)
        sql_insert = '''insert into monitor.f_fee (biz_code,amt,fee,rate) VALUES('%s','%s','%s','%s')'''\
                     % (re[0], re[1], re[2], re[3])
        # print(sql_insert)
        insert_conn.insert_trade(sql_insert)
        time.sleep(900)


def trade_cash():
    """
    用户出款金额
    :return:
    """
    while True:
        sql_statement = '''SELECT t.amt,t.fee,(t.amt-t.fee) as cash FROM 
    (SELECT  COALESCE(SUM(profit),0) AS fee,COALESCE(SUM(amount),0) AS amt FROM leatrade.trade_order  WHERE  
    GMT_CREATE>DATE_SUB(NOW(), INTERVAL 60 MINUTE) AND
    GMT_PAY> DATE_SUB(NOW(), INTERVAL 15 MINUTE) AND STATUS=5
    ) t'''
        re = conn.f_trade(sql_statement)
        logging.info('trade_cash:%s', re)
        sql_insert = '''insert into monitor.f_cash (amt,fee,cash) VALUES('%s','%s','%s')''' \
                     % (re[0], re[1], re[2])
        # print(sql_insert)
        insert_conn.insert_trade(sql_insert)
        time.sleep(900)


threads = []
t1 = threading.Thread(target=success, args=())
threads.append(t1)
t2 = threading.Thread(target=trade_fee, args=())
threads.append(t2)
t3 = threading.Thread(target=trade_cash, args=())
threads.append(t3)


if __name__ == '__main__':
    for t in threads:
        t.setDaemon(True)
        t.start()
    t.join()