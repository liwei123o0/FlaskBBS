# -*- coding: utf-8 -*-
#! /usr/bin/env python
from flask import Flask,render_template
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
app = Flask(__name__)
Bootstrap(app)

manager = Manager(app)


@app.route('/')
def index():
    return 'hello'
@app.route('/html')
def html():
    return render_template('/index.html')

if __name__ =="__main__":

    manager.run()
