# coding:utf-8
import os
HERE = os.path.abspath(os.path.dirname(__file__))
from privacy_config import *

# 邮件配置
MAIL_DEBUG = False                                  # 开启debug的话可以看到响应结果
MAIL_SUPPRESS_SEND = False                          # 发送邮件，为True则不发送
MAIL_SERVER = 'smtp.qq.com'                         # 邮箱服务器
MAIL_PORT = 465                                     # 端口
MAIL_USE_SSL = True                                 # 重要，qq邮箱需要使用SSL
MAIL_USE_TLS = False                                # 不需要使用TLS
MAIL_USERNAME = MAIL_USERNAME                       # 填邮箱
MAIL_PASSWORD = MAIL_PASSWORD                       # 填授权码
FLASK_MAIL_SENDER = FLASK_MAIL_SENDER               # 邮件发送方
FLASK_MAIL_RECEIVER = FLASK_MAIL_RECEIVER           # 邮件接收方
FLASK_MAIL_SUBJECT = 'WechatBot需要您扫码登录'
MAIL_CONTENT = ''


# 数据库配置 (Mysql / Redis / MongoDB)
SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
REDIS_URL = REDIS_URL
SESSION_TYPE = 'redis'
SQLALCHEMY_RECORD_QUERIES = True
DATABASE_QUERY_TIMEOUT = 0.5
MONGODB_HOST = MONGODB_HOST
MONGODB_PORT = MONGODB_PORT
MONGODB_DB = 'wxbot'


# 微信机器人配置
AUTO_ACCEPT_VERIFY_TXT = ''                         # 自动接收好友请求时设置验证文本
NEW_FRIENDS_WELECOME_TXT = ''                       # 添加新的好友时的问候文本
HELP_TXT = ''                                       # /help 指令的响应文本