#!/usr/bin/python3
#encoding=utf-8

import StockPushingDAL.StockPushingDal
import datetime
import tushare as ts
from Common.Common import HolidayList

def getStockList():
    return  StockPushingDAL.StockPushingDal.getStockList()

def getStockPushingWithAllData(page, size):
    list = StockPushingDAL.StockPushingDal.getStockPushingWithAllData(page, size)

    for m in list:
        strStockName = m.StockName
        listNameAndPrice = strStockName.split(',')
        for s in listNameAndPrice:
            if s.find('=') > 0:
                stockName = s.split('=')
                m.ListStockName.append(stockName[0])

    return  list

def getStockPushing(page, size):
    listHoliday = HolidayList()

    list = StockPushingDAL.StockPushingDal.getStockPushing(page, size)

    for m in list:
        strStockName = m.StockName
        listNameAndPrice = strStockName.split(',')
        for s in listNameAndPrice:
            if s.find('=') > 0:
                stockName = s.split('=')
                m.ListStockName.append(stockName[0])

    return  list

def Get5DaysMinPictureUrl(stockName):
    intStockCode = getStockCodeByName(stockName)
    if intStockCode > 0:
        stockCode = '{:0>6}'.format(str(intStockCode))
        listStockCode = []
        url1 = "http://pifm.eastmoney.com/EM_Finance2014PictureInterface/" \
               "Index.aspx?imagetype=t&type=M4&id=" + stockCode + "1&" \
               "token=4f1862fc3b5e77c150a2b985b12db0fd&rt=12054"
        url2 = "http://pifm.eastmoney.com/EM_Finance2014PictureInterface/" \
               "Index.aspx?imagetype=t&type=M4&id=" + stockCode + "2&" \
               "token=4f1862fc3b5e77c150a2b985b12db0fd&rt=12054"
        listStockCode.append(url1)
        listStockCode.append(url2)
        return  listStockCode
    else:
        return []

def getStockCodeByName(stockName):
    return StockPushingDAL.StockPushingDal.getStockCodeByName(stockName)

def getStockCodeListForPushingDate(pushingDate):
    # 获取当天推送股票列表
    strPushingDate = datetime.datetime.strftime(pushingDate, '%Y-%m-%d')
    listStock = StockPushingDAL.StockPushingDal.getStockPushingForDate(strPushingDate)
    # 列表生成式，生成股票名字的列表
    listStockN = [m.StockName for m in listStock]
    listStockName = []  # 因为一个推送股票object有可能包含几个股票，而且去除股票价格
    for strStockName in listStockN:
        listNameAndPrice = strStockName.split(',')
        for s in listNameAndPrice:
            if s.find('=') > 0:
                stockName = s.split('=')
                # utf8StockName = stockName[0].encode("utf-8")
                # listStockName.append(str.strip(utf8StockName))
                listStockName.append(getStockCodeByName(stockName[0]))

    def by_name(t):
        return t

    ls = list(set(listStockName))
    listStockNameSorted = sorted(ls, key=by_name)  # 排序
    print(listStockNameSorted)
    return listStockNameSorted

def takeNoteForPushingStockCode(pushingDate):
    #获取当天推送股票列表
    strPushingDate = datetime.datetime.strftime(pushingDate, '%Y-%m-%d')
    listStock = StockPushingDAL.StockPushingDal.getStockPushingForDate(strPushingDate)
    #列表生成式，生成股票名字的列表
    listStockN = [m.StockName for m in listStock]
    listStockName = [] #因为一个推送股票object有可能包含几个股票，而且去除股票价格
    for strStockName in listStockN:
        listNameAndPrice = strStockName.split(',')
        for s in listNameAndPrice:
            if s.find('=') > 0:
                stockName = s.split('=')
                # utf8StockName = stockName[0].encode("utf-8")
                # listStockName.append(str.strip(utf8StockName))
                listStockName.append(str.strip(stockName[0]))

    def by_name(t):
        return t

    ls = list(set(listStockName))
    listStockNameSorted = sorted(ls, key=by_name)#排序
    print(listStockNameSorted)
    fullSetDate = getFullSetDateForPushingDate(pushingDate)

    for stockName in listStockNameSorted:
        stockName = stockName.replace('A','')
        stockCode = getStockCodeByName(stockName)
        x = StockPushingDAL.StockPushingDal.getCheckDatesForStock(stockCode, fullSetDate)

        def removeChecked(d):
            return not (d in x)
        l = list(filter(removeChecked, fullSetDate))
        cl = l[:]#浅复制，不是引用
        print(stockName)

        if len(l) > 0:
            for checkDate in l:
                df = ts.get_tick_data('{:0>6}'.format(str(stockCode)), date=checkDate, pause=3)
                timesList = df.time
                priceList = df.price
                timeCount = len(timesList)

                flag = True
                if timeCount > 1:
                    prevTime = 0.00
                    currentTime = 0.00
                    listMinTime = []
                    listMinPrice = []
                    for n in range(0,len(timesList)):
                        print("{name:%s,code:%s,checkdate:%s,time:%s,price:%s}" % (stockName, stockCode, checkDate, timesList[n], priceList[n]))
                        if timesList[n] == 'alert("当天没有数据");':
                            print("sss")
                            cl.remove(checkDate)
                            flag = False
                            break

                        #筛选一分钟最后的价格
                        listCurrentTime = str(timesList[n]).split(':')
                        currentTime = float(listCurrentTime[0]) + 0.01 * float(listCurrentTime[1])
                        if currentTime != prevTime:
                            listMinTime.append(timesList[n])
                            listMinPrice.append(priceList[n])
                            prevTime = currentTime


                if flag:
                    q = StockPushingDAL.StockPushingDal.insertCheckDatesForStock(stockCode, checkDate, listMinTime, listMinPrice)
            # s = StockPushingDAL.StockPushingDal.insertCheckDatesForStock("603113", cl)

    return ""

def getFullSetDateForPushingDate(pushingDate):
    delta = datetime.timedelta(days=1)
    listFullSetDate = []
    listHolidays = HolidayList()

    #拿前5后3
    i = 1
    while len(listFullSetDate) < 5:
        theDate = pushingDate - i * delta
        if theDate.isoweekday() != 6 and theDate.isoweekday() != 7:
            try:
                listHolidays.holidayList.index(theDate.date()) >= 0
            except ValueError as e:
                listFullSetDate.append(theDate)
        i = i + 1

    i = 1
    while len(listFullSetDate) < 8:
        theDate = pushingDate + i * delta
        if theDate.isoweekday() != 6 and theDate.isoweekday() != 7:
            try:
                listHolidays.holidayList.index(theDate.date()) >= 0
            except ValueError as e:
                listFullSetDate.append(theDate)
        i = i + 1

    listFullSetDate.append(pushingDate)
    listStrFullDate = [datetime.datetime.strftime(d,"%Y-%m-%d") for d in sorted(listFullSetDate)]
    return listStrFullDate

def getMinPriceForStockOnDate(stockCode, checkDate, checkTime):
    list = StockPushingDAL.StockPushingDal.getMinPriceForStockOnDate(stockCode, checkDate, checkTime)
    return list

def getMinPriceForForFullSetDate(stockCode, checkDate, checkTime):
    fullSetDate = getFullSetDateForPushingDate(checkDate)
    fulList = []
    for strDate in fullSetDate:
        list = StockPushingDAL.StockPushingDal.getMinPriceForStockOnDate(stockCode, strDate, checkTime)
        for m in list:
            fulList.append(m)
    return fulList

def getTodayMinPriceForForFullSetDate():
    today = datetime.date.today()
    delta = datetime.timedelta(days=1)
    listDates = []
    i = 0
    while len(listDates) < 3:
        theDate = today - i * delta
        if theDate.isoweekday() != 6 and theDate.isoweekday() != 7:
            listDates.append(theDate)
        i = i + 1

    # listStrDates = [datetime.datetime.strftime(d, "%Y-%m-%d") for d in sorted(listDates)]
    for theDate in listDates:
        takeNoteForPushingStockCode(theDate)
    return ""

def getTheDateMinPriceForForFullSetDate(checkDate):

    delta = datetime.timedelta(days=1)
    listDates = []
    i = 0
    listHolidays = HolidayList()

    while len(listDates) < 3:
        theDate = checkDate - i * delta
        if theDate.isoweekday() != 6 and theDate.isoweekday() != 7:
            try:
                listHolidays.holidayList.index(theDate.date()) >= 0
            except ValueError as e:
                listDates.append(theDate)

        i = i + 1

    for theDate in listDates:
        takeNoteForPushingStockCode(theDate)
    return ""

def getMinPriceForFullSetDateForPushingDate(checkDate):


    listFullSetDate = getFullSetDateForPushingDate(checkDate)

    for strTheDate in listFullSetDate:
        theDate = datetime.datetime.strptime(strTheDate, '%Y-%m-%d')
        takeNoteForPushingStockCode(theDate)
    return ""

def AddStockPushing(stockModel):
    return StockPushingDAL.StockPushingDal.AddStockPushing(stockModel)