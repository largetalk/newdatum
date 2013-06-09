#!/usr/bin/env python
import argparse

wi = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
VerC = [1, 0, 'X', 9, 8, 7, 6, 5, 4, 3, 2]
def check(num):
    if len(num) < 17:
        raise 'too short'
    i = 0
    total = 0
    for x in num[:17]:
        total += int(x) * wi[i]
        i += 1
    y = total%11
    return VerC[y]


parser = argparse.ArgumentParser(description='check mainland id correct or not')
parser.add_argument('-c',  dest='id', type=str, help='check id', required=True)

args = parser.parse_args()

try:
    tail = check(args.id)
    if args.id[17].upper() == str(tail):
        print args.id, ' is valid'
    else:
        print args.id, ' is invalid'
except:
    print 'too short'
