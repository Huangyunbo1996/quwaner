from . import main
from ..models import User
from flask import render_template,request
from flask_login import current_user

@main.route('/')
def index():
    return render_template('base.html',user=current_user)