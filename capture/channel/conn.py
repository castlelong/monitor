#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "longyucen"
# Date: 2017/11/30

import pymysql


def mysql_select(sql):
    db = pymysql.connect("10.200.201.101", "root", "123456", "tdcode", charset='utf8')
    cur = db.cursor(cursor=pymysql.cursors.DictCursor)
    cur.execute(sql)
    result = cur.fetchall()
    return result
    db.commit()
    db.close()


def mysql_insert(sql):
    db = pymysql.connect("10.200.201.101", "root", "123456", "tdcode", charset='utf8')
    cur = db.cursor(cursor=pymysql.cursors.DictCursor)
    cur.execute(sql)
    db.commit()
    db.close()
