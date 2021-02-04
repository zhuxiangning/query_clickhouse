#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python 3.6

__author__ = 'Lou Zehua <cs_zhlou@163.com>'
__time__ = '2019/6/16 0016 16:47'


# Return True if any word in words is a substring of sentence string
def isAnyWordWithinStr(words, sent):
    for word in words:
        if word and word in sent:
            return True
    return False
