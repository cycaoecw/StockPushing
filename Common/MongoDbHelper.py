#!/usr/bin/python3
#encoding=utf-8

from mongoengine import connect

__author__ = "CY Cao"

# 连接 mongodb
def ConnectMongoDB():
    connect('StockPushing', host='119.23.73.195', port=27017)
    return