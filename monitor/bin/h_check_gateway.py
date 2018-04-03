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
logger = logging.getLogger('kf-Monitor')
logger.setLevel(logging.INFO)
fh = logging.FileHandler(base_dir + '/logs/kf_check.log', encoding="utf-8")
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


def run():
    """
    统计10分钟内注册数
    统计10分钟内登陆数
    :return:
    re_reg 返回10分钟类注册数量
    re_login 返回10分钟登陆数量
    """
    try:
        pro_config = dbconfig.al_pro_config()
        monitor_config = dbconfig.monitor_config()
        while True:
            sql_reg = """SELECT count(*) from leacrm.lyj_member_info a
            where a.CREAT_TIME > now() -interval 10 minute"""
            sql_loggin = """SELECT count(*) from leacrm.member_extend_info a
            where a.login_time > now() - interval 10 minute """
            sql_msg_send = """SELECT count(*) from leagotone.gt_sms_out a
            where a.GMT_CREATE > now() - interval 10 minute """
            sql_msg_succ = """SELECT count(*) from leagotone.gt_sms_out a
            where a.STATUS='S' and a.GMT_CREATE > now() -  interval 10 minute"""
            sql_check_count = """SELECT count(*) from preroute.member_verify_his a
            where a.GMT_CREATE > now() - interval 10 minute """
            sql_check_succ = """SELECT count(*) from preroute.member_verify_his a
            where a.is_success=1 and a.GMT_CREATE > now() - interval 10 minute """
            sql_list = [sql_reg, sql_loggin, sql_msg_send, sql_msg_succ, sql_check_count, sql_check_succ]
            value_list = []
            for sql in sql_list:
                select_conn = mysql_conn.DbConnect(pro_config, sql, 'check_gateway')
                result = select_conn.select()
                value_list.append(result[0][0])
            # print(value_list)
            logger.info('gateway data %s' % value_list)
            insert_sql = """insert into monitor.c_gateway (reg,login,msg_send,msg_succ,check_count,check_succ) \
            VALUES ('%s','%s','%s','%s','%s','%s')""" \
            % (value_list[0], value_list[1], value_list[2], value_list[3], value_list[4], value_list[5])
            insert_conn = mysql_conn.DbConnect(monitor_config, insert_sql, 'check_gateway')
            re = insert_conn.insert()
            logger.info('gateway update data:%s' % re)
            time.sleep(600)
    except Exception as error:
        logger.exception("Exception Logged", error)


if __name__ == '__main__':
    run()

