#!/usr/bin/env python
# -*- coding:utf-8 -*-
def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False


def is_number(uchar):
    """判断一个unicode是否是数字"""
    if uchar >= u'\u0030' and uchar <= u'\u0039':
        return True
    else:
        return False


def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""
    if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
        # if (uchar >= u'\u0020' and uchar <= u'\u007e'):
        return True
    else:
        return False


def is_chinaesechar(uchar):
    """判断一个unicode是否是符号"""
    c = [u'\u3001', u'\u3002', u'\u302a', u'\u302f', u'\u002c', u'\u002e', u'\uff0c', u'\u0020 ']
    if uchar in c:
        return True
    else:
        return False


def format_str(content):
    content_str = ''
    for i in content:
        if is_chinese(i) or is_number(i) or is_alphabet(i) or is_chinaesechar(i):
            content_str = content_str + i
    return content_str
