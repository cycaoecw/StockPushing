from StockPushingModels.MongoDbModel import Ranking

def TestSave():
    d = dict()
    d["r_type"] = 1
    d["r_rank"] = 2
    d["r_name"] = "测试"
    d["r_code"] = 6
    d["r_date"] = "2018-01-01"
    d["r_time"] = "09:30"

    ranking = Ranking(**d)
    try:
        ranking.save()
    except Exception as e:
        print("保存失败 data=%s" % post.to_json(), exc_info=True)
    return

def SaveRanking(ranking):
    try:
        ranking.save()
    except Exception as e:
        print("保存失败 data=%s" % ranking.to_json(), exc_info=True)
    return