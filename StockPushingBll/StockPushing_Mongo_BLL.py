from StockPushingDAL import StockPushing_Mongo_DAL
from StockPushingModels.MongoDbModel import Ranking
from StockPushingDAL import StockPushingDal
from datetime import datetime, timedelta, timezone

def TestSave():
    StockPushing_Mongo_DAL.TestSave()
    return

def SaveRanking(dict_rank):
    tz_utc_8 = timezone(timedelta(hours=8))  # 创建时区UTC+8:00

    if "compare" in dict_rank and "list" in dict_rank and "hit_rule" in dict_rank:
        int_compare_rank = int(dict_rank["compare"])
        int_hit_rule = int(dict_rank["hit_rule"])
        dict_hitting_stock = dict()

        for one_type_rank in dict_rank["list"]:
            str_rank_type = one_type_rank["name"]
            i_ranking = 0

            for ranking_stock in one_type_rank["ranking"]:
                i_ranking = i_ranking + 1
                str_stock_name = ranking_stock["name"]

                #把记录保存到MongoDB
                d = dict()
                d["r_type"] = str_rank_type
                d["r_rank"] = i_ranking
                d["r_name"] = str_stock_name
                d["r_code"] = getStockCodeByName(ranking_stock["name"])  # int(ranking_stock["code"])
                d["r_datetime"] = tz_utc_8.fromutc(datetime.utcnow().replace(tzinfo=tz_utc_8))
                d["r_price"] = ranking_stock["price"]
                ranking = Ranking(**d)
                StockPushing_Mongo_DAL.SaveRanking(ranking)

                #检查股票在规定前X中hit中多少次，大于hit_rule就推送
                if i_ranking <= int_compare_rank:
                    if str_stock_name in dict_hitting_stock:
                        dict_hitting_stock[str_stock_name] = dict_hitting_stock[str_stock_name] + 1
                    else:
                        dict_hitting_stock[str_stock_name] = 1

                    #print("%s : %d" % (str_stock_name, dict_hitting_stock[str_stock_name]))
                    if dict_hitting_stock[str_stock_name] == int_hit_rule:
                        print("the stock %s which code is %s already hit %d times, pushing price is %.2f" %
                              (str_stock_name,'{:0>6}'.format(str(d["r_code"])) ,int_hit_rule, d["r_price"]))


    else:
        return False


    return True

def getStockCodeByName(stockName):
    return StockPushingDal.getStockCodeByName(stockName)