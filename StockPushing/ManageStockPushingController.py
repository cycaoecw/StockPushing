#encoding=utf-8
#!/usr/bin/python3


from django.http import HttpResponse
from StockPushingModels.models import *
import StockPushingBll.ManageStockPushingBLL
import json
import datetime

def getMinPriceForStockOnDate(request):
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
        model.Model = StockPushingBll.ManageStockPushingBLL.getMinPriceForStockOnDate(dtCheckDate)
        model.Status = '200'
        model.Msg = 'success'
    else:
        model.Model = 'Please using real date!'  # StockPushingBll.StockPushingBll.takeNoteForPushingStockCode(pushingDate)
        model.Status = '206'
        model.Msg = 'ERROR, Please using real date!'

    return HttpResponse(json.dumps(model, default=lambda o: o.__dict__, ensure_ascii=False))