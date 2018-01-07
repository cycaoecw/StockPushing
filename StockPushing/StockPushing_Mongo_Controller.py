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
    "hit_rule": 4,
    "push_date_time": "2018-01-07 10:01:03",
    "list": [
        {
            "name": "raising",
            "ranking": [
                {
                    "name": "振静股份",
                    "code": 111,
                    "price": 1
                },
                {
                    "name": "北斗星通",
                    "code": 222,
                    "price": 2
                }
                ,
                {
                    "name": "北京科锐",
                    "code": 222,
                    "price": 2
                }
            ]
        },
        {
            "name": "change",
            "ranking": [
                {
                    "name": "美芝股份",
                    "code": 333,
                    "price": 3
                },
                {
                    "name": "蒙草生态",
                    "code": 444,
                    "price": 4
                }
                ,
                {
                    "name": "北京科锐",
                    "code": 222,
                    "price": 2
                }
            ]
        },
        {
            "name": "deal",
            "ranking": [
                {
                    "name": "文一科技",
                    "code": 555,
                    "price": 5
                },
                {
                    "name": "雅克科技",
                    "code": 666,
                    "price": 6
                }
                ,
                {
                    "name": "北京科锐",
                    "code": 222,
                    "price": 2
                }
            ]
        },
        {
            "name": "net",
            "ranking": [
                {
                    "name": "北斗星通",
                    "code": 777,
                    "price": 7
                },
                {
                    "name": "武汉凡谷",
                    "code": 888,
                    "price": 8
                }
                ,
                {
                    "name": "北京科锐",
                    "code": 222,
                    "price": 2
                }
            ]
        }
    ]
}
"""

    str_request_json = request.POST.get('str_json')
    model = HttpResp()
    if str_request_json == None:
        d = json.loads(str_json)
        model.Model = StockPushing_Mongo_BLL.SaveRanking(d)
        model.Status = '200'
        model.Msg = 'success'
    else:
        model.Model = "No json str"
        model.Status = '511'
        model.Msg = 'Failed'




    return HttpResponse(json.dumps(model, default=lambda o: o.__dict__, ensure_ascii=False))