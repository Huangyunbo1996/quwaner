from . import auth
from .forms import RegisterForm,LoginForm
from ..models import User
from ..utils.email import send_mail,email_server
from .. import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import render_template,redirect,flash,request,url_for,make_response,current_app
from flask_login import login_user,current_user,login_required,logout_user

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
@login_required
def jumpEmail():
    server = current_user.email.split('@')[-1:][0]
    server_url = email_server[server]
    return render_template('auth/jumpEmail.html',url=server_url,user=current_user)

@auth.route('/confirm')
@login_required
def confirm():
    if current_user.confirmed == True:
        return redirect(url_for('main.index'))
    token = request.args.get('token')
    if current_user.confirm(token):
        flash('账号验证成功')
    else:
        flash('验证失败或验证链接已过期')
    return redirect(url_for('main.index')) 

@auth.route('/reconfirm')
@login_required
def reconfirm():
    if current_user.confirmed == True:
        return redirect(url_for('main.index'))
    token = current_user.generate_confirm_token()
    send_mail(recipient=current_user.email, subject='请验证你的趣玩儿账户',
                    template='auth/email/confirm', user=current_user, 
                    token=token)
    flash('重新发送验证邮件成功')
    return redirect(url_for('main.index'))

@auth.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.index'))
        flash('登陆失败，邮箱地址或密码错误')
    return render_template('auth/login.html', form=form, user=current_user)

@auth.route('/logout')
@login_required
def logout():
    try:
        logout_user()
    except:
        flash('注销失败，请重试')
    return redirect(url_for('main.index'))