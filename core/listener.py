# coding:utf-8
"""

将微信机器人所有的的自动化服务写在这，比如对话、聊天、、、、等等工具

"""
import os
import re

from wxpy.api import consts

from core.globals import current_bot as bot
from config import *

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

    
# TODO: 开发闲鱼商品订阅服务