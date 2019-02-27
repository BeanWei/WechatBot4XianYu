# coding:utf-8
import os
here = os.path.abspath(os.path.dirname(__file__))
from celery_task.celery import CeleryApp
from config import *
from app import app
from views.api import json_api
from core.wx import get_bot
from models.user import User

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
                User(id=u.puid, subscriptions=[]).save()


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
def send_scan_qrcode_email(*args, **kwargs):
    """将登录扫码的二维码图片发送给自己"""
    # TODO: 增加获取二维码的间隔/添加主动登录入口
    from app import mail
    from flask_mail import Message
    with app.app_context():
        #app = current_app._get_current_object()
        msg = Message(
            subject=FLASK_MAIL_SUBJECT,
            sender=FLASK_MAIL_SENDER,
            recipients=[FLASK_MAIL_RECEIVER])
        with app.open_resource(os.path.join(here, "../QRimage/qr_code.png")) as fp:
            msg.attach("image.jpg", "image/jpg", fp.read())
            mail.send(msg)


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
    from models.xyproduct import XyproductMethod
    no_push_products = XyproductMethod.get_nopush_xyproduct()
