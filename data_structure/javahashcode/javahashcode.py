# -*- coding: utf-8 -*-

import ctypes

def hash_code(s):
    hash_code = 0
    for c in s:
        hash_code += (ord(c) * pow(31, len(s) - 1 - s.index(c)))

    return ctypes.c_int32(hash_code).value

print hash_code("hello world")
