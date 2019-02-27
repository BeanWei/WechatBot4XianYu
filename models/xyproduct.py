# conding:utf-8
from models import SQLBase, sql_session
from sqlalchemy import Column, Integer, String, DateTime, Boolean

class XYProduct(SQLBase):
    """ 闲鱼二手商品Model """
    __tablename__ = 'xyproduct'
    __table_args__ = {'mysql_charset': 'utf8mb4'}
    id = Column(Integer, primary_key=True)
    categoryId = Column(String(60))
    imageUrl = Column(String(255))
    itemUrl = Column(String(255))
    isBrandNew = Column(Boolean())
    price = Column(String(60))
    orgPrice = Column(String(60))
    city = Column(String(60))
    description = Column(String(255))
    commentCount = Column(String(60))
    title = Column(String(255))
    userNick = Column(String(120))
    vipLevel = Column(String(10))
    isSinaV = Column(Boolean())
    userItemsUrl = Column(String(255))
    ispush = Column(Boolean, default=False)



# SQL 方法
class XyproductMethod(object):
    """ xyproduct 表操作集合方法 """

    def batch_add_xyproduct(self, product_list):
        """ 添加多个商品 """
        sql_session.add(product_list)
        sql_session.commit()

    def update_xyproduct_ispush_field(self, product_id):
        """ 更新商品是否已经推送给用户的状态 """
        sql_session.query(XYProduct).\
            filter(XYProduct.id == product_id).\
            update({'ispush': True})
        sql_session.commit()

    def get_nopush_xyproduct(self):
        """ 获取未推送的商品 """
        return sql_session.query(XYProduct).\
                filter_by(ispush=False).all()






















