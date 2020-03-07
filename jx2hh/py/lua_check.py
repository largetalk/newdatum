import os
import sys

def check_lua(base_dir):
    base_dir = os.path.abspath(base_dir)
    for root, dirs, files  in os.walk(base_dir):
        for filename in files:
            if filename.endswith('.lua'):
                luaFn = os.path.join(root, filename)
                u8Fn = '%s.u8' % luaFn
                tsFn = '%s.ts' % u8Fn
                if not os.path.exists(tsFn):
                    continue
                luaC = tsC = 0
                for luaC, l in enumerate(open(luaFn, 'rU')):
                    pass
                for tsC, l in enumerate(open(tsFn, 'rU')):
                    pass
                if luaC != tsC:
                    print luaFn, 'error'

if __name__ == '__main__':
    root = '/Users/largetalk/Downloads/jx2JQ/gs/script/'
    check_lua(root)

