#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Python 3.7

# @Time     : 2021/2/4 20:19
# @Author   : 'Lou Zehua'
# @File     : profile.py

encoding = 'utf-8'

# ----------------------------------------------------------------------------------------------------------------------
#  Default settings
# ----------------------------------------------------------------------------------------------------------------------
WHICH_TABLE = 0
tables = ["github_log.year2019", "github_log.year2020"]
pre_processor = 'pre-processor.js'
sql = 'sql'
manifest = 'manifest.json'
post_processor = 'post-processor.js'
image_svg = "image.svg"

# ----------------------------------------------------------------------------------------------------------------------
#  Authentication settings
# ----------------------------------------------------------------------------------------------------------------------
USERNAME = "*"
PASSWORD = "*"  # replace '\' with '\\'.
SSH_PRIVATE_KEY = "*"  # optional: the path of your ssh_private_key file 'id_rsa'
REMOTE_SERVER_IP = "*"
REMOTE_SERVER_PORT = 22
PRIVATE_SERVER_IP = "*"
PRIVATE_SERVER_PORT = 3306
MYSQL_USERNAME = '*'
MYSQL_PASSWORD = '*'
USE_DATABASE = '*'


# ----------------------------------------------------------------------------------------------------------------------
# How to show results
# ----------------------------------------------------------------------------------------------------------------------
SHOW_TABLE = 0
SHOW_SVG = 1
