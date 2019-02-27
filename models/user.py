from models import mdb


class User(mdb.Document):
    """ 用户Model，主要存放用户puid及订阅信息 """
    # Puid 微信用户的ID
    id = mdb.StringField(required=True)
    # 暂时仅支持订阅闲鱼二手手机, 支持同时监控多款型号的手机
    care_mobiles = mdb.ListField(mdb.StringField(max_length=120))
    care_price = mdb.ListField(mdb.IntField(required=True))

