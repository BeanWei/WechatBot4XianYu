import os
here = os.path.abspath(os.path.dirname(__file__))

from wxpy import Bot
from config import *
from .utils import open_url, send_scan_qrcode_email

def callback_for_get_bot():
    if SEND_MAIL_TIPS_TO_LOGIN:
        qr_callback = send_scan_qrcode_email
    else:
        raise NotImplementedError("Sorry, Now Unsupport! This way on Development ")
    return qr_callback

def get_bot():
    qr_callback = callback_for_get_bot()
    bot = Bot('bot.pkl', qr_path=os.path.join(
        here, '../static/img/qr_code.png'
    ), console_qr=True, qr_callback=qr_callback)
    bot.enable_puid()
    bot.messages.max_history = 0
    return bot

def get_logged_in_user(bot):
    user_ = bot.self
    user = dict(
        id = user_.puid,
        name = user_.nick_name)
    return user