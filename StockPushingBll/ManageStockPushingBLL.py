#!/usr/bin/python3
#encoding=utf-8


import datetime
import tushare as ts
import Common.Common
import StockPushingDAL.ManageStockPushingDal

def getFullSetDateForPushingDate(pushingDate):
    delta = datetime.timedelta(days=1)
    listFullSetDate = []

    #拿前5
    i = 1
    while len(listFullSetDate) < 5:
        theDate = pushingDate - i * delta
        if Common.Common.isWorkingDay(theDate):
            listFullSetDate.append(theDate)
        i = i + 1

    #拿后3
    i = 1
    while len(listFullSetDate) < 8:
        theDate = pushingDate + i * delta
        if Common.Common.isWorkingDay(theDate):
            listFullSetDate.append(theDate)
        i = i + 1

    #还有自己
    listFullSetDate.append(pushingDate)
    #排序,转成string
    listStrFullDate = [datetime.datetime.strftime(d,"%Y-%m-%d") for d in sorted(listFullSetDate)]
    return listStrFullDate

def getStockCodeListOnDate(strCheckDate):

    # 获取当天推送股票列表
    listStock = StockPushingDAL.ManageStockPushingDal.getStockPushingOnDate(strCheckDate)
    # 列表生成式，生成股票名字的列表
    listStockN = [m.StockName for m in listStock]
    listStockCode = []  # 因为一个推送股票object有可能包含几个股票，而且去除股票价格
    for strStockName in listStockN:
        listNameAndPrice = strStockName.split(',')
        for s in listNameAndPrice:
            if s.find('=') > 0:
                stockName = s.split('=')
                # utf8StockName = stockName[0].encode("utf-8")
                # listStockName.append(str.strip(utf8StockName))
                listStockCode.append(getStockCodeByName(stockName[0]))

    def by_code(t):
        return t

    ls = list(set(listStockCode))
    listStockCodeSorted = sorted(ls, key=by_code)  # 排序
    #print(listStockCodeSorted)
    return listStockCodeSorted

def getMinPriceForStockOnDate(dtCheckDate):
    strCheckDate = datetime.datetime.strftime(dtCheckDate, '%Y-%m-%d')
    lsStockCode = getStockCodeListOnDate(strCheckDate)
    lsCheckedStockCode = StockPushingDAL.ManageStockPushingDal.getCheckDatesForStock(strCheckDate)

    def removeChecked(d):
        return not (d in lsCheckedStockCode)

    lsNotCheckStockCode = list(filter(removeChecked, lsStockCode))
    #cl = lsNotCheckStockCode[:]  # 浅复制，不是引用

    for stockCode in lsNotCheckStockCode:
        df = ts.get_tick_data('{:0>6}'.format(str(stockCode)), date=strCheckDate, pause=3)
        timesList = df.time
        priceList = df.price
        timeCount = len(timesList)

        flag = True
        if timeCount > 1:
            prevTime = 0.00
            currentTime = 0.00
            listMinTime = []
            listMinPrice = []
            for n in range(0, len(timesList)):
                # print("{code:%s,checkdate:%s,time:%s,price:%s}" % (stockCode, dtCheckDate, timesList[n], priceList[n]))
                if timesList[n] == 'alert("当天没有数据");':
                    # print("sss")
                    # cl.remove(checkDate)
                    flag = False
                    break

                # 筛选一分钟最后的价格
                listCurrentTime = str(timesList[n]).split(':')
                currentTime = float(listCurrentTime[0]) + 0.01 * float(listCurrentTime[1])
                if currentTime != prevTime:
                    listMinTime.append(timesList[n])
                    listMinPrice.append(priceList[n])
                    print("{code:%s,checkdate:%s,time:%s,price:%s}" % (
                    stockCode, strCheckDate, timesList[n], priceList[n]))
                    prevTime = currentTime

        if flag:
            q = StockPushingDAL.ManageStockPushingDal.insertCheckDatesForStock(stockCode, strCheckDate, listMinTime,
                                                                         listMinPrice)

    return ""

def getMinPriceForStockOnFullSetDate(checkDate):
    listStrFullDate = getFullSetDateForPushingDate(checkDate)
    return listStrFullDate

def getStockCodeByName(stockName):
    return StockPushingDAL.ManageStockPushingDal.getStockCodeByName(str.strip(stockName))

