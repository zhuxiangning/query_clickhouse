#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python 3.7

# @Time     : 2021/2/22 20:22
# @Author   : 'Lou Zehua'
# @File     : __init__.py.py

from flask import Flask

app = Flask(__name__, static_folder='../', static_url_path='')

from app import routes
