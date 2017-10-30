#!/usr/bin/python3
#encoding=utf-8

import time

def logging(content):
    print(time.strftime("%H:%M:%S", time.localtime(time.time())) + " : " + str(content))