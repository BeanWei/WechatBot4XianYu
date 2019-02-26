# coding:utf-8
import os
here = os.path.abspath(os.path.dirname(__file__))
from celery_task.celery import CeleryApp
from config import *
from app import app, mail
from flask_mail import Message


@CeleryApp.task
def send_scan_qrcode_email(*args, **kwargs):
    """将登录扫码的二维码图片发送给自己"""
    with app.app_context():
        #app = current_app._get_current_object()
        msg = Message(
            subject=FLASK_MAIL_SUBJECT,
            sender=FLASK_MAIL_SENDER,
            recipients=[FLASK_MAIL_RECEIVER])
        with app.open_resource(os.path.join(here, "../QRimage/qr_code.png")) as fp:
            msg.attach("image.jpg", "image/jpg", fp.read())
            mail.send(msg)
