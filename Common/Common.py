#!/usr/bin/python3
#encoding=utf-8
import StockPushingBll.AnalyzePushingBLL
from functools import wraps

def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False


def isWorkingDay(checkDate):
    listHolidays = HolidayList()
    if checkDate.isoweekday() != 6 and checkDate.isoweekday() != 7:
        try:
            if listHolidays.holidayList.index(checkDate.date()) >= 0:
                return False
        except ValueError as e:
            return True
    return False

def singleton(cls):
    instances = {}

    @wraps(cls)
    def getinstance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return getinstance




@singleton
class HolidayList(object):
    holidayList = StockPushingBll.AnalyzePushingBLL.getHolidayList()
