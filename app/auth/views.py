from . import auth
from .forms import RegisterForm
from ..models import User
from ..utils.email import send_mail
from .. import db
from flask import render_template,redirect,flash,request,url_for,make_response

@auth.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(form.email.data,form.username.data,form.password.data)
        db.session.add(new_user)
        db.session.commit()
        send_mail(recipient=new_user.email, subject='请验证你的趣玩儿账户',
                    template='auth/email/confirm', user=new_user, 
                    token=new_user.generate_confirm_token())
        flash('注册成功，请查看你的邮箱，点击验证邮件里的链接进行验证。')
        resp = make_response(redirect(url_for('auth.jumpEmail')))
        resp.set_cookie('username',new_user.username)
        return resp
    return render_template('auth/register.html', form=form)

@auth.route('/jumpEmail')
def jumpEmail():
    return 'ok'

@auth.route('/confirm')
def confirm():
    pass