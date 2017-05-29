from ..models import User,Travel
from . import user_blueprint
from .. import db
from os.path import join,exists
from os import remove
from random import randint
from base64 import b64encode
from werkzeug.utils import secure_filename
from flask_login import login_required,current_user
from flask import render_template,current_app,request,flash,redirect,url_for

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

def allow_avatar(file):
    if '.' in file and \
        file.rsplit('.',1)[1].lower() in current_app.config['ALLOW_AVATAR_TYPE']:
        return True  

@user_blueprint.route('/modifyAvatar', methods=['GET','POST'])
@login_required
def modifyAvatar():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('没有文件被上传')
            return redirect(url_for('user.modifyAvatar'))
        file = request.files.get('file')
        if file.filename == '':
            flash('没有文件被上传')
            return redirect(url_for('user.modifyAvatar'))
        if file and allow_avatar(file.filename):
            filename = (b64encode(bytes(current_user.username + str(randint(1,20)),encoding='utf-8')).decode()).rstrip('=') + '.jpg'
            save_path = join(current_app.config['AVATAR_SAVE_PATH'], filename)
            old_avatar_path = join(current_app.config['AVATAR_SAVE_PATH'], current_user.avatar.rsplit('/',1)[1])
            if exists(old_avatar_path):
                remove(old_avatar_path)
            file.save(save_path)
            current_user.avatar = url_for('static', filename='images/avatars/' + filename)
            flash('修改头像成功')
            db.session.add(current_user)
            db.session.commit()
            return redirect(url_for('user.modifyAvatar'))
    return render_template('user/modifyAvatar.html',user=current_user)