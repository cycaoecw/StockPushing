#encoding=utf-8
# Create your models here.



class StockWithNameAndId():
    def __init__(self, code, name):
        self.name = name
        self.code = int(code)


class HttpResp:
    def __init__(self):
        self.Status = '501'
        self.Msg = 'init'
        self.Model = ''

class StockPushing():
    def __init__(self, id, StockName, Source, CreateTime, ValidateTime, Type):
        self.id = id
        self.StockName = StockName
        self.Source = Source
        self.CreateTime = str(CreateTime)
        self.ValidateTime = str(ValidateTime)
        self.Type = Type
        self.ListStockName = []


class StockMinPrice():
    def __init__(self, code, checkDate, checkTime, price):
        self.code = code
        self.checkDate = checkDate
        self.checkTime = checkTime
        self.price = price


