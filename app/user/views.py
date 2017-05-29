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
    followers = [User.query.get(user.follower_id) for user in number_of_followers]
    number_of_followed = current_user.followed.all()
    followed = [User.query.get(user.followed_id) for user in number_of_followed]
    number_of_friends = len(set(followers) & set(followed))
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

@user_blueprint.route('/verifySchool',methods=['GET','POST'])
@login_required
def verifySchool():
    if request.method == 'POST':
        school = request.form.get('school')
        if school == '' or school == '点击选择学校':
            flash('请选择学校')
        else:
            current_user.school = school
            db.session.add(current_user)
            db.session.commit()
            flash('认证学校成功')
            return redirect(url_for('main.index'))
    return render_template('user/verifySchool.html', user=current_user)

@user_blueprint.route('/userinfo/<int:id>')
def userinfo(id):
    user = User.query.get_or_404(id)
    if user == current_user:
        return redirect(url_for('user.personalInfo'))
    number_of_travels = len(user.travels.all())
    number_of_followers = user.followers.all()
    followers = [User.query.get(follower_user.follower_id) for follower_user in number_of_followers]
    number_of_followed = user.followed.all()
    followed = [User.query.get(followed_user.followed_id) for followed_user in number_of_followed]
    number_of_friends = len(set(followers) & set(followed))
    travels = user.travels.all()
    return render_template('user/userinfo.html', user=current_user, this_user=user, travels=travels,
        number_of_travels=number_of_travels, number_of_followers=len(number_of_followers),
        number_of_followed=len(number_of_followed), number_of_friends=number_of_friends)

@user_blueprint.route('/follow/<int:id>')
@login_required
def follow(id):
    user = User.query.get_or_404(id)
    if current_user == user:
        flash('不能关注自己')
        return redirect(url_for('user.userinfo',id=id))        
    if current_user.is_following(user):
        flash('不允许重复关注')
        return redirect(url_for('user.userinfo',id=id))
    current_user.follow(user)
    flash('关注成功')
    return redirect(url_for('user.userinfo',id=id))

@user_blueprint.route('/unfollow/<int:id>')
@login_required
def unfollow(id):
    user = User.query.get_or_404(id)
    if not current_user.is_following(user):
        flash('不允许取消关注一个你没有关注的人')
        return redirect(url_for('user.userinfo',id=id))
    current_user.unfollow(user)
    flash('取消关注成功')
    return redirect(url_for('user.userinfo',id=id))

@user_blueprint.route('/fans/<int:id>')
@login_required
def fans(id):
    user = User.query.get_or_404(id)
    fans = [User.query.get(follow_object.follower_id) for follow_object in user.followers.all()]
    return render_template('user/fans.html', user=current_user, this_user=user, fans=fans, len=len)

@user_blueprint.route('/followed/<int:id>')
@login_required
def followed(id):
    user = User.query.get_or_404(id)
    followeds = [User.query.get(follow_object.followed_id) for follow_object in user.followed.all()]
    return render_template('user/followed.html', user=current_user, this_user=user, followeds=followeds, len=len)