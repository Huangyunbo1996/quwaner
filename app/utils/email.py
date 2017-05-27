from .. import mail
from flask_mail import Message
from flask import current_app,render_template
from threading import Thread

def send_mail(recipient,subject,template,**kwargs):
    msg = Message(current_app.config['MAIL_SUBJECT_PREFIX'] + subject,
                    recipients=[recipient])
    msg.html = render_template(template + '.html', **kwargs)
    msg.body = render_template(template + '.txt', **kwargs)
    app = current_app._get_current_object()
    thread = Thread(target=async_send_email,args=[app,msg])
    thread.start()
    return thread

def async_send_email(app,msg):
    with app.app_context():
        mail.send(msg)

email_server = {
    'qq.com' : 'https://mail.qq.com',
    '163.com' : 'https://mail.163.com',
    '126.com' : 'http://www.126.com',
    'gmail.com' : 'https://mail.google.com',
    'outlook.com' : 'https://outlook.live.com'
}