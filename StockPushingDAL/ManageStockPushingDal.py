#!/usr/bin/python3
# encoding=utf-8
import Common.MySqlDbHelper
import Common.LogHandler
#import datetime
from StockPushingModels.models import StockWithNameAndId, StockPushing, StockMinPrice

def getStockPushingOnDate(strCheckDate):
    # SQL 查询语句
    Common.LogHandler.logging("start DAL.getStockPushing")

    listStock = []

    # nowDate = datetime.datetime.now()
    # delta = datetime.timedelta(days=1)
    # pushingDate = nowDate - 2 * delta

    strPushingDate = strCheckDate #datetime.datetime.strftime(pushingDate, '%Y-%m-%d')

    # sql = "SELECT code, name FROM stockpush_stockcodelist"
    sql = "select * from stockpush_pushingstock where Date(ValidateTime) = '" \
          + strPushingDate + "'"
    c = Common.MySqlDbHelper.getResults(sql)
    for row in Common.MySqlDbHelper.generate_dicts(c):
        model = getStockPushingFromRow(row)
        listStock.append(model)

    Common.LogHandler.logging("end DAL.getStockPushing")
    return listStock

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

def insertCheckDatesForStock(stockCode, strDate, listTimes, listPrices):
    sql = "insert into stockpush_stockcheckdate(stockcode, checkdate) values (" + str(stockCode) + ",'" + strDate + "');"

    sql += "insert into stockpush_stockminprice (code, checkdate, checktime, price) values ("
    sql += str(stockCode) + ",'" + str(strDate) + "','" + str(listTimes[0]) + "'," + str(listPrices[0]) + ")"

    for n in range(1, len(listPrices) ):
        sql += ", (" + str(stockCode) + ",'" + str(strDate) + "','" + str(listTimes[n]) + "'," + str(listPrices[n]) + ")"

    sql += ";"
    ret = Common.MySqlDbHelper.executeSql(sql)
    return ret

def getCheckDatesForStock(strCheckDate):
    # SQL 查询语句
    listCheckedCode = []
    sql = "select stockcode from stockpush_stockcheckdate where checkDate = '" + strCheckDate + "' "

    c = Common.MySqlDbHelper.getResults(sql)
    for row in Common.MySqlDbHelper.generate_dicts(c):
        stockcode = row['stockcode']
        listCheckedCode.append(stockcode)

    return sorted(listCheckedCode)


def getStockPushingFromRow(row):
    model = StockPushing(row['id'], row['stockname'], row['source'], row['createtime'], row['validatetime'], row['type'])
    return model
