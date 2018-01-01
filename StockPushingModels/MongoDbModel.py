from mongoengine import Document
from mongoengine import IntField
from mongoengine import StringField
from mongoengine import DateTimeField
import Common.MongoDbHelper

Common.MongoDbHelper.ConnectMongoDB()

class Ranking(Document):
    """
    排行榜
    0. default, 异常
    1. 升幅
    2. 换手
    3. 大单
    4. 净利
    """
    r_type = IntField(default=0)
    r_rank = IntField(default=0)
    r_name = StringField(default="")
    r_code = IntField(default=0)
    r_date = DateTimeField()
    r_time = DateTimeField()
