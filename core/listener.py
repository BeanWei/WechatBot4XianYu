# coding:utf-8
import os
import re

from wxpy.api import consts

from core.globals import current_bot as bot

@bot.register(msg_types=consts.FRIENDS)
def new_friends(msg):
    user = msg.card.accept()
    
