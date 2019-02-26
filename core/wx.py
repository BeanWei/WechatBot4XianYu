import os
here = os.path.abspath(os.path.dirname(__file__))

from wxpy import Bot
from celery_task.tasks import send_scan_qrcode_email, update_contact

def get_bot():
    bot = Bot('bot.pkl', qr_path=os.path.join(
        here, '../QRimage/qr_code.png'
    ), qr_callback=send_scan_qrcode_email, login_callback=update_contact)
    bot.enable_puid()
    bot.messages.max_history = 0
    return bot

def get_logged_in_user(bot):
    user_ = bot.self
    user = dict(
        id = user_.puid,
        name = user_.nick_name
    )
    return user