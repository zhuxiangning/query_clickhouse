#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python 3.6
import threading

__author__ = 'Lou Zehua <cs_zhlou@163.com>'
__time__ = '2019/6/16 0016 16:47'


# Singleton pattern
class SingletonType(type):
    _instance_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with SingletonType._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super(SingletonType,cls).__call__(*args, **kwargs)
        return cls._instance
