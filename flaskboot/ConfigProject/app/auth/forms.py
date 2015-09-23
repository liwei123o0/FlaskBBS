# -*- coding: utf-8 -*-
#! /usr/bin/env python

#处理表单
from flask_wtf import Form
from wtforms import StringField,SubmitField,PasswordField,BooleanField
from wtforms.validators import DataRequired,Length,Email

#创建了文本框和提交按钮
class LoginForm(Form):
    email = StringField(u'邮箱登陆',validators=[DataRequired(),Length(1,64),Email(message=u'请输入正确的邮箱账号！')])
    password = PasswordField(u'密码',validators=[DataRequired()])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登陆')
