#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "longyucen"
# Date: 2017/12/14


import pymysql
import logging
import os
import sys

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
log_file = base_dir + 'mysql.log'
logging.basicConfig(filename=log_file, level=logging.INFO, \
                    format='%(asctime)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S')


class DbConnect(object):
    def __init__(self, dbparamete, grammar, module):
        self.DBPARMAMETE = dbparamete
        self.SQL = grammar
        self.MODULE = module
        self.db_conn = pymysql.connect(host=self.DBPARMAMETE['host'], user=self.DBPARMAMETE['user'], \
                                       password=self.DBPARMAMETE['passwd'], port=self.DBPARMAMETE['port'],
                                       charset='utf8')

    def select(self):
        db = self.db_conn
        try:
            with db.cursor() as conn_mysql:
                conn_mysql.execute(self.SQL)
                result = conn_mysql.fetchall()
                return result
        except Exception as error:
            logging.exception('CONN ERROR:%s,%s' % (self.MODULE, error))
        finally:
            db.close()

    def insert(self):
        db = self.db_conn
        try:
            with db.cursor() as insert_mysql:
                insert_result = insert_mysql.execute(self.SQL)
                return insert_result
        except Exception as error:
            logging.info('INSERT ERROR:%s,%s' % (self.MODULE, error))
        finally:
            db.commit()
            db.close()

    def update(self):
        db = self.db_conn
        try:
            with db.cursor() as updata_mysql:
                updata_result = updata_mysql.execute(self.SQL)
                return updata_result
        except Exception as error:
            logging.info('UPDATA ERROR:%s,%s' % (self.MODULE, error))
        finally:
            db.commit()
            db.close()

    def delete(self):
        db = self.db_conn
        try:
            with db.cursor() as delete_mysql:
                delete_result = delete_mysql.execute(self.SQL)
                return delete_result
        except Exception as error:
            logging.info('DELETE ERROR:%s,%s' % (self.MODULE, error))
        finally:
            db.commit()
            db.close()