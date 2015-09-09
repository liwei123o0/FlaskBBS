# -*- coding: utf-8 -*-
#! /usr/bin/env python
from flask import Flask,request,redirect,abort,render_template

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>hello word!!! </h1>'

@app.route('/<name>')
def name(name):
    return '<h1>hello %s !</h1>'% name

#获取浏览器
@app.route('/req')
def req():
    user_agent = request.headers.get('User_Agent')
    return '<h1>Your browser is %s</h1>'% user_agent

#重定向地址 302
@app.route('/red')
def red():
    return redirect('http://www.baidu.com')

#处理404错误
@app.route('/abort/1')
def bort():
    user = ''
    if not user:
        abort(404)
    return '<h1>hello %s</h1>' % user

#使用html页面来访问
@app.route('/html')
def indexhtml():
    return render_template('index.html')

#html使用jinjia2的方式写
@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)

if __name__ =='__main__':
    app.run(debug=True)
