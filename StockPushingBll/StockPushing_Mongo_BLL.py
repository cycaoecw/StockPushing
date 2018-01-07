from StockPushingDAL import StockPushing_Mongo_DAL
from StockPushingModels.MongoDbModel import Ranking, PushingStock
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

        str_push_date_time = dict_rank["push_date_time"] # e.g. 2017-09-10 10:01:03
        dtPushingDate = ""
        try:
            dtPushingDate = datetime.strptime(str_push_date_time, '%Y-%m-%d %H:%M:%S')
            print(dtPushingDate)
        except ValueError as e:
            dtPushingDate = ""

        for one_type_rank in dict_rank["list"]:
            str_rank_type = one_type_rank["name"]
            i_ranking = 0


            for ranking_stock in one_type_rank["ranking"]:
                i_ranking = i_ranking + 1
                str_stock_name = ranking_stock["name"]
                int_stock_code = getStockCodeByName(ranking_stock["name"])  # int(ranking_stock["code"])


                #把记录保存到MongoDB
                d = dict()
                d["r_type"] = str_rank_type
                d["r_rank"] = i_ranking
                d["r_name"] = str_stock_name
                d["r_code"] = int_stock_code
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

                        p = dict()
                        p["p_name"] = str_stock_name
                        p["p_code"] = int_stock_code
                        p["p_price"] = d["r_price"]
                        p["p_dict_list"] = dict_rank
                        pushing = PushingStock(**p)
                        StockPushing_Mongo_DAL.SavePushingStock(pushing)
                        #db.getCollection('ranking').find({"r_datetime":{$gte:ISODate("2018-01-05T00:00:00+08:00")},"r_datetime":{$lte:ISODate("2018-01-05T06:45:59+08:00")}})


    else:
        return False


    return True

def getStockCodeByName(stockName):
    return StockPushingDal.getStockCodeByName(stockName)