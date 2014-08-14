#!/usr/bin/env python
import sys

def _hash_(obj):
    if isinstance(obj, basestring):
        h = 0
        if len(obj) > 0:
            for c in obj:
                h = 31 * h + ord(c)
                h &= 0xFFFFFFFF
        return h
    raise Exception("input string")

class HashCodeBuilder:
    def __init__(self, iTotal, iConstant):
        self._iTotal = iTotal
        self._iConstant = iConstant

    def append(self, obj):
        if (obj is None):
            self._iTotal = self._iTotal * self._iConstant
        else:
            #skip list object hash
            self._iTotal = self._iTotal * self._iConstant + _hash_(obj)
        return self
    
    def toHashCode(self):
        return self._iTotal


def main(uid, numPartitions):
    if not isinstance(uid, basestring):
        uid = str(uid)
    builder = HashCodeBuilder(23, 13)
    builder.append(uid)
    blockID = abs(builder.toHashCode())
    print blockID % numPartitions

#main("14056579944214142", 1000)
if __name__ == '__main__':
    if len(sys.argv) <= 1 or sys.argv[1] == '--help':
        print ''
        print 'Usage: ' + sys.argv[0] + 'userID numPartitions'
        print ''
        sys.exit(0)
    uid = sys.argv[1]
    numPartitions = int(sys.argv[2])
    main(uid, numPartitions)

