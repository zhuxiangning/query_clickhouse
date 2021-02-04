#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python 3.6

import os

__author__ = 'Lou Zehua <cs_zhlou@163.com>'
__time__ = '2019/6/16 0016 16:47'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Base directory: ROOT DIRECTORY

# ----------------------------------------------------------------------------------------------------------------------
#  Define file_names
# ----------------------------------------------------------------------------------------------------------------------
# Define the relative path of directory:
# Notes:  A directory must end with a suffix '_DIR' and end with '/' in the content.
#   A path ending with a suffix '_PATH' is recommended.
SRC_DIR = 0
SQLS_DIR = 1
CASE_STUDY_SQLS_DIR = 2

RESULT_DIR = 100

absPathDict = {
    SRC_DIR: os.path.join(BASE_DIR, 'data/src/'),
    SQLS_DIR: os.path.join(BASE_DIR, 'data/src/sqls/'),
    CASE_STUDY_SQLS_DIR: os.path.join(BASE_DIR, 'data/src/case-study/sqls/'),
    RESULT_DIR: os.path.join(BASE_DIR, 'data/result/'),
}

fileNameDict = {k: v.replace('\\', '/').split('/')[-1] for k, v in absPathDict.items()}

absDirDict = {k: '/'.join(v.replace('\\', '/').split('/')[:-1]) for k, v in absPathDict.items()}
