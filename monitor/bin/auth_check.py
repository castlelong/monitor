#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "longyucen"
# Date: 2017/12/20

import os
import sys
import logging
import time

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
log_file = base_dir + '/logs/auth_check.log'
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(message)s', \
                    datefmt='%Y/%m/%d %H:%M:%S')
from conf import dbconfig
from conf import mysql_conn

sql = """SELECT AVG(t.bet_time) AS avg_time,#平均时间
COUNT(*) AS total_num,#总次数
SUM(CASE WHEN t.`AUTHENTICATION_STATE`='4' THEN 1 ELSE 0 END) AS succ_num,#成功次数
SUM(CASE WHEN t.`AUTHENTICATION_STATE`='4' THEN 1 ELSE 0 END)/COUNT(*) AS succ_percent #成功比例
FROM (
SELECT TIMESTAMPDIFF(SECOND,a.`GMT_AUTH_APPLY`,(SELECT MIN(t.`GMT_AUTH_TIME`) FROM leacrm.`t_e_auth_info_history` t
	WHERE t.`MEMBER_NO`=a.`MEMBER_NO` AND t.`GMT_AUTH_TIME`>SYSDATE()-INTERVAL 2 DAY
	AND t.GMT_AUTH_TIME>a.`GMT_AUTH_APPLY`)) AS bet_time,
     a.`AUTH_APPLY_USER_ID`,a.`AUTHENTICATION_STATE`
FROM leacrm.`lyj_member_info` a
  WHERE a.`GMT_AUTH_APPLY`>SYSDATE()-INTERVAL 1 HOUR
  AND DATE_FORMAT(a.GMT_AUTH_APPLY,'%H:%i:%s')>'09:00:00'
  AND DATE_FORMAT(a.GMT_AUTH_APPLY,'%H:%i:%s')<'20:55:00'
  AND a.`AUTH_APPLY_USER_ID` IS NOT  NULL
)t"""


def run():
    try:
        pro_config = dbconfig.al_pro_config()
        monitor_config = dbconfig.monitor_config()
        while True:
            select_conn = mysql_conn.DbConnect(pro_config, sql, 'auth_check')
            re = select_conn.select()
            value_list = []
            for value in re[0]:
                # print(value)
                value_list.append(value)
            logging.info('auth_check module %s' % value_list)
            sql_insert = """insert into monitor.auth_check (total, avg_time, succ_num, succ_percent) \
                        VALUES ('%s', '%s', '%s','%s')""" % (value_list[1], value_list[0], value_list[2], value_list[3])
            insert_conn = mysql_conn.DbConnect(monitor_config, sql_insert, 'auth_check')
            insert_conn.insert()
            time.sleep(3600)
    except Exception as e:
        logging.info(e)