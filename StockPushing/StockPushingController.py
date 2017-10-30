#encoding=utf-8
#!/usr/bin/python3


from django.http import HttpResponse
from StockPushingModels.models import *
import StockPushingBll.StockPushingBll
import json
import datetime
import Common.LogHandler

class HttpResp1:
    def __init__(self):
        self.status = '501'
        self.msg = '成功'
        self.model = ''

def AddStockPushing(request):

    StockName = request.POST.get('StockName')
    ValidateTime = request.POST.get('ValidateTime')
    Source = request.POST.get('Source')
    Type = request.POST.get('Type')
    stockModel = StockPushing("",StockName, Source, "", ValidateTime, Type)

    model = HttpResp()
    model.Model = StockPushingBll.StockPushingBll.AddStockPushing(stockModel)
    model.Status = '200'
    model.Msg = 'success'


    return HttpResponse(json.dumps(model, default=lambda o: o.__dict__, ensure_ascii=False))

def getStockList(request):
    model = HttpResp()
    model.Model = StockPushingBll.StockPushingBll.getStockList()
    model.Status = '200'
    model.Msg = 'success'

    return HttpResponse(json.dumps(model, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False))

def getStockPushing(request):
    # Common.LogHandler.logging("start getStockPushing")
    model = HttpResp()

    page = int(request.GET.get('page'))
    size = int(request.GET.get('size'))

    model.Model = StockPushingBll.StockPushingBll.getStockPushing(page, size)
    model.Status = '200'
    model.Msg = 'success'
    # Common.LogHandler.logging("start getStockPushing")
    return HttpResponse(json.dumps(model, default=lambda o: o.__dict__, ensure_ascii=False))

def getStockPushingWithAllData(request):
    # Common.LogHandler.logging("start getStockPushingWithAllData")

    model = HttpResp()

    page = int(request.GET.get('page'))
    size = int(request.GET.get('size'))

    model.Model = StockPushingBll.StockPushingBll.getStockPushingWithAllData(page, size)
    model.Status = '200'
    model.Msg = 'success'
    # Common.LogHandler.logging("end getStockPushingWithAllData")
    return HttpResponse(json.dumps(model, default=lambda o: o.__dict__, ensure_ascii=False))

def showTest(request):

    parm1 = p1 = request.GET.get('parm1')
    m = HttpResp1()
    m.model = parm1

    return HttpResponse(json.dumps(m, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False))



def Get5DaysMinPicUrl(request):
    stockName = request.GET.get('stockname')
    model = HttpResp()

    list = StockPushingBll.StockPushingBll.Get5DaysMinPictureUrl(stockName)

    if len(list) == 2:
        model.Model = list
        model.Status = '200'
        model.Msg = 'success'
    else:
        model.Model = list
        model.Status = '206'
        model.Msg = 'Errir, can not find the stock ' + stockName
    # Common.LogHandler.logging("end getStockPushingWithAllData")
    return HttpResponse(json.dumps(model, default=lambda o: o.__dict__, ensure_ascii=False))

def GetMinTradForDate(request):
    pushingDate = request.GET.get('pushingDate') # e.g. 2017-09-10

    getRealDate = True
    try:
        dtPushingDate = datetime.datetime.strptime(pushingDate,'%Y-%m-%d')
    except ValueError as e:
        getRealDate = False

    model = HttpResp()

    if getRealDate:
        model.Model = StockPushingBll.StockPushingBll.takeNoteForPushingStockCode(dtPushingDate)
        model.Status = '200'
        model.Msg = 'success'
    else:
        model.Model = 'Please using real date!'  # StockPushingBll.StockPushingBll.takeNoteForPushingStockCode(pushingDate)
        model.Status = '206'
        model.Msg = 'ERROR, Please using real date!'

    return HttpResponse(json.dumps(model, default=lambda o: o.__dict__, ensure_ascii=False))

def GetStockCodeListForPushingDate(request):
    pushingDate = request.GET.get('pushingDate')  # e.g. 2017-09-10

    getRealDate = True
    try:
        dtPushingDate = datetime.datetime.strptime(pushingDate, '%Y-%m-%d')
    except ValueError as e:
        getRealDate = False

    model = HttpResp()

    if getRealDate:
        model.Model = StockPushingBll.StockPushingBll.getStockCodeListForPushingDate(dtPushingDate)
        model.Status = '200'
        model.Msg = 'success'
    else:
        model.Model = 'Please using real date!'  # StockPushingBll.StockPushingBll.takeNoteForPushingStockCode(pushingDate)
        model.Status = '206'
        model.Msg = 'ERROR, Please using real date!'

    return HttpResponse(json.dumps(model, default=lambda o: o.__dict__, ensure_ascii=False))

def getMinPriceForStockOnDate(request):
    # Common.LogHandler.logging("start getStockPushing")
    model = HttpResp()

    stockCode = request.GET.get('stockcode')
    checkDate = request.GET.get('checkdate')
    checkTime = request.GET.get('checktime')

    model.Model = StockPushingBll.StockPushingBll.getMinPriceForStockOnDate(stockCode, checkDate, checkTime)
    model.Status = '200'
    model.Msg = 'success'
    # Common.LogHandler.logging("start getStockPushing")
    return HttpResponse(json.dumps(model, default=lambda o: o.__dict__, ensure_ascii=False))

def getMinPriceForForFullSetDate(request):
    checkDate = request.GET.get('checkdate') # e.g. 2017-09-10

    getRealDate = True
    try:
        dtCheckDate = datetime.datetime.strptime(checkDate,'%Y-%m-%d')
    except ValueError as e:
        getRealDate = False

    model = HttpResp()

    if getRealDate:
        stockCode = request.GET.get('stockcode')
        checkTime = request.GET.get('checktime')
        model.Model = StockPushingBll.StockPushingBll.getMinPriceForForFullSetDate(stockCode, dtCheckDate, checkTime)
        model.Status = '200'
        model.Msg = 'success'
    else:
        model.Model = 'Please using real date!'  # StockPushingBll.StockPushingBll.takeNoteForPushingStockCode(pushingDate)
        model.Status = '206'
        model.Msg = 'ERROR, Please using real date!'

    return HttpResponse(json.dumps(model, default=lambda o: o.__dict__, ensure_ascii=False))

def getMinPriceForForFullSetDateThruName(request):
    checkDate = request.GET.get('checkdate') # e.g. 2017-09-10

    stockName = request.GET.get('stockname')
    stockCode = StockPushingBll.StockPushingBll.getStockCodeByName(stockName)
    getRealDate = True
    try:
        dtCheckDate = datetime.datetime.strptime(checkDate,'%Y-%m-%d')
    except ValueError as e:
        getRealDate = False

    model = HttpResp()

    if getRealDate:
        checkTime = request.GET.get('checktime')
        model.Model = StockPushingBll.StockPushingBll.getMinPriceForForFullSetDate(stockCode, dtCheckDate, checkTime)
        model.Status = '200'
        model.Msg = 'success'
    else:
        model.Model = 'Please using real date!'  # StockPushingBll.StockPushingBll.takeNoteForPushingStockCode(pushingDate)
        model.Status = '206'
        model.Msg = 'ERROR, Please using real date!'

    return HttpResponse(json.dumps(model, default=lambda o: o.__dict__, ensure_ascii=False))

def getTodayMinPriceForForFullSetDate(request):
    model = HttpResp()
    model.Status = '200'
    model.Msg = 'success'
    model.Model = StockPushingBll.StockPushingBll.getTodayMinPriceForForFullSetDate()
    return HttpResponse(json.dumps(model, default=lambda o: o.__dict__, ensure_ascii=False))

def getTheDateMinPriceForForFullSetDate(request):
    model = HttpResp()
    model.Status = '200'
    model.Msg = 'success'

    checkDate = request.GET.get('checkdate')  # e.g. 2017-09-10
    getRealDate = True
    try:
        dtCheckDate = datetime.datetime.strptime(checkDate, '%Y-%m-%d')
    except ValueError as e:
        getRealDate = False

    if getRealDate:
        model.Model = StockPushingBll.StockPushingBll.getTheDateMinPriceForForFullSetDate(dtCheckDate)
        model.Status = '200'
        model.Msg = 'success'
    else:
        model.Model = 'Please using real date!'  # StockPushingBll.StockPushingBll.takeNoteForPushingStockCode(pushingDate)
        model.Status = '206'
        model.Msg = 'ERROR, Please using real date!'

def getMinPriceForFullSetDateForPushingDate(request):
    model = HttpResp()
    model.Status = '200'
    model.Msg = 'success'

    checkDate = request.GET.get('checkdate')  # e.g. 2017-09-10
    getRealDate = True
    try:
        dtCheckDate = datetime.datetime.strptime(checkDate, '%Y-%m-%d')
    except ValueError as e:
        getRealDate = False

    if getRealDate:
        model.Model = StockPushingBll.StockPushingBll.getMinPriceForFullSetDateForPushingDate(dtCheckDate)
        model.Status = '200'
        model.Msg = 'success'
    else:
        model.Model = 'Please using real date!'  # StockPushingBll.StockPushingBll.takeNoteForPushingStockCode(pushingDate)
        model.Status = '206'
        model.Msg = 'ERROR, Please using real date!'



    return HttpResponse(json.dumps(model, default=lambda o: o.__dict__, ensure_ascii=False))

def testCurlSuccess(request):
    model = HttpResp()
    model.Status = '200'
    model.Msg = 'success'
    return HttpResponse(json.dumps(model, default=lambda o: o.__dict__, ensure_ascii=False))

def testCurlFailed(request):
    model = HttpResp()
    model.Status = '400'
    model.Msg = 'failed'
    ts.sss()
    return HttpResponse(json.dumps(model, default=lambda o: o.__dict__, ensure_ascii=False))