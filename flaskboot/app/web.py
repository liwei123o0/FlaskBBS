# -*- coding: utf-8 -*-
#! /usr/bin/env python

from flask import Flask,render_template
from flask_moment import Moment
from flask_wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
boot = Bootstrap(app)
#本地化时间
moment = Moment(app)

@app.route('/',methods=['GET','POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data=''
    return render_template('index.html',
                           current_time=datetime.utcnow(),
                           form=form,
                           name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500

class NameForm(Form):
    name = StringField(u'你是谁?',validators=[DataRequired()])
    submit = SubmitField(u'提交')

if __name__ =='__main__':
    app.run(debug=True)

