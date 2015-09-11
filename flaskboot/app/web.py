# -*- coding: utf-8 -*-
#! /usr/bin/env python
import os

from flask import Flask,render_template,session,redirect,url_for,flash
#本地化时间
from flask_moment import Moment
#处理表单
from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired

from flask_script import Manager

from datetime import datetime
from flask_bootstrap import Bootstrap

##数据库操作
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__name__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

#数据库的相关配置
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

boot = Bootstrap(app)
#本地化时间
moment = Moment(app)

manager = Manager(app)

@app.route('/',methods=['GET','POST'])
def index():
    form = NameForm()
    #validate_on_submit函数验证提交的数据是否正确
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name !=form.name.data:
            flash(u'你居然修改自己的名字，你妈知道吗？')
        session['name'] = form.name.data
        return redirect(url_for('index'))

    #将数据传值给前段页面引用
    return render_template('index.html',
                           current_time=datetime.utcnow(),
                           form=form,
                           name=session.get('name'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500
#创建了文本框和提交按钮
class NameForm(Form):
    #DataRequired验证是否有数据输入
    name = StringField(u'你是谁?',validators=[DataRequired()])
    submit = SubmitField(u'提交')

#数据模型定义
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    #指定外键
    users = db.relationship('User',backref='role')
    def __repr__(self):
        return '<Role %r>' % self.name
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    #关于外键的设置
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    def __repr__(self):
        return '<User %r>' % self.username

if __name__ =='__main__':
    manager.run()

