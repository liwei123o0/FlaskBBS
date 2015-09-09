# -*- coding: utf-8 -*-
#! /usr/bin/env python
from flask import Flask
from flask.ext.script import Manager

app = Flask(__name__)

manager = Manager(app)

@manager.command
def index():
    print "hello word! %s"

if __name__ =="__main__":

    manager.run()
