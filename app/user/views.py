from ..models import User,Travel
from . import user_blueprint
from flask_login import login_required,current_user
from flask import render_template

@user_blueprint.route('/personalInfo')
@login_required
def personalInfo():
    number_of_travels = len(current_user.travels.all())
    number_of_followers = current_user.followers.all()
    number_of_followed = current_user.followed.all()
    number_of_friends = len(set(number_of_followers) & set(number_of_followed))
    travels = current_user.travels.all()
    return render_template('user/personalInfo.html',user=current_user, travels=travels,
        number_of_travels=number_of_travels, number_of_followers=len(number_of_followers),
        number_of_followed=len(number_of_followed), number_of_friends=number_of_friends)


@user_blueprint.route('/modifyAvatar')
@login_required
def modifyAvatar():
    return render_template('user/modifyAvatar.html',user=current_user)