# coding:utf-8
import os, sys
here = os.path.abspath(os.path.dirname(__file__))

def open_url(url):
    os_dev = sys.platform
    if os_dev == "win32":
        os.system("start {}".format(url))
    elif os_dev == "darwin":
        os.system("open {}".format(url))
    elif os_dev == "linux":
        os.system("xdg-open {}".format(url))
    else:
        os.system("start {}".format(url))

import base64
from app import mail, app
from config import *
from flask_mail import Message
from flask import render_template_string
def send_scan_qrcode_email(*args, **kwargs):
    """将登录扫码的二维码图片发送给自己"""

    with app.app_context():
        msg = Message(
            subject=FLASK_MAIL_SUBJECT,
            sender=FLASK_MAIL_SENDER,
            recipients=[FLASK_MAIL_RECEIVER])
        with app.open_resource(os.path.join(here, "../static/img/qr_code.png")) as fp:
            msg.attach("image.jpg", "image/jpg", fp.read(), 'inline', headers=[('Content-ID', 'image')])
            # img = base64.b64encode(fp.read())
            # msg.html = render_template_string(MAIL_CONTENT, img=img)
            mail.send(msg)
            from time import sleep
            sleep(10)












