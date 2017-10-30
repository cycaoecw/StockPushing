#!/usr/bin/python3
#encoding=utf-8

import StockPushingDAL.AnalyzPushingDAL
import datetime
import Common

def getStockCodeByName(stockName):
    return StockPushingDAL.AnalyzPushingDAL.getStockCodeByName(stockName)

def getStockCodeListForPushingDate(pushingDate):
    # 获取当天推送股票列表
    strPushingDate = datetime.datetime.strftime(pushingDate, '%Y-%m-%d')
    listStock = StockPushingDAL.AnalyzPushingDAL.getStockPushingForDate(strPushingDate)
    # 列表生成式，生成股票名字的列表

    listStockN = [{"name": m.StockName, "time": m.ValidateTime} for m in listStock]
    listStockName = []  # 因为一个推送股票object有可能包含几个股票，而且去除股票价格
    for m in listStockN:
        strStockName = m["name"]
        listNameAndPrice = strStockName.split(',')
        for s in listNameAndPrice:
            if s.find('=') > 0:
                stockName = s.split('=')
                # utf8StockName = stockName[0].encode("utf-8")
                # listStockName.append(str.strip(utf8StockName))
                sName = str.strip(stockName[0])
                sPrice = float(str.strip(stockName[1]))
                if sPrice > 0:
                    stock = {"name": sName, "time": m["time"], "code": getStockCodeByName(sName), "price": sPrice}
                    listStockName.append(stock)

    def by_name(t):
        return t["name"]

    # ls = list(set(listStockName))
    listStockNameSorted = sorted(listStockName, key=by_name)  # 排序
    listStockNoDuplicated = []
    if len(listStockNameSorted) > 0:
        listStockNoDuplicated.append(listStockNameSorted[0])
        for m in listStockNameSorted:
            if m["name"] != listStockNoDuplicated[len(listStockNoDuplicated) - 1]["name"]:
                listStockNoDuplicated.append(m)
            elif m["time"] < listStockNoDuplicated[len(listStockNoDuplicated) - 1]["time"]:
                listStockNoDuplicated[len(listStockNoDuplicated) - 1]["time"] = m["time"]
                listStockNoDuplicated[len(listStockNoDuplicated) - 1]["price"] = m["price"]

    delta = datetime.timedelta(days=1)
    nextDate = pushingDate
    i=1
    while nextDate == pushingDate:
        theDate = pushingDate + i * delta
        if Common.Common.isWorkingDay(theDate):
            nextDate = theDate
        i = i + 1

    strNextDate = datetime.datetime.strftime(nextDate, '%Y-%m-%d')
    for stock in listStockNoDuplicated:
        nextDayPrice = StockPushingDAL.AnalyzPushingDAL.getOpenPriceOnNextDay(strNextDate, stock["code"])
        stock["nextOpenPrice"] = nextDayPrice
        stock["nextOpenDate"] = strNextDate
        print(stock)


    print(listStockNoDuplicated)
    return listStockNoDuplicated

def getStockForAnalyzeInPeriod(startDate, endDate):
    listStock = []

    delta = datetime.timedelta(days=1)
    theDate = startDate
    while theDate <= endDate:
        list = getStockCodeListForPushingDate(theDate)
        for m in list:
            listStock.append(m)

        theDate = theDate + delta
        while not Common.Common.isWorkingDay(theDate):
            theDate = theDate + delta


    return listStock

def getHolidayList():
    return StockPushingDAL.AnalyzPushingDAL.getHolidayList()