from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from datetime import datetime

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), unique = True)
    username = db.Column(db.String(40), unique = True)
    password_hash = db.Column(db.String(130))
    school = db.Column(db.String(40))
    province = db.Column(db.String(20))
    city = db.Column(db.String(40))
    register_time = db.Column(db.DateTime,default=datetime.now)
    travels = db.relationship('Travel',backref='user',lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User:{}>'.format(self.username)
        
    
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