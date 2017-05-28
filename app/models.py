from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from flask import current_app
from . import db,login_manager
from .utils.email import send_mail
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


like = db.Table('like',
                db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
                db.Column('travel_id',db.Integer,db.ForeignKey('travel.id')))


user_tag = db.Table('user_tag',
                    db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
                    db.Column('tag_id',db.Integer,db.ForeignKey('tag.id')))


travel_tag = db.Table('travel_tag',
                    db.Column('travel_id',db.Integer,db.ForeignKey('travel.id')),
                    db.Column('tag_id',db.Integer,db.ForeignKey('tag.id')))


class Follow(db.Model):
    follower_id = db.Column(db.Integer,db.ForeignKey('user.id'),primary_key=True) #粉丝
    followed_id = db.Column(db.Integer,db.ForeignKey('user.id'),primary_key=True) #被关注的人
    timestamp = db.Column(db.DateTime,default=datetime.now)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return '<Tag:{}>'.format(self.name)


class PrivateMessage(db.Model):
    sender_id = db.Column(db.Integer,db.ForeignKey('user.id'),primary_key=True)
    recipient_id = db.Column(db.Integer,db.ForeignKey('user.id'),primary_key=True)
    timestamp = db.Column(db.DateTime,default=datetime.now)
    detail_message = db.Column(db.String(200))
    reader = db.Column(db.Boolean,default=False)

    def __init__(self,sender,recipient,detail_message):
        self.sender_id = sender.id
        self.recipient_id = recipient.id
        self.detail_message = detail_message

    def __repr__(self):
        return '<PrivateMessage:{} to {}({})>'.format(self.sender_id,self.recipient_id,
                                                        self.detail_message)


class User(db.Model,UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), unique = True)
    username = db.Column(db.String(40), unique = True)
    password_hash = db.Column(db.String(130))
    school = db.Column(db.String(40))
    province = db.Column(db.String(20))
    city = db.Column(db.String(40))
    register_time = db.Column(db.DateTime,default=datetime.now)
    avatar = db.Column(db.String(200))
    confirmed = db.Column(db.Boolean,default=False)
    travels = db.relationship('Travel',backref='user',lazy='dynamic')
    followers = db.relationship('Follow',foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed',lazy='joined'),
                                lazy='dynamic',
                                cascade='all,delete-orphan')
    followed = db.relationship('Follow',foreign_keys=[Follow.follower_id],
                                backref=db.backref('follower',lazy='joined'),
                                lazy='dynamic',
                                cascade='all,delete-orphan')
    likes = db.relationship('Travel',secondary=like,
                            backref=db.backref('likeusers',lazy='dynamic'))
    comments = db.relationship('Comment',backref='user',lazy='dynamic')
    tags = db.relationship('Tag',secondary='user_tag',
                            backref=db.backref('users',lazy='dynamic'))
    system_messages = db.relationship('SystemMessage',backref='user',
                                        lazy='dynamic')
    send_messages = db.relationship('PrivateMessage',
                                    foreign_keys=[PrivateMessage.sender_id],
                                    backref=db.backref('senders',lazy='joined'),
                                    lazy='dynamic',
                                    cascade='all,delete-orphan')
    recive_messages = db.relationship('PrivateMessage',
                                      foreign_keys=[PrivateMessage.recipient_id],
                                      backref=db.backref('recipients',lazy='joined'),
                                      lazy='dynamic',
                                      cascade='all,delete-orphan')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def generate_confirm_token(self):
        s = Serializer(current_app.config['SECRET_KEY'],expires_in=1800)
        token = s.dumps({'confirm':self.id})
        return token

    def confirm(self,token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            confirm_info = s.loads(token)
        except:
            return False
        else:
            confirm_id = confirm_info.get('confirm')
            if confirm_id != self.id:
                return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User:{}>'.format(self.username)
        

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

    
class Travel(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    begin_time = db.Column(db.DateTime)
    travel_days = db.Column(db.Integer)
    avg_cost = db.Column(db.Float)
    destination = db.Column(db.String(40))
    body = db.Column(db.Text)
    background_img = db.Column(db.String(200))
    publish_time = db.Column(db.DateTime,default=datetime.now)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    comments = db.relationship('Comment',backref='travel',lazy='dynamic')
    tags = db.relationship('Tag',secondary='travel_tag',
                            backref=db.backref('travels',lazy='dynamic'))

    def __init__(self,title,begin_time,travel_days,avg_cost,
                destination,body,background_img,user_id):
        self.title = title
        self.begin_time = begin_time
        self.travel_days = travel_days
        self.avg_cost = avg_cost
        self.destination = destination
        self.body = body
        self.background_img = background_img
        self.user_id = user_id
            
    def __repr__(self):
        return '<Travel:{}>'.format(self.title)


class Comment(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    travel_id = db.Column(db.Integer,db.ForeignKey('travel.id'))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime,default=datetime.now)

    def __init__(self,user_id,travel_id,body):
        self.user_id = user_id
        self.travel_id = travel_id
        self.body = body

    def __repr__(self):
        return '<Comment:{}>'.format(self.body[:5] + '...')


class SystemMessage(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(40))
    timestamp = db.Column(db.DateTime,default=datetime.now)
    detail_message = db.Column(db.String(200))
    readed = db.Column(db.Boolean,default=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
