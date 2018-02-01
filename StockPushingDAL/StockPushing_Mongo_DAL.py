#encoding: utf-8
from StockPushingModels.MongoDbModel import RankingDaily, StockCodeName


def TestSave():
    d = dict()
    d["r_type"] = 1
    d["r_rank"] = 2
    d["r_name"] = "test"
    d["r_code"] = 6
    d["r_date"] = "2018-01-01"
    d["r_time"] = "09:30"

    ranking = RankingDaily(**d)
    try:
        ranking.save()
    except Exception as e:
        print("save failed data=%s" % ranking.to_json())
    return

def SaveRanking(ranking):
    try:
        ranking.save()
    except Exception as e:
        print("save failed data=%s" % ranking.to_json())
    return

def SavePushingStock(pushing):
    try:
        pushing.save()
    except Exception as e:
        print("save failed data=%s" % pushing.to_json())
    return

def GetRankingDateList():

    return RankingDaily._get_collection().distinct("r_date_str")

def GetRankingListByDate(checkDate):
    list = RankingDaily._get_collection().aggregate([
    { '$group' :
        { '_id' : {'day':'$r_date_str', 'code':'$r_code'},
          'count' : { '$sum' : 1 },
          'name' : {'$first': "$r_name"}
        }
    },
    { '$sort' : {'_id.day': -1, 'count':-1}},
    {'$match': {'_id.day': checkDate}}
    ])
    return list

def GetCodeByName(searching_name):
    results = StockCodeName.objects(s_name = searching_name)
    if len(results) > 0:
        return results[0]["s_code"]
    else:
        return 0

def GetNameByCode(searching_code):
    results = StockCodeName.objects(s_code = searching_code)
    if len(results) > 0:
        return results[0]["s_name"]
    else:
        return '0'

def SaveStockCodeName(s_code, s_name):
    d = dict()
    d["s_code"] = s_code
    d["s_name"] = s_name
    s = StockCodeName(**d)
    try:
        s.save()
        return True
    except Exception as e:
        print("save failed data=%s" % s.to_json())
        return False

def UpdateCodeByName(updating_code, updating_name):
    results = StockCodeName.objects(s_name = updating_name).update(set__s_code = updating_code)
    return True

def UpdateNameByCode(updating_code, updating_name):
    results = StockCodeName.objects(s_code = updating_code).update(s_name = updating_name)
    return True

def UpdateRankingCodeByName(updating_code, updating_name, original_code):
    results = RankingDaily.objects(r_name = updating_name, r_code = original_code).update(r_code = updating_code)
    return

def GetRankingListByDateAndCode(checkDate, checkCode):
    rankings = RankingDaily.objects(r_date_str = checkDate, r_code = checkCode)
    return rankings

def GetRankingCountByDateAndCode(checkDate, checkCode):
    list = RankingDaily._get_collection().aggregate([
    { '$group' :
        { '_id' : {'day':'$r_date_str', 'code':'$r_code','type':'$r_type'},
          'count' : { '$sum' : 1 }
        }
    },
    { '$sort' : {'count':-1}}
    ,
    { '$match' : {'_id.day': checkDate,'_id.code': int(checkCode)}}
    ])
    return list

def GetRankingListByDate_Code_type(checkDate, checkCode, checkType):
    rankings = RankingDaily.objects(r_date_str = checkDate, r_code = checkCode, r_type = checkType)
    return rankings

def GetNameForUnknowCodeOnDate(checkDate):
    list = RankingDaily._get_collection().aggregate([
    { '$group' :
        { '_id' : {'day':'$r_date_str', 'code':'$r_code','name':'$r_name'},
          'count' : { '$sum' : 1 },
          'name' : {'$first': "$r_name"}
        }
    },
    { '$sort' : {'_id.day': -1, 'count':-1}},
    {'$match': {'_id.day': checkDate,'_id.code': 0}}
    ])
    return list