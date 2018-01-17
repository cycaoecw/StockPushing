#encoding: utf-8
from StockPushingModels.MongoDbModel import RankingDaily

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