#!coding:utf8
import re

YN_PATTERN = re.compile(ur'[\u1e00-\u1eff]+')

#def extractTCVN(line):
#    print line
#    if YN_PATTERN.search(line) is None:
#        return [(line, False)]
#
#    spl = line.split('"')
#    ret = []
#    for i in range(len(spl)):
#        l = spl[i]
#        if i%2 == 0:
#            ret.append((l, False))
#            continue
#        ret.append((u'"', False))
#        if len(l) < 1 or YN_PATTERN.search(l) is None:
#            ret.append((l, False))
#        else:
#            iidx = l.find('/')
#            if iidx != -1:
#                ret.append((l[:iidx], True))
#                ret.append((l[iidx:], False))
#            else:
#                ret.append((l, True))
#        ret.append((u'"', False))
#    return ret

class State(object):
    NORMAL = 1
    PRE_TCVN = 2
    IN_PAIR = 3
    IN_TCVN = 4
    END_TCVN = 5
    END = 6

    STAND_BY = 7

class Automat(object):
    def __init__(self):
        self.pre_state = None
        self.state = State.NORMAL
        self.ret = []
        self.normal = []
        self.tcvn = []
        self.stand = []

    def processNormal(self):
        if len(self.normal) > 0:
            self.ret.append((''.join(self.normal), False))
            self.normal = []
    def processTcvn(self):
        if len(self.tcvn) > 0:
            self.ret.append((''.join(self.tcvn), True))
            self.tcvn = []

    def caseNormal(self, c):
        self.normal.append(c)
        if c == '"':
            self.state = State.PRE_TCVN

    def casePreTCVN(self, c):
        if c in [' ', '\t', ',', ':', '(', ')', '*', '+', '[', ']', '!', '{', '}', '.', '?', '>']:
            self.normal.append(c)
        elif c == '"':
            self.normal.append(c)
            self.state = State.NORMAL
        elif c == '<':
            self.normal.append(c)
            self.state = State.IN_PAIR
        elif c == '/':
            self.normal.append(c)
            self.state = State.END_TCVN
        elif c == '%' or c == '\\':
            self.stand.append(c)
            self.state = State.STAND_BY
        else:
            self.processNormal()
            self.tcvn.append(c)
            self.state = State.IN_TCVN

    def caseInPair(self, c):
        self.normal.append(c)
        if c == '>':
            self.state = State.PRE_TCVN

    def caseInTcvn(self, c):
        if c == '"':
            self.processTcvn()
            self.normal.append(c)
            self.state = State.NORMAL
        elif c == '/':
            self.processTcvn()
            self.normal.append(c)
            self.state = State.END_TCVN
        elif c == '<':
            self.processTcvn()
            self.normal.append(c)
            self.state = State.IN_PAIR
        elif c in [' ', ',', '%']:
            self.stand.append(c)
            self.state = State.STAND_BY
        else:
            self.tcvn.append(c)

    def caseStandBy(self, c):
        if self.pre_state == State.PRE_TCVN:
            pre_c = self.stand[-1]
            self.normal.extend(self.stand)
            self.stand = []
            self.state = State.PRE_TCVN
            if pre_c == '%' and c in ['s', '%', 'd', 'f', 'Y', 'H', 'm', 'M', 'S', 'y', 'q']:
                self.normal.append(c)
            elif pre_c == '\\' and c in ['n', 't', 'r', '\\']:
                self.normal.append(c)
            else:
                self.casePreTCVN(c)
        if self.pre_state == State.IN_TCVN:
            pre_c = self.stand[-1]
            if c in [' ', ',', '%']:
                self.stand.append(c)
            elif pre_c == '%' and c in ['s', 'd', 'f', 'Y', 'H', 'm', 'M', 'S', 'y', 'q']:
                self.processTcvn()
                self.normal.extend(self.stand)
                self.normal.append(c)
                self.stand = []
                self.state = State.PRE_TCVN
            elif c in ['"', '/', '<']:
                self.normal.extend(self.stand)
                self.stand = []
                self.caseInTcvn(c)
            else:
                self.tcvn.extend(self.stand)
                self.stand = []
                self.tcvn.append(c)
                self.state = State.IN_TCVN

    def caseEndTcvn(self, c):
        self.normal.append(c)
        if c == '"':
            self.state = State.NORMAL

    def feed(self, c):
        if self.state != State.STAND_BY:
            self.pre_state = self.state
        if self.state == State.NORMAL:
            return self.caseNormal(c)
        if self.state == State.PRE_TCVN:
            return self.casePreTCVN(c)
        if self.state == State.IN_PAIR:
            return self.caseInPair(c)
        if self.state == State.IN_TCVN:
            return self.caseInTcvn(c)
        if self.state == State.END_TCVN:
            return self.caseEndTcvn(c)
        if self.state == State.STAND_BY:
            return self.caseStandBy(c)

    def end(self):
        self.processNormal()
        return self.ret


excludes = ['\\script\\', '\\image\\', '\\sound\\', '\\music\\', '.mp3', '.wav']

def extractTCVN(line):
    #print '########'
    #print line
    if line.count('"') % 2 != 0:
        return [(line, False)]
    #if YN_PATTERN.search(line) is None:
    #    return [(line, False)]
    pidx = 0
    flag = False
    ret = []
    while True:
        nidx = line.find('"', pidx)
        if nidx == -1:
            if pidx < len(line):
                ret.append((line[pidx:], flag))
            break
        elif nidx == pidx:
            if flag:
                ret.append(('""', False))
            pidx += 1
            flag = not flag
        else:
            if flag:
                ret.extend(extractInQuote(line[pidx-1:nidx+1]))
                #ret.append((line[pidx-1:nidx+1], flag))
            else:
                ret.append((line[pidx:nidx], flag))
            flag = not flag
            pidx = nidx + 1
   
    rlen = sum([len(x[0]) for x in ret])
    if len(line) != rlen:
        print '#########auto extract error', line
        return [(line, False)]
    return ret
        

def extractInQuote(line):
    if YN_PATTERN.search(line) is None:
        return [(line, False)]
    for e in excludes:
        if e in line:
            return [(line, False)]
    auto = Automat()
    for c in line:
        auto.feed(c)
    ret = auto.end()
    #rlen = sum([len(x[0]) for x in ret])
    #if len(line) != rlen:
    #    print '#########auto extract error', line
    #    return [(line, False)]
    return ret


if __name__ == '__main__':
    l1 = u'  local tName = {"Chế tạo binh khí dài", "Chế tạo binh khí ngắn", "Chế tạo kỳ môn binh khí", "Làm hộ giáp", "Hạ trang", "Đầu quán"};'
    l2 = u'     str = str.."<color=gold>"..v.."<color>,"'
    l3 = u'         local msg = g_szTitle..format("Hiện tại chỉ có thể thăng cấp kỹ năng %s, <color=gold>%s<color> đang đạt cấp <color=green>%d<color>, muốn thăng cấp <color=gold>%s<color> đến cấp <color=green>%d<color> không?",)'
    l4 = u'         Say(msg, 2, format("Đồng ý/#upgrade_compose_skill_do(%d, %d)", v, nMax), "Hủy bỏ/nothing")'
    l5 = u'     "<sex> đã gia nhập môn phái."'
    l6 = u'    this.msCamp:turnPlayer(0, SendScript2Client, [[Add3EElf(450,350,"\\image\\EFFECT\\sfx\\其他\\战斗开始_越南.3e",1000*2,0.7)]])'
    print filter(lambda x: x[1], extractTCVN(l1))
    print filter(lambda x: x[1], extractTCVN(l2))
    print filter(lambda x: x[1], extractTCVN(l3))
    print filter(lambda x: x[1], extractTCVN(l4))
    print filter(lambda x: x[1], extractTCVN(l5))
    print filter(lambda x: x[1], extractTCVN(l6))

    #l7 = u'aaa"bbb"ccc'
    #print extractTCVN(l7)
    #l7 = u'aaa"bbb"'
    #print extractTCVN(l7)
    #l7 = u'"bbb"'
    #print extractTCVN(l7)
    #l7 = u'"aaa"bbb'
    #print extractTCVN(l7)
    #l7 = u'aaa""bbb'
    #print extractTCVN(l7)
    #l7 = u'""'
    #print extractTCVN(l7)
