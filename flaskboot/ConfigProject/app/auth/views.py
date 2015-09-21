# -*- coding: utf-8 -*-
#! /usr/bin/env python

from flask import  render_template,redirect,request,url_for,flash
from  flask_login import login_user

from  . import auth
from ..models import User
from .forms import LoginForm

@auth.route('/login',methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('用户名或密码无效!')
    return render_template('auth/login.html',
                           form=form)
