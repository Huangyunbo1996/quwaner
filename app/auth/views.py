from . import auth
from .forms import RegisterForm
from ..models import User
from ..utils.email import send_mail,email_server
from .. import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import render_template,redirect,flash,request,url_for,make_response,current_app
from flask_login import login_user,current_user

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
        login_user(new_user)
        return redirect(url_for('auth.jumpEmail'))
    return render_template('auth/register.html', form=form)

@auth.route('/jumpEmail')
def jumpEmail():
    server = current_user.email.split('@')[-1:][0]
    server_url = email_server[server]
    return render_template('auth/jumpEmail.html',url=server_url,user=current_user)

@auth.route('/confirm')
def confirm():
    if current_user.confirmed == True:
        return redirect(url_for('main.index'))
    token = request.args.get('token')
    if current_user.confirm(token):
        flash('账号验证成功')
    else:
        flash('验证失败或验证链接已过期')
    return redirect(url_for('main.index')) 
