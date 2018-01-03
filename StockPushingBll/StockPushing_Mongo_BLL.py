from StockPushingDAL import StockPushing_Mongo_DAL
from StockPushingModels.MongoDbModel import Ranking
from StockPushingDAL import StockPushingDal
import datetime

def TestSave():
    StockPushing_Mongo_DAL.TestSave()
    return

def SaveRanking(dict_rank):
    for one_type_rank in dict_rank:
        str_rank_type = one_type_rank["name"]
        i_ranking = 0
        for ranking_stock in one_type_rank["ranking"]:
            i_ranking = i_ranking + 1
            d = dict()
            d["r_type"] = str_rank_type
            d["r_rank"] = i_ranking
            d["r_name"] = ranking_stock["name"]
            d["r_code"] = getStockCodeByName(ranking_stock["name"])#int(ranking_stock["code"])
            d["r_datetime"] = datetime.datetime.now()
            ranking = Ranking(**d)
            StockPushing_Mongo_DAL.SaveRanking(ranking)
            print(ranking)


    return

def getStockCodeByName(stockName):
    return StockPushingDal.getStockCodeByName(stockName)