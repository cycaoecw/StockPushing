#!/usr/bin/python3
# encoding=utf-8
import Common.MySqlDbHelper
import Common.LogHandler
from StockPushingModels.models import StockWithNameAndId, StockPushing, StockMinPrice


def getStockCodeByName(stockName):
    # SQL 查询语句
    listStockCode = []
    sql = "SELECT * FROM stockpush_stockcodelist WHERE name LIKE '%" + stockName + "%'"
    c = Common.MySqlDbHelper.getResults(sql)
    for row in Common.MySqlDbHelper.generate_dicts(c):
        sotckCode = row['code']
        listStockCode.append(sotckCode)

    if len(listStockCode) > 0:
        return listStockCode[0]
    else:
        return 0

def getStockPushingForDate(pushingDate):
    # SQL 查询语句
    Common.LogHandler.logging("start DAL.getStockPushing")

    listStock = []
    strPushingDate = pushingDate #datetime.datetime.strftime(pushingDate, '%Y-%m-%d'
    sql = "select * from stockpush_pushingstock where Date(ValidateTime) = '" \
          + strPushingDate + "'"
    c = Common.MySqlDbHelper.getResults(sql)
    for row in Common.MySqlDbHelper.generate_dicts(c):
        model = getStockPushingFromRow(row)
        listStock.append(model)

    Common.LogHandler.logging("end DAL.getStockPushing")
    return listStock

def getStockPushingFromRow(row):
    model = StockPushing(row['id'], row['stockname'], row['source'], row['createtime'], row['validatetime'], row['type'])
    return model

def getOpenPriceOnNextDay(nextDate, code):

    strPushingDate = nextDate #datetime.datetime.strftime(pushingDate, '%Y-%m-%d'
    sql = "select * from stockpush_stockminprice where code = " + str(code) + " and checkDate = '" \
          + strPushingDate + "' and checkTime > '09:29:59' order by price desc limit 1"

    c = Common.MySqlDbHelper.getResults(sql)
    price = 0
    for row in Common.MySqlDbHelper.generate_dicts(c):
        price = row['price']
    # row = Common.MySqlDbHelper.getResults(sql)

    return price

def getHolidayList():
    # SQL 查询语句
    Common.LogHandler.logging("start DAL.getHolidayList")

    listHoliday = []

    sql = "select * from stockpush_holiday order by holiday desc"
    c = Common.MySqlDbHelper.getResults(sql)
    for row in Common.MySqlDbHelper.generate_dicts(c):
        listHoliday.append(row["holiday"])

    Common.LogHandler.logging("end DAL.getHolidayList")
    return listHoliday
