#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "longyucen"
# Date: 2017/11/27
import os
import sys
import threading
import logging
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
logger = logging.getLogger('main')
logger.setLevel(logging.INFO)
fh = logging.FileHandler(base_dir + '/logs/main.log', encoding="utf-8")
fh.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

import td_merics_oop
import td_df



threads = []
t1 = threading.Thread(target=td_merics_oop.run, args=())
threads.append(t1)
t2 = threading.Thread(target=td_df.run, args=())
threads.append(t2)

if __name__ == '__main__':
    try:
        for t in threads:
            logger.info(t)
            t.setDaemon(True)
            t.start()
        t.join()
    except Exception as e:
        logger.exception(e)

