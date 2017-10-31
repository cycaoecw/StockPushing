#encoding=utf-8
#!/usr/bin/python3

from django.http import HttpResponse
from StockPushingModels.models import *
import StockPushingBll.AnalyzePushingBLL
import json
import datetime


def GetStockCodeListForPushingDate(request):
    pushingDate = request.GET.get('pushingDate')  # e.g. 2017-09-10

    getRealDate = True
    try:
        dtPushingDate = datetime.datetime.strptime(pushingDate, '%Y-%m-%d')
    except ValueError as e:
        getRealDate = False

    model = HttpResp()

    if getRealDate:
        model.Model = StockPushingBll.AnalyzePushingBLL.getStockCodeListForPushingDate(dtPushingDate)
        model.Status = '200'
        model.Msg = 'success'
    else:
        model.Model = 'Please using real date!'  # StockPushingBll.StockPushingBll.takeNoteForPushingStockCode(pushingDate)
        model.Status = '206'
        model.Msg = 'ERROR, Please using real date!'
    return HttpResponse(json.dumps(model, default=lambda o: o.__dict__, ensure_ascii=False))


def getStockForAnalyzeInPeriod(request):
    startDate = request.GET.get('startDate')  # e.g. 2017-09-10
    endDate = request.GET.get('endDate')  # e.g. 2017-09-10

    getRealDate = True
    try:
        dtStartDate = datetime.datetime.strptime(startDate, '%Y-%m-%d')
        dtEndDate = datetime.datetime.strptime(endDate, '%Y-%m-%d')
    except ValueError as e:
        getRealDate = False

    model = HttpResp()

    if getRealDate:
        model.Model = StockPushingBll.AnalyzePushingBLL.getStockForAnalyzeInPeriod(dtStartDate, dtEndDate)
        model.Status = '200'
        model.Msg = 'success'
    else:
        model.Model = 'Please using real date!'  # StockPushingBll.StockPushingBll.takeNoteForPushingStockCode(pushingDate)
        model.Status = '206'
        model.Msg = 'ERROR, Please using real date!'
    return HttpResponse(json.dumps(model, default=lambda o: o.__dict__, ensure_ascii=False))

def collect_stock_pushing_in_period(request):
    startDate = request.GET.get('startDate')  # e.g. 2017-09-10
    endDate = request.GET.get('endDate')  # e.g. 2017-09-10

    getRealDate = True
    try:
        dtStartDate = datetime.datetime.strptime(startDate, '%Y-%m-%d')
        dtEndDate = datetime.datetime.strptime(endDate, '%Y-%m-%d')
    except ValueError as e:
        getRealDate = False

    model = HttpResp()

    if getRealDate:
        model.Model = StockPushingBll.AnalyzePushingBLL.collect_stock_pushing_in_period(dtStartDate, dtEndDate)
        model.Status = '200'
        model.Msg = 'success'
    else:
        model.Model = 'Please using real date!'  # StockPushingBll.StockPushingBll.takeNoteForPushingStockCode(pushingDate)
        model.Status = '206'
        model.Msg = 'ERROR, Please using real date!'
    return HttpResponse(json.dumps(model, default=lambda o: o.__dict__, ensure_ascii=False))