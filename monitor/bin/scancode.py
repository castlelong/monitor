#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "longyucen"
# Date: 2018/2/5

import os
import sys
import time
import logging
import urllib.request
import json

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)

# print(base_dir)

logging.basicConfig(filename=base_dir + '/logs/scancode.log', level=logging.INFO, \
                    format='%(asctime)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S')
import falcon_oop


def run():
    while True:
        fp = urllib.request.urlopen("http://106.15.109.216:9527/noCard-outreach/consumeAndPaymentMonitored")
        data_bytes = fp.read()
        try:
            if len(data_bytes) > 0:
                data_str = data_bytes.decode("utf-8")
                data = json.loads(data_str)
                for key in data:
                    logging.info("scancode key:%s, value is %s" % (key, data[key]))
                    upload = falcon_oop.FalconMain("scancode", key, data[key], 300, "scancode"+key)
                    re_upload = upload.td()
                    logging.info("scancode:%s, is %s" % (key, re_upload))
                time.sleep(300)
        except Exception as error:
            logging.error(error)


run()

