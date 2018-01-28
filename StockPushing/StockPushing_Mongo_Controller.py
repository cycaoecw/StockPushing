#encoding=utf-8
#!/usr/bin/python3

from django.http import HttpResponse
from StockPushingBll import StockPushing_Mongo_BLL
from StockPushingModels.models import *
import json


__author__ = "CY Cao"

def TestSave(request):
    model = HttpResp()
    model.Model = StockPushing_Mongo_BLL.TestSave()
    model.Status = '200'
    model.Msg = 'success'

    return HttpResponse(json.dumps(model, default=lambda o: o.__dict__, ensure_ascii=False))

def GetRankingDateList(request):
    model = HttpResp()
    model.Model = StockPushing_Mongo_BLL.GetRankingDateList()
    model.Status = '200'
    model.Msg = 'success'

    return HttpResponse(json.dumps(model, default=lambda o: o.__dict__, ensure_ascii=False))

def GetRankingListByDate(request):
    model = HttpResp()
    checkDate = request.GET.get('checkdate')  # e.g. 2018-01-17
    model.Model = StockPushing_Mongo_BLL.GetRankingListByDate(checkDate)
    model.Status = '200'
    model.Msg = 'success'

    return HttpResponse(json.dumps(model, default=lambda o: o.__dict__, ensure_ascii=False))

def SaveRanking(request):
    '''
    test
    '''



    str_json = """
{
	"compare": 4,
	"hit_rule": 4,
	"push_date_time": "2018-01-15 10:50:02",
	"list": [{
		"name": "raising",
		"ranking": [{
			"code": 0,
			"price": 29.88,
			"name": "登云股份"
		}, {
			"code": 0,
			"price": 7.18,
			"name": "壹桥股份"
		}, {
			"code": 0,
			"price": 20.78,
			"name": "蓝帆医疗"
		}, {
			"code": 0,
			"price": 10.88,
			"name": "凯恩股份"
		}, {
			"code": 0,
			"price": 11.52,
			"name": "日播时尚"
		}]
	}, {
		"name": "change",
		"ranking": [{
			"code": 0,
			"price": 11.2,
			"name": "迪生力"
		}, {
			"code": 0,
			"price": 39.72,
			"name": "联诚精密"
		}, {
			"code": 0,
			"price": 16.91,
			"name": "卫信康"
		}, {
			"code": 0,
			"price": 7.18,
			"name": "壹桥股份"
		}, {
			"code": 0,
			"price": 1445.0,
			"name": "金龙羽"
		}]
	}, {
		"name": "deal",
		"ranking": [{
			"code": 0,
			"price": 36.84,
			"name": "三聚环保"
		}, {
			"code": 0,
			"price": 8.83,
			"name": "潍柴动力"
		}, {
			"code": 0,
			"price": 7.18,
			"name": "壹桥股份"
		}, {
			"code": 0,
			"price": 20.78,
			"name": "蓝帆医疗"
		}, {
			"code": 0,
			"price": 14.91,
			"name": "上海银行"
		}]
	}, {
		"name": "net",
		"ranking": [{
			"code": 0,
			"price": 7.18,
			"name": "桥股份"
		}, {
			"code": 0,
			"price": 8.83,
			"name": "潍柴动力"
		}, {
			"code": 0,
			"price": 36.84,
			"name": "聚环保"
		}, {
			"code": 0,
			"price": 20.78,
			"name": "蓝帆医疗"
		}, {
			"code": 0,
			"price": 14.91,
			"name": "上海银行"
		}]
	}]
}
"""

    str_request_json = request.POST.get('str_json')
    model = HttpResp()
    if str_request_json != None:
        d = json.loads(str_request_json)
        model.Model = StockPushing_Mongo_BLL.SaveRanking(d)
        model.Status = '200'
        model.Msg = 'success'
    else:
        # d = json.loads(str_json)
        # model.Model = StockPushing_Mongo_BLL.SaveRanking(d)
        model.Model = "Not correct json_str!!"
        model.Status = '511'
        model.Msg = 'Failed - Not correct json_str!!'




    return HttpResponse(json.dumps(model, default=lambda o: o.__dict__, ensure_ascii=False))

def GetCodeByName(request):
    model = HttpResp()
    searching_name = request.GET.get('searching_name')  # e.g. 读者传媒
    model.Model = StockPushing_Mongo_BLL.GetCodeByName(searching_name)
    model.Status = '200'
    model.Msg = 'success'

    return HttpResponse(json.dumps(model, default=lambda o: o.__dict__, ensure_ascii=False))

def UpdateCodeByName(request):
    model = HttpResp()
    updating_code = request.GET.get('updating_code')  # e.g. 读者传媒
    updating_name = request.GET.get('updating_name')  # e.g. 读者传媒
    model.Model = StockPushing_Mongo_BLL.UpdateCodeByName(updating_code, updating_name)
    model.Status = '200'
    model.Msg = 'success'

    return HttpResponse(json.dumps(model, default=lambda o: o.__dict__, ensure_ascii=False))

def GetRankingListByDateAndCode(request):
    model = HttpResp()
    checkDate = request.GET.get('checkDate')  # e.g. 2018-01-25
    checkCode = request.GET.get('checkCode')  # e.g. 603363
    model.Model = StockPushing_Mongo_BLL.GetRankingListByDateAndCode(checkDate, checkCode)
    model.Status = '200'
    model.Msg = 'success'

    return HttpResponse(json.dumps(model, default=lambda o: o.__dict__, ensure_ascii=False))

def GetRankingCountByDateAndCode(request):
    model = HttpResp()
    checkDate = request.GET.get('checkDate')  # e.g. 2018-01-25
    checkCode = request.GET.get('checkCode')  # e.g. 603363
    model.Model = StockPushing_Mongo_BLL.GetRankingCountByDateAndCode(checkDate, checkCode)
    model.Status = '200'
    model.Msg = 'success'
    return HttpResponse(json.dumps(model, default=lambda o: o.__dict__, ensure_ascii=False))

def GetRankingListByDate_Code_type(request):
    model = HttpResp()
    checkDate = request.GET.get('checkDate')  # e.g. 2018-01-25
    checkCode = request.GET.get('checkCode')  # e.g. 603363
    checkType = request.GET.get('checkType')  # e.g. raising
    model.Model = StockPushing_Mongo_BLL.GetRankingListByDate_Code_type(checkDate, checkCode, checkType)
    model.Status = '200'
    model.Msg = 'success'
    return HttpResponse(json.dumps(model, default=lambda o: o.__dict__, ensure_ascii=False))

def TryGetStockCodeByNameThruInterenet(request):
    model = HttpResp()
    checkName = request.GET.get('checkName')  # e.g. ST金宇

    model.Model = StockPushing_Mongo_BLL.TryGetStockCodeByNameThruInterenet(checkName)
    model.Status = '200'
    model.Msg = 'success'
    return HttpResponse(json.dumps(model, default=lambda o: o.__dict__, ensure_ascii=False))

def GetNameForUnknowCodeOnDate(request):
    model = HttpResp()
    checkDate = request.GET.get('checkDate')  # e.g. 2018-01-26

    model.Model = StockPushing_Mongo_BLL.GetNameForUnknowCodeOnDate(checkDate)
    model.Status = '200'
    model.Msg = 'success'
    return HttpResponse(json.dumps(model, default=lambda o: o.__dict__, ensure_ascii=False))