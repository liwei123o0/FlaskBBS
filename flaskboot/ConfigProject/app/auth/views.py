# -*- coding: utf-8 -*-
#! /usr/bin/env python

from flask import  render_template,redirect,request,url_for,flash
from  flask_login import login_user,login_required

from  . import auth
from ..models import User
from .forms import LoginForm



@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm(csrf_enabled=False)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash(u'用户名或密码无效!')
    return render_template('auth/login.html',
                           form=form)



@auth.route('/logout')
@login_required
def logout():
    login_user()
    flash(u'您已经成功退出！')
    return redirect(url_for('main.index'))

@auth.route('/secret')
@login_required
def secret():
    return u'您为登陆，请登录！'

