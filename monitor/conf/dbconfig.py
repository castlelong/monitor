#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "longyucen"
# Date: 2017/12/14
"""
数据库配置文件
"""


def monitor_config():
    config_file = {
        'host': '10.200.201.101',
        'user': 'root',
        'passwd': '123456',
        'port': 3306
    }
    return config_file


def al_pro_config():
    config_file = {
        'host': '172.19.24.145',
        'user': 'alter',
        'passwd': '666666',
        'port': 3306
    }
    return config_file
