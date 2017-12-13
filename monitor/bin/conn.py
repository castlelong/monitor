#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "longyucen"
# Date: 2017/11/27
# 生产数据库连接 查询数据库
import pymysql
import os
import sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(base_dir)
sys.path.append(base_dir)
import falcon
import logging
logging.basicConfig(filename=base_dir + '/logs/mysql.log', level=logging.INFO, \
                    format='%(asctime)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S')


def mysql(statement):
    db = pymysql.connect(host="106.15.208.12", user="alter", password="666666", port=3306, charset='utf8')
    try:
        with db.cursor() as cursor:
            cur = db.cursor()
            sql = statement
            cur.execute(sql)
            result = cur.fetchall()
            for value in result:
                # print(value)
                v_list = []
                for v in value:
                    v_list.append(v)
                falcon.falcon(v_list[0], float(v_list[3]), v_list[4])
    finally:
        cur.close()


def td_monitor(statement):
    db = pymysql.connect(host='10.200.201.101', user='root', password='123456', port=3306, db='tdcode', charset='utf8')
    try:
        with db.cursor() as cursor:
            cur = db.cursor()
            sql = statement
            cur.execute(sql)
            result = cur.fetchall()
            for value in result:
                # print(value)
                v_list = []
                for v in value:
                    v_list.append(v)
                v_list[2] = v_list[2].strftime("%Y-%m-%d %H:%M:%S")
                return falcon.td_falcon(v_list[0], float(v_list[1]), v_list[2])
    finally:
        cur.close()


def f_trade(statement):
    # print(statement)
    db = pymysql.connect(host="106.15.208.12", user="alter", password="666666", port=3306, charset='utf8')
    try:
        with db.cursor() as cursor:
            cur = db.cursor()
            sql = statement
            cur.execute(sql)
            result = cur.fetchall()
            for value in result:
                # print(value)
                v_list = []
                for v in value:
                    v_list.append(v)
                return v_list
    finally:
        cur.close()


def conn(statement):
    # print(statement)
    db = pymysql.connect(host="10.200.201.101", user="root", password="123456", port=3306, charset='utf8')
    try:
        with db.cursor() as cursor:
            cur = db.cursor()
            sql = statement
            cur.execute(sql)
            result = cur.fetchall()
            return result
    finally:
        cur.close()


def w_conn(statement):
    # print(statement)
    db = pymysql.connect(host="10.200.201.101", user="root", password="123456", port=3306, charset='utf8')
    try:
        with db.cursor() as cursor:
            cur = db.cursor()
            sql = statement
            cur.execute(sql)
            result = cur.fetchall()
            # print('result:', result)
            return result
    except:
        logging.exception("ERROR W_CONN Module")
    finally:
        cur.close()