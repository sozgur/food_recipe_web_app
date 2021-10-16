from flask_mail import Message
from app import mail
from flask import render_template
import os


def send_email(to, subject, template, **kwargs):
    msg = Message(subject, 
        sender=os.environ.get('MAIL_SENDER'), recipients=[to])
    msg.html = render_template(template+'.html', **kwargs)
    mail.send(msg)
