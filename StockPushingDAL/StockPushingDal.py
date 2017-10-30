#!/usr/bin/python3
# encoding=utf-8
import Common.MySqlDbHelper
import Common.LogHandler
#import datetime

from StockPushingModels.models import StockWithNameAndId, StockPushing, StockMinPrice


def getStockList():
    # SQL 查询语句
    listStock = []
    sql = "SELECT code, name FROM stockpush_stockcodelist"
    c = Common.MySqlDbHelper.getResults(sql)

    for row in Common.MySqlDbHelper.generate_dicts(c):
        # code = int(row['code'])
        # name = row['name']
        # model = StockWithNameAndId()
        # model.code = code
        # model.name = name
        model = getStockWithNameAndIdFromRow(row)
        listStock.append(model)

    # print(listStock)
    return listStock

def getStockWithNameAndIdFromRow(row):
    model = StockWithNameAndId(row['code'], row['name'])
    return model

def getStockPushing(page, size):
    # SQL 查询语句
    Common.LogHandler.logging("start DAL.getStockPushing")

    listStock = []

    rowStart = (page - 1) * size
    # rowEnd = page * size

    sql = "SELECT id, StockName, Source, CreateTime, ValidateTime, Type " \
          "FROM stockpush_pushingstock order by ValidateTime desc " \
          "LIMIT " + str(rowStart) + "," + str(size)
    c = Common.MySqlDbHelper.getResults(sql)
    for row in Common.MySqlDbHelper.generate_dicts(c):
        model = getStockPushingFromRow(row)
        listStock.append(model)

    Common.LogHandler.logging("end DAL.getStockPushing")
    return listStock

def getStockPushingFromRow(row):
    model = StockPushing(row['id'], row['stockname'], row['source'], row['createtime'], row['validatetime'], row['type'])
    return model

def getStockPushingForDate(pushingDate):
    # SQL 查询语句
    Common.LogHandler.logging("start DAL.getStockPushing")

    listStock = []

    # nowDate = datetime.datetime.now()
    # delta = datetime.timedelta(days=1)
    # pushingDate = nowDate - 2 * delta

    strPushingDate = pushingDate #datetime.datetime.strftime(pushingDate, '%Y-%m-%d')

    # sql = "SELECT code, name FROM stockpush_stockcodelist"
    sql = "select * from stockpush_pushingstock where Date(ValidateTime) = '" \
          + strPushingDate + "'"
    c = Common.MySqlDbHelper.getResults(sql)
    for row in Common.MySqlDbHelper.generate_dicts(c):
        model = getStockPushingFromRow(row)
        listStock.append(model)

    Common.LogHandler.logging("end DAL.getStockPushing")
    return listStock

def getCheckDatesForStock(stockCode, listStrDates):
    # SQL 查询语句
    if len(listStrDates) > 0:
        listCheckedDates = []
        sql = "select checkdate from stockpush_stockcheckdate where stockcode = '" + str(stockCode) + "' and (checkDate = '" + str(listStrDates[0]) + "' "

        for n in range(1,len(listStrDates) ):
            sql = sql + " or checkDate = '" + str(listStrDates[n]) + "' "

        sql = sql + ")"

        c = Common.MySqlDbHelper.getResults(sql)
        for row in Common.MySqlDbHelper.generate_dicts(c):
            checkedDate = row['checkdate']
            listCheckedDates.append(checkedDate)

        return sorted(listCheckedDates)
    else:
        return []

def insertCheckDatesForStock(stockCode, listStrDates):
    sql = "insert into stockpush_stockcheckdate(stockcode, checkdate) values (" + str(stockCode) + ",'" + listStrDates[0] + "')"

    for n in range(1, len(listStrDates) ):
        sql += ", (" + str(stockCode) + ",'" + listStrDates[n] + "')"

    ret = Common.MySqlDbHelper.executeSql(sql)
    return

def insertCheckDatesForStock(stockCode, listStrDate, listTimes, listPrices):
    sql = "insert into stockpush_stockcheckdate(stockcode, checkdate) values (" + str(stockCode) + ",'" + listStrDate + "');"

    sql += "insert into stockpush_stockminprice (code, checkdate, checktime, price) values ("
    sql += str(stockCode) + ",'" + str(listStrDate) + "','" + str(listTimes[0]) + "'," + str(listPrices[0]) + ")"

    for n in range(1, len(listPrices) ):
        sql += ", (" + str(stockCode) + ",'" + str(listStrDate) + "','" + str(listTimes[n]) + "'," + str(listPrices[n]) + ")"

    sql += ";"
    ret = Common.MySqlDbHelper.executeSql(sql)
    return




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

def getMinPriceForStockOnDate(stockCode, checkDate, checkTime):
    # SQL 查询语句
    listMinPrice = []
    sql = "SELECT code, checkDate, checkTime, price FROM stockpush_stockminprice WHERE checkDate = '" + checkDate + "' "# limit 0,1000"

    if stockCode != None:
        sql += " and code = " + str(stockCode)

    if checkTime != None:
        sql += " and checkTime like '" + checkTime + "%' "

    sql += " order by checkTime ASC"
    c = Common.MySqlDbHelper.getResults(sql)
    for row in Common.MySqlDbHelper.generate_dicts(c):
        model = StockMinPrice(row['code'], row['checkdate'], row['checktime'], row['price'])
        listMinPrice.append(model)

    return listMinPrice

def AddStockPushing(stockModel):
    model = stockModel

    sql = "insert into stockpush_pushingstock (StockName, ValidateTime, Source, Type) values ("
    sql += ("'" + model.StockName + "',")
    sql += ("'" + model.ValidateTime + "',")
    sql += ("'" + model.Source + "',")
    sql += ("'" + model.Type + "'")
    sql += ");"

    return Common.MySqlDbHelper.executeSql(sql)

