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

from flask_script import Manager,Shell

from datetime import datetime
from flask_bootstrap import Bootstrap

##数据库操作
from flask_sqlalchemy import SQLAlchemy

#数据库迁移模块
from flask_migrate import Migrate,MigrateCommand

#邮件发送服务模块
from  flask_mail import Mail,Message

basedir = os.path.abspath(os.path.dirname(__name__))

app = Flask(__name__)

#配置模块
app.config['SECRET_KEY'] = 'hard to guess string'
#数据库的相关配置
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
#邮件配置
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '877129310@qq.com'
app.config['MAIL_PASSWORD'] = 'xiaowei429'
app.config['MAIL_ADMIN'] = 'liwei'
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = u'Hi,我的第一封邮件!'
app.config['FLASKY_MAIL_SENDER'] = u'Flasky发送的邮件<877129310@qq.com>'
#初始化相关功能扩展模块
db = SQLAlchemy(app)
boot = Bootstrap(app)
#邮件服务初始化
mail = Mail(app)
#本地化时间
moment = Moment(app)
#数据库迁移模块使用
migrate = Migrate(app,db)

#flask启动管理模块
manager = Manager(app)
#为启动管理模块添加数据迁移命令
manager.add_command('db',MigrateCommand)

@app.route('/',methods=['GET','POST'])
def index():
    form = NameForm()
    #validate_on_submit函数验证提交的数据是否正确
    if form.validate_on_submit():
        #按提交信息查询数据库是否有该信息
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            flash(u'数据表里面无此姓名，添加进数据库！')
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if app.config['MAIL_ADMIN']:
                send_mail(app.config['MAIL_ADMIN'],
                          u'有新注册人员进来了！',
                          'mail/new_user',
                          user=user)
        else:
            flash(u'数据库此人姓名已存在,不做重复添加!')
            session['known'] = True

    #     old_name = session.get('name')
    #     if old_name is not None and old_name !=form.name.data:
    #         flash(u'你居然修改自己的名字，你妈知道吗？')
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))

    #将数据传值给前段页面引用
    return render_template('index.html',
                           current_time=datetime.utcnow(),
                           form=form,
                           name=session.get('name'),
                           known = session.get('known',False))

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

#邮件内容
def send_mail(to,subject,template,**kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'],recipients=[to])
    msg.body = render_template(template + '_txt',**kwargs)
    msg.html = render_template(template + '_html', **kwargs)
    mail.send(msg)

#将特定对象导入进shell里面
def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role)
manager.add_command('shell',Shell(make_context=make_shell_context))

if __name__ =='__main__':

    manager.run()