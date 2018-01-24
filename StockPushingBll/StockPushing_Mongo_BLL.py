#encoding: utf-8
from StockPushingDAL import StockPushing_Mongo_DAL
from StockPushingModels.MongoDbModel import RankingDaily, PushingStock
from StockPushingDAL import StockPushingDal
from datetime import datetime, timedelta, time
from Common import JpushHelper
import pytz

def TestSave():
    StockPushing_Mongo_DAL.TestSave()
    return

def GetRankingDateList():

    return sorted(StockPushing_Mongo_DAL.GetRankingDateList(), reverse=True)

def GetRankingListByDate(checkDate):
    cursor = StockPushing_Mongo_DAL.GetRankingListByDate(checkDate)
    list_ranking = []
    for r in cursor:
        list_ranking.append(r)

    return list_ranking

def SaveRanking(dict_rank):


    if "compare" in dict_rank and "list" in dict_rank and "hit_rule" in dict_rank:
        int_compare_rank = int(dict_rank["compare"]) #只查看榜中的前几个
        int_hit_rule = int(dict_rank["hit_rule"])    #中了多少个榜就推送
        dict_hitting_stock = dict()
        tzSH = pytz.timezone('Asia/Shanghai')

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
                int_stock_code = GetCodeByName(ranking_stock["name"])  # int(ranking_stock["code"])
                ranking_stock["code"] = int_stock_code

                #把记录保存到MongoDB
                d = dict()
                d["r_type"] = str_rank_type
                d["r_rank"] = i_ranking
                d["r_name"] = str_stock_name
                d["r_code"] = int_stock_code
                d["r_datetime"] = dtPushingDate
                d["r_price"] = ranking_stock["price"]
                d["r_date_str"] = dtPushingDate.strftime('%Y-%m-%d')
                d["r_time_str"] = dtPushingDate.strftime('%H:%M:%S')
                ranking = RankingDaily(**d)
                StockPushing_Mongo_DAL.SaveRanking(ranking)

                #检查股票在规定前X中hit中多少次，大于hit_rule就推送
                if i_ranking <= int_compare_rank:
                    flag_found = False
                    for s_to_matching in dict_hitting_stock:
                        if str_stock_name in s_to_matching:#如果股票名字已经包含在dict里
                            dict_hitting_stock[s_to_matching] = dict_hitting_stock[s_to_matching] + 1
                            str_stock_name = s_to_matching
                            flag_found = True
                            break

                        elif s_to_matching in str_stock_name:#如果dict里的名字包含在股票名字里
                            dict_hitting_stock[str_stock_name] = dict_hitting_stock[s_to_matching] + 1
                            dict_hitting_stock.popitem(s_to_matching)
                            flag_found = True
                            break

                    if not flag_found:
                        dict_hitting_stock[str_stock_name] = 1

                    # if str_stock_name in dict_hitting_stock:
                    #     dict_hitting_stock[str_stock_name] = dict_hitting_stock[str_stock_name] + 1
                    # else:
                    #     dict_hitting_stock[str_stock_name] = 1

                    #print("%s : %d" % (str_stock_name, dict_hitting_stock[str_stock_name]))
                    if dict_hitting_stock[str_stock_name] == int_hit_rule:

                        print("the stock %s which is %s already hit %d times, pushing price is %.2f" %
                                (str_stock_name, '{:0>6}'.format(str(d["r_code"])), int_hit_rule, d["r_price"]))
                        JpushHelper.Push_message("Found the stock which code is %s already hit %d times, pushing price is %.2f" %
                                ( '{:0>6}'.format(str(d["r_code"])), int_hit_rule, d["r_price"]))

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

def GetCodeByName(searching_name):
    return StockPushing_Mongo_DAL.GetCodeByName(searching_name)

def UpdateCodeByName(updating_code, updating_name):
    # s_code = StockPushing_Mongo_DAL.GetCodeByName(updating_name)
    s_name = StockPushing_Mongo_DAL.GetNameByCode(updating_code)
    flag = True
    if flag == '0':
        flag = StockPushing_Mongo_DAL.SaveStockCodeName(updating_code, updating_name)
    else:
        flag = StockPushing_Mongo_DAL.UpdateNameByCode(updating_code, updating_name)
    return flag