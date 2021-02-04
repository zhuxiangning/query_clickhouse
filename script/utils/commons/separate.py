#!/usr/bin/env python
# -*- coding: utf-8 -*-
# python 3.6

__author__ = 'Lou Zehua <cs_zhlou@163.com>'
__time__ = '2019/6/16 0016 16:47'


# sep represent separation character. Return pair: (prefix, suffix). Default: pos=1
def separate(s, sep='-', pos=1):
    pos = pos if pos >= 0 else 0
    seg_list = s.split(sep=sep, maxsplit=-1)  # s:'a-b-c', seg_list: ['a', 'b', 'c']
    prefix = sep.join(seg_list[0:pos])  # prefix: 'a'
    suffix = sep.join(seg_list[pos:len(seg_list)])  # suffix: 'b-c'
    return prefix, suffix


def main():
    for i in range(4):
        p, s = separate('a-b-c', sep='-', pos=i)
        print(p, '|', s)
    for i in range(4):
        p, s = separate('a-b-c', sep='-', pos=-i)
        print(p, '|', s)


if __name__ == '__main__':
    main()
