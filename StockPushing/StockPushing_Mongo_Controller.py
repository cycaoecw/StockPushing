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