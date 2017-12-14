#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "longyucen"
# Date: 2017/12/11

"""
1、注册数的统计
2、登陆数的统计
"""
import os
import sys
import logging
import time

base_dir = os.path.dirname((os.path.dirname(os.path.abspath(__file__))))
sys.path.append(base_dir)
# print(base_dir)
from conf import dbconfig
from conf import mysql_conn
log_file = base_dir + '/logs/c_gateway.log'
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s %(message)s', \
                    datefmt='%Y/%m/%d %H:%M:%S')


def run():
    """
    统计10分钟内注册数
    统计10分钟内登陆数
    :return:
    re_reg 返回10分钟类注册数量
    re_login 返回10分钟登陆数量
    """
    start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    start_time = int(time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M:%S')))
    try:
        pro_config = dbconfig.al_pro_config()
        monitor_config = dbconfig.monitor_config()
        while True:
            time.sleep(600)
            end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            end_time = int(time.mktime(time.strptime(end_time, '%Y-%m-%d %H:%M:%S')))
            sql_reg = """SELECT count(*) from leacrm.lyj_member_info a
            where unix_timestamp(a.CREAT_TIME) >'%s' and unix_timestamp(a.CREAT_TIME)<'%s';""" % (start_time, end_time)
            sql_loggin = """SELECT count(*) from leacrm.member_extend_info a
            where unix_timestamp(a.login_time) >'%s' and unix_timestamp(a.login_time)< '%s'""" % (start_time, end_time)
            sql_msg_send = """SELECT count(*) from leagotone.gt_sms_out a
            where unix_timestamp(a.GMT_CREATE) >'%s' and unix_timestamp(a.GMT_CREATE)< '%s'""" % (start_time, end_time)
            sql_msg_succ = """SELECT count(*) from leagotone.gt_sms_out a
            where a.`STATUS`='S' and unix_timestamp(a.GMT_CREATE) >'%s' and unix_timestamp(a.GMT_CREATE)< '%s'""" % (start_time, end_time)
            sql_check_count = """SELECT count(*) from preroute.member_verify_his a
            where unix_timestamp(a.GMT_CREATE) >'%s' and unix_timestamp(a.GMT_CREATE)< '%s'""" % (start_time, end_time)
            sql_check_succ = """SELECT count(*) from preroute.member_verify_his a
            where a.is_success=1 and unix_timestamp(a.GMT_CREATE) >'%s' and unix_timestamp(a.GMT_CREATE)< '%s'""" % (start_time, end_time)
            sql_list = [sql_reg, sql_loggin, sql_msg_send, sql_msg_succ, sql_check_count, sql_check_succ]
            value_list = []
            for sql in sql_list:
                select_conn = mysql_conn.DbConnect(pro_config, sql, 'check_gateway')
                result = select_conn.select()
                value_list.append(result[0][0])
            logging.info('gateway data %s' % value_list)
            insert_sql = """insert into monitor.c_gateway (reg,login,msg_send,msg_succ,check_count,check_succ) \
            VALUES ('%s','%s','%s','%s','%s','%s')""" \
            % (value_list[0], value_list[1], value_list[2], value_list[3], value_list[4], value_list[5])
            insert_conn = mysql_conn.DbConnect(monitor_config, insert_sql, 'check_gateway')
            re = insert_conn.insert()
            logging.info('gateway update data:%s' % re)
            start_time = end_time
    except Exception as error:
        logging.exception("Exception Logged", error)

