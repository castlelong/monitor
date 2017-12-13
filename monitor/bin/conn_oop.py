#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "longyucen"
# Date: 2017/12/13

import pymysql
import logging
import os
import sys
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
logging.basicConfig(filename=base_dir + '/logs/falcon-oop.logs', level=logging.INFO, \
                    format='%(asctime)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S')


class FalconRun(object):
    def __init__(self, hosts, user, password, port, grammar, module):
        self.USER = user
        self.HOSTS = hosts
        self.PORT = port
        self.PASS = password
        self.SQL = grammar
        self.MODULE = module
        self.db_conn = pymysql.connect(host=self.HOSTS, user=self.USER, password=self.PASS, port=self.PORT, charset='utf8')

    def conn(self):
        db = self.db_conn
        try:
            with db.cursor() as conn_mysql:
                conn_mysql.execute(self.SQL)
                result = conn_mysql.fetchall()
                return result
        except Exception as error:
            logging.exception('CONN ERROR:', self.MODULE, error)
        finally:
            conn_mysql.close()

    def insert(self):
        db = self.db_conn
        try:
            with db.cursor() as insert_mysql:
                insert_mysql.execute(self.SQL)
        except Exception as error:
            logging.exception('INSERT ERROR:', self.MODULE, error)
        finally:
            insert_mysql.close()