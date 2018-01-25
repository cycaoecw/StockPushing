#encoding: utf-8
from mongoengine import Document
from mongoengine import IntField
from mongoengine import StringField
from mongoengine import DateTimeField
from mongoengine import DecimalField
from mongoengine import DictField
from mongoengine import queryset_manager

import Common.MongoDbHelper

Common.MongoDbHelper.ConnectMongoDB()

class RankingDaily(Document):
    """
    排行榜
    0. default, 异常
    1. 升幅
    2. 换手
    3. 大单
    4. 净利
    """
    r_type = StringField(default="")
    r_rank = IntField(default=0)
    r_name = StringField(default="")
    r_code = IntField(default=0)
    r_datetime = DateTimeField()
    r_price = DecimalField(default=0, precision=2)
    r_date_str = StringField(default="2000-01-01")
    r_time_str = StringField(default="00:00:00")

    @queryset_manager
    def objects(doc_cls, queryset):
        # This may actually also be done by defining a default ordering for
        # the document, but this illustrates the use of manager methods
        return queryset.order_by('-r_datetime')

class PushingStock(Document):
    p_type =IntField(default = 0)
    p_name = StringField(default="")
    p_code = IntField(default=0)
    p_price = DecimalField(default=0, precision=2)
    p_dattime = DateTimeField()
    p_dict_list = DictField()

class StockCodeName(Document):
    s_name = StringField(default="")
    s_code = IntField(default=0)
