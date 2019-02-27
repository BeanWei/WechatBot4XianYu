# coding:utf-8
import os
here = os.path.abspath(os.path.dirname(__file__))
from celery_task.celery import CeleryApp
from config import *
from app import app
from views.api import json_api
from models.user import User
from core.wx import get_bot

bot = get_bot()

def _get_self(bot):
    """ 从MongoDB获取bot信息，不存在则获取并入库 """
    myself = User.objects(id=bot.self.puid).first()
    if not myself:
        myself = bot.self.puid
        User(id=myself, subscriptions=[]).save()
    return myself


def _update_contact(bot, update=False):
    """ 更新好友 """
    # myself = _get_self(bot)
    wx_friends = bot.friends(update)
    local_ids = set([u.id for u in User.objects.all()])
    wx_ids = set([u.puid for u in wx_friends])
    need_add = wx_ids.difference(local_ids)
    if need_add:
        for u in wx_friends:
            if u.puid in need_add:
                User(id=u.puid, care_mobiles=[], care_price=[999999,999999]).save()


@CeleryApp.task
def listener():
    """ 启动bot """
    from core.listener import bot
    with app.app_context():
        # join 为 `wxpy` 中的方法
        # 堵塞进程，直到结束消息监听 (例如，机器人被登出时)
        bot.join()



@CeleryApp.task
def update_contact(update=False):
    with json_api.app_context():
        _update_contact(bot, update=update)






@CeleryApp.task
def xyspider():
    """ 闲鱼爬虫 """
    from spider.xysj import xy_spider
    xy_spider(PRODUCT_CATEGORY_ID, SPIDER_PAGES_TOTAL)


@CeleryApp.task
def push_xyproduct_to_wxfriends():
    """
    1. 获取MySQL数据库中未推送的商品
    2. 查询MongoDB中的User需求类别
    3. 利用Flask建立的api接口分别推送到对应的好友
    4. 推送完成后更新数据库中的推送状态
    """
    msg_tmp = "{}\n发布者: {}\n价格: {}\n原始价格: {}\n城市: {}\n评论数: {}\n简述: {}\n商品链接: {}\n"
    import requests
    from models.xyproduct import XyproductMethod
    no_push_products = XyproductMethod.get_nopush_xyproduct()

    just_care_price_users = User.objects.filter(care_mobiles=[]).all()
    for npp in no_push_products:
        msg = msg_tmp.format(
            npp.title,
            npp.userNick,
            npp.price,
            npp.orgPrice,
            npp.city,
            npp.commentCount,
            npp.description,
            npp.itemUrl
        )
        one_part_users = list()
        # 先推送只关注价格的订阅者
        for jcpu in just_care_price_users:
            if jcpu.care_price[0] <= int(npp.price) and jcpu.care_price[1] >= int(npp.price):
                one_part_users.append(jcpu)

        requests.get(
            SERVER_URI+"/sendmsg",
            params={
                "target": "["+",".join(one_part_users)+"]",
                "content": msg
            })

        #TODO 再推送剩余订阅者



