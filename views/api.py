# coding:utf-8
import glob
import re
import os
here = os.path.abspath(os.path.dirname(__file__))
from flask import request

from views import json_api
from core.wx import get_logged_in_user
from core.globals import current_bot, _wx_ctx_stack

@json_api.route('/login', methods=['post'])
def login():
    user = get_logged_in_user(current_bot)
    return {
        'error': '',
        'type': 'login',
        'user': user
    }


@json_api.route('/logout', methods=['post'])
def logout():
    _wx_ctx_stack.pop()
    for f in glob.glob('{}/*.pkl'.format(here)):
        try:
            os.remove(f)
        except FileNotFoundError:
            pass
    return {
        'error': '',
        'type': 'logout'
    }


@json_api.route('/friends', methods=['get'])
def allfriends():
    # TODO: 改为从数据库中获取
    users = current_bot.friends()
    return {
        'error': '',
        'type': 'get_all_friends',
        'users': users
    }


@json_api.route('/sendmsg', methods=['post'])
def sendmsg():
    ''' 发送消息给  部分(单个)好友/全部好友
    消息暂只支持文本类型
    '''
    data = request.get_json()
    target = data['target']   # target = [] => 将消息发送给所有好友
                               # target = [puid, puid...] => 将消息发送给部分(单个)好友
    content = data['content']
    users = current_bot.friends()
    if target != "[]":
        rm = re.match(r'\[(.*?)\]', target)
        if not rm:
            return {
                'error': '参数错误',
                'type': 'send_message_to_friends'
            }
        t_li = rm.group(1).split(",")
        users = [u for u in users if u.puid in t_li]
    for user in users:
        user.send_msg(content)
    # TODO: 列出发送失败的好友
    return {
        'error': '',
        'type': 'send_message_to_friends'
    }











