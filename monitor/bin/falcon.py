#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "longyucen"
# Date: 2017/11/27
# falcon push API接口
import time
import requests
import json


def falcon(name, metrics, messages):
    ts = int(time.time())
    payload = [
        {
            "endpoint": "TD" + name,
            "metric": "TD" + name,
            "timestamp": ts,
            "step": 60,
            "value": metrics,
            "counterType": "GAUGE",
            "tags": "TD Monitor",
        }
    ]
    r = requests.post("http://10.200.201.99:1988/v1/push", data=json.dumps(payload))
    # print(r.text)


def td_falcon(type, metrics, date):
    # print(date)
    date = int(time.mktime(time.strptime(date, "%Y-%m-%d %H:%M:%S")))
    payload = [
        {
            "endpoint": "XF",
            "metric": "XF" + type,
            "timestamp": date,
            "step": 20,
            "value": metrics,
            "counterType": "GAUGE",
            "tags": "XF Error Type",
        }
    ]
    r = requests.post("http://10.200.201.99:1988/v1/push", data=json.dumps(payload))
    return r


def df(type, metrics):
    date = int(int(time.time()))
    payload = [
        {
            "endpoint": "DF",
            "metric": "DF" + type,
            "timestamp": date,
            "step": 60,
            "value": metrics,
            "counterType": "GAUGE",
            "tags": "DF Error Type",
        }
    ]
    r = requests.post("http://10.200.201.99:1988/v1/push", data=json.dumps(payload))
    # print(r.text)


def w_monitor(name, metrics):
    """
    网页监控信息上传
    :param name: app名称
    :param metrics: 0为状态正常，1位状态异常
    :param messages:
    :return:
    """
    ts = int(time.time())
    payload = [
        {
            "endpoint": "WEB_Monitor",
            "metric": name,
            "timestamp": ts,
            "step": 60,
            "value": metrics,
            "counterType": "GAUGE",
            "tags": "WEB_Monitor",
        }
    ]
    r = requests.post("http://10.200.201.99:1988/v1/push", data=json.dumps(payload))
    # print(r.text)
