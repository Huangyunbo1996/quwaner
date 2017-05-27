from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Length,Email,Regexp,Required,EqualTo,ValidationError
from ..models import User


class RegisterForm(FlaskForm):
    username = StringField('',validators=[Length(min=6,max=40,message='用户名长度要求在6~40位'),Required(),
                                                Regexp('[\u4e00-\u9fa5a-zA-Z0-9]+',message='用户名只能由字母、数字、下划线组成')],
                                                render_kw={"placeholder": "用户名"})
    email = StringField('',validators=[Required(),Email(message='请输入正确的邮箱地址')],
                                        render_kw={"placeholder": "邮箱地址"})
    password = PasswordField('',validators=[Required(),
                            Length(min=6,max=40,message='密码长度请在6位以上'),
                            Regexp('.*[a-zA-Z].*[0-9].*|.*[0-9].*[a-zA-Z].*',message='密码必须同时含有字母与数字')],
                            render_kw={"placeholder": "密码"})
    re_password = PasswordField('',validators=[Required(),
                            EqualTo('password',message='密码与重复密码必须一致。')],
                            render_kw={"placeholder": "重复密码"})
    submit = SubmitField("注册")

    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已被注册')

    def validate_username(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('此用户名已被注册')