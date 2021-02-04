#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python 3.6
import os

__author__ = 'Lou Zehua <cs_zhlou@163.com>'
__time__ = '2019/6/16 0016 16:47'


def create_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    return None


def create_fpath(path):
    if not os.path.exists(path):
        create_dir('/'.join(path.replace('\\', '/').split('/')[0:-1]))
        file = open(path, 'w', encoding='utf-8')
        file.close()
    return None
