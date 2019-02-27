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


from app import mail, app
from config import *
from flask_mail import Message
def send_scan_qrcode_email():
    """将登录扫码的二维码图片发送给自己"""

    with app.app_context():
        msg = Message(
            subject=FLASK_MAIL_SUBJECT,
            sender=FLASK_MAIL_SENDER,
            recipients=[FLASK_MAIL_RECEIVER])
        with app.open_resource(os.path.join(here, "../static/img/qr_code.png")) as fp:
            msg.attach("image.jpg", "image/jpg", fp.read())
            mail.send(msg)