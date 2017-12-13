#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "longyucen"
# Date: 2017/11/24
# 通道metrics监控
# 通过数据库直接访问
# 每60s监控一次
import time
import os
import sys
base_dir = os.path.dirname(os.path.abspath(__file__))
# print(base_dir)
sys.path.append(base_dir)
import conn_oop
import falcon_oop

sql = '''SELECT CASE WHEN t.`channel`='cardinfo' THEN '卡友' WHEN t.`channel`='zx-posp' THEN '众鑫' END AS chl,
SUM(CASE WHEN t.trade_result='00' THEN t.result_num ELSE 0 END) AS success_num,
SUM(CASE WHEN t.trade_result NOT IN ('51','75','00','55') THEN t.result_num ELSE 0 END) AS error_num,
ROUND(SUM(CASE WHEN t.trade_result NOT IN ('51','75','00','55') THEN t.result_num ELSE 0 END)/SUM(t.result_num),4) AS error_percnt,
GROUP_CONCAT(CASE WHEN t.trade_result NOT IN ('51','75','00','55') 
             THEN CONCAT('结果码:[',t.trade_result,']-',t.result_num) ELSE NULL END)AS res_code
FROM (
SELECT a.channel,a.trade_result,COUNT(*) AS result_num
FROM `mercht_route_xft`.`trade_flow` a 
WHERE a.trade_time>SUBDATE(NOW(),INTERVAL 15 MINUTE) AND a.trade_time<NOW()
AND a.channel IN ('zx-posp','cardinfo')
GROUP BY channel,a.trade_result
) t
GROUP BY t.channel'''


def run():
    """
    判读是否在工作时间内
    :return:
    """
    begin_t, last_t = ('06:00:00', '20:59:59')
    begin_t = time.mktime(time.strptime(begin_t, '%H:%M:%S'))
    last_t = time.mktime(time.strptime(last_t, '%H:%M:%S'))
    while True:
        curen_t = time.strftime('%H:%M:%S', time.localtime(time.time()))
        curen_t = time.mktime(time.strptime(curen_t, '%H:%M:%S'))
        # print(begin_t, last_t, curen_t)
        connect = conn_oop.FalconRun("106.15.208.12", "alter", "666666", 3306, sql, "td_metics")
        re = connect.conn()
        # print(re)
        for value in re:
            name = 'TD' + value[0]  #通道名称
            metric = str(value[3])  #通道出错比例
            metric_name = name
            step = 60  # falcon获取值时间
            tags = "TD Monitor"
            # print(name, metric, step)
            insert = falcon_oop.FalconMain(name, metric_name, metric, step, tags)
            re = insert.td()
            # print(re)
            # exit()
            if last_t > curen_t > begin_t:
                # print('工作时间')
                time.sleep(60)
            else:
                # print('工作时间外')
                time.sleep(900)
