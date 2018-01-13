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

def SaveRanking(request):
    '''
    test
    '''



    str_json = """
{
	"compare": 3,
	"hit_rule": 3,
	"push_date_time": "2018-01-13 09:13:29",
	"list": [{
		"name": "raising",
		"ranking": [{
			"code": 0,
			"price": 9.55,
			"name": "江泉实业"
		}, {
			"code": 0,
			"price": 19.32,
			"name": "文投控股"
		}, {
			"code": 0,
			"price": 14.89,
			"name": "旋极信息"
		}, {
			"code": 0,
			"price": 25.85,
			"name": "君禾股份"
		}, {
			"code": 0,
			"price": 10.01,
			"name": "欧浦智网"
		}]
	}, {
		"name": "change",
		"ranking": [{
			"code": 0,
			"price": 36.0,
			"name": "华森制药"
		}, {
			"code": 0,
			"price": 25.85,
			"name": "君禾股份"
		}, {
			"code": 0,
			"price": 94.04,
			"name": "深南电路"
		}, {
			"code": 0,
			"price": 44.98,
			"name": "美芝股份"
		}, {
			"code": 0,
			"price": 5740.0,
			"name": "中设股份"
		}]
	}, {
		"name": "deal",
		"ranking": [{
			"code": 0,
			"price": 19.32,
			"name": "文投控股"
		}, {
			"code": 0,
			"price": 53.3,
			"name": "格力电器"
		}, {
			"code": 0,
			"price": 7.82,
			"name": "驰宏锌锗"
		}, {
			"code": 0,
			"price": 788.42,
			"name": "贵州茅台"
		}, {
			"code": 0,
			"price": 64.82,
			"name": "料大讯飞"
		}]
	}, {
		"name": "net",
		"ranking": [{
			"code": 0,
			"price": 19.32,
			"name": "文投控股"
		}, {
			"code": 0,
			"price": 53.3,
			"name": "格力电器"
		}, {
			"code": 0,
			"price": 7.82,
			"name": "驰宏锌锗"
		}, {
			"code": 0,
			"price": 64.82,
			"name": "料大讯飞"
		}, {
			"code": 0,
			"price": 788.42,
			"name": "贵州茅台"
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
        d = json.loads(str_json)
        model.Model = StockPushing_Mongo_BLL.SaveRanking(d)
        # model.Model = "Not correct json_str!!"
        model.Status = '511'
        model.Msg = 'Failed - Not correct json_str!!'




    return HttpResponse(json.dumps(model, default=lambda o: o.__dict__, ensure_ascii=False))