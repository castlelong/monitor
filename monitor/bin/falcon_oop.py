#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "longyucen"
# Date: 2017/12/13

import time
import requests
import json
import os
import sys
import logging

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
logging.basicConfig(filename=base_dir + '/logs/falcon_oop.logs', level=logging.INFO, \
                    format='%(asctime)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S')


class FalconMain(object):
    def __init__(self, name, metric_name, metric, step, tags):
        self.NAME = name
        self.METRIC_NAME = metric_name
        self.METRIC = metric
        self.TIME = int(time.time())
        self.STEP = step
        self.TAGS = tags

    def td(self):
        try:
            payload = [
                {
                    "endpoint": self.NAME,
                    "metric": self.METRIC_NAME,
                    "timestamp": self.TIME,
                    "step": self.STEP,
                    "value": self.METRIC,
                    "counterType": "GAUGE",
                    "tags": self.TAGS,
                }
            ]
            r = requests.post("http://10.200.201.99:1988/v1/push", data=json.dumps(payload))
            return r
        except Exception as error:
            logging.exception('ERROR TD MODULE', error)
