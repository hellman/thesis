#-*- coding:utf-8 -*-

from itertools import *

def impl(a, b):
    return (a ^ 1) | b

# just or
for a, b, or_ab in product(range(2), repeat=3):
    correct = (or_ab == a | b)
    match = 1
    match &= impl(or_ab ^ b, a)
    match &= impl(a, or_ab)
    if match ^ correct:
        print "wrong:",
        print "a=%d, b=%d, v=%d" % (a, b, or_ab), "correct %d match %d" % (correct, match)

# 3-sat clause
for a, b, c, or_bc in product(range(2), repeat=4):
    correct = (a | b | c) & (or_bc == b | c)
    match = 1
    match &= impl(b, or_bc)
    match &= impl(or_bc ^ c, b)
    match &= a | or_bc
    if match ^ correct:
        print "wrong:",
        print "a=%d, b=%d, c=%d, v_bc=%d" % (a, b, c, or_bc), "correct %d match %d" % (correct, match)
