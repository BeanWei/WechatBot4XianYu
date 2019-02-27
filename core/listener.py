# coding:utf-8
"""

将微信机器人所有的的自动化服务写在这，比如对话、聊天、、、、等等工具

"""
import os
import re

from wxpy.api import consts
from wxpy import ensure_one

from core.globals import current_bot as bot
from config import *
from models.user import User

@bot.register(msg_types=consts.FRIENDS)
def auto_accept_friends(msg):
    """ 自动接收好友请求 """
    if AUTO_ACCEPT_VERIFY_TXT:
        if AUTO_ACCEPT_VERIFY_TXT in msg.text.lower():
            new_friend = bot.accept_friend(msg.card)
            new_friend.send(NEW_FRIENDS_WELECOME_TXT)
    else:
        new_friend = msg.card.accept()
        new_friend.send(NEW_FRIENDS_WELECOME_TXT)

    
@bot.register([bot.friends()], consts.TEXT)
def auto_reply(msg):
    """ 自动回复 """
    # 固定格式: @[小米9&小米8,2000-4000] 或 @[2000-4000]
    fromuser = ensure_one(bot.search(msg.fromUserName))
    res = re.match(r'\@\[(.*?)\]', msg)
    if res:
        msg = res.group(1)
        msg = msg.replace("，", ",")
        a = msg.split(",")
        if len(a) == 1:
            b = a[0].split("-")
            if len(b) != 2:
                return "价格范围是必要条件且必须符合`0-9999`此格式"
            try:
                ap, bp = int(b[0]), int(b[1])
                if ap > bp:
                    Lprice, Hprice = bp, ap
                else:
                    Lprice, Hprice = ap, bp
            except Exception as e:
                return "价格必须为数值"
            mobiles, prices = [], [Lprice, Hprice]
            User(id=fromuser.puid, care_mobiles=mobiles, care_price=prices).save()
            return """
                恭喜订阅成功! \n
                你关注的手机为: 无限制 \n
                你关注的价格范围为: ￥{} 至 ￥{}这个价格区间
                """.format(Lprice, Hprice)
        elif len(a) == 2:
            b = a[1].split("-")
            if len(b) != 2:
                return "价格范围必须符合`0-9999`此格式"
            try:
                ap, bp = int(b[0]), int(b[1])
                if ap > bp:
                    Lprice, Hprice = bp, ap
                else:
                    Lprice, Hprice = ap, bp
            except Exception as e:
                return "价格必须为数值"
            mobiles, prices = a[0].split("&"), [Lprice, Hprice]
            User(id=fromuser.puid, care_mobiles=mobiles, care_price=prices).save()
            return """
                恭喜订阅成功! \n
                你关注的手机为: {} \n
                你关注的价格范围为: ￥{} 至 ￥{}这个价格区间
                """.format(" | ".join(mobiles), Lprice, Hprice)
        else:
            return "订阅信息必须符合`@[小米9&小米8,2000-4000]或者@[2000-4000]`"
    else:
        return "暂时不支持闲聊功能。。。"
