import random
import time
import string
import timeit
import hashlib
import uuid

def randomchoice():
    return ''.join([ random.choice(string.lowercase + string.digits) for _ in range(6)])

SALT_KEY = 'SI&*(SD'

def short_url():
    long_url = str(uuid.uuid1())
    array = string.ascii_letters + string.digits
    m = hashlib.md5()
    m.update(SALT_KEY + long_url)
    md5 = m.hexdigest()
    short_url_lst = []
    for i in range(4):
        part_str = ''
        part = int(md5[i*8 : i*8 + 8], 16) & 0x3FFFFFFF
        for j in range(6):
            part_str += array[part & 0x0000001F]
            part = part >> 5
        short_url_lst.append(part_str)
    return short_url_lst[random.randint(0,3)]


def _time(f, n=1000000):
    print 'start timeit function ', f
    t = timeit.timeit(f, number=n)
    print 'repeat %s times and used %ss' % (n, t)
    print 'end timeit function ', f
    print

_time(randomchoice)
_time(short_url)


def _collide(f, n=1000000):
    print 'start _collide function ', f
    dic = {}
    col = 0
    for _ in xrange(n):
        r = f()
        if r in dic:
            col + 1
        else:
            dic[r] = 1
    rate = float(col) / n
    print 'repeat %s times and collision %s times, collsion rate is %s' % (n , col, rate)
    print 'end _collide function ', f
    print 

_collide(randomchoice)
_collide(short_url)
