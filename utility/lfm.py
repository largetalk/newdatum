import random

USERS = ["u1", "u2", "u3", "u4", "u5", "u6", "u7", "u8"]
ITEMS = ["i1", "i2", "i3", "i4", "i5", "i6", "i7", "i8", "i9", "i10", "i11", "i12", "i13", "i14", "i15", "i16"]

items_pool = [random.choice(ITEMS) for x in range(30)]
#items_pool = ['i3', 'i1', 'i3', 'i7', 'i6', 'i7', 'i7', 'i6', 'i5', 'i4', 'i3', 'i1', 'i6', 'i7', 'i1', 'i4', 'i4', 'i1', 'i3', 'i5', 'i6']

def genUI():
    ui = {}
    for u in USERS:
        ui[u] = {}
        rand = random.randint(2, 9)
        for x in range(0, rand):
            ui[u][random.choice(ITEMS)] = 1
    return ui

ui = genUI()

#ui ={'u1': {'i1': 1, 'i3': 1},
#     'u2': {'i1': 1, 'i3': 1, 'i4': 1},
#     'u3': {'i2': 1, 'i3': 1, 'i6': 1},
#     'u4': {'i2': 1, 'i4': 1, 'i7': 1},
#     'u5': {'i6': 1, 'i7': 1},
#     'u6': {'i1': 1, 'i2': 1, 'i6': 1},
#     'u7': {'i5': 1, 'i6': 1, 'i7': 1},
#     'u8': {'i4': 1, 'i5': 1}} 

def RandSelectNegativeSamples(items):
    ret = dict()
    for i in items.keys():
        ret[i] = 1
    n = 0
    for i in range(0, len(items) * 3):
        item = items_pool[random.randint(0, len(items_pool) - 1)]
        if item in ret:
            continue
        ret[item] = 0
        n += 1
        if n > len(items):
            break
    return ret

def InitModel(user_items, F):
    P = {}
    Q = {}
    for u in USERS:
        P[u] = {}
        sum = 0
        for f in range(0, F):
            P[u][f] = random.random()
            sum += P[u][f]
        for f in range(0, F):
            P[u][f] /= sum

    for i in ITEMS:
        sum = 0
        for f in range(0, F):
            if f not in Q:
                Q[f] = {}
            Q[f][i] = random.random()
            sum += Q[f][i]
        for f in range(0, F):
            Q[f][i] /= sum

    return P, Q

def Predict(user, item, P, Q):
    uc = P[user]
    ret = 0
    for i in range(len(uc)):
        ret += uc[i] * Q[i][item]
    return ret


def LatentFactorModel(user_items, F, N, alpha, lambd):
    P, Q = InitModel(user_items, F)
    for step in range(0, N):
        for user, items in user_items.items():
            samples = RandSelectNegativeSamples(items)
            for item, rui in samples.items():
                eui = rui - Predict(user, item, P, Q)
                for f in range(0, F):
                    P[user][f] += alpha * (eui * Q[f][item] - lambd * P[user][f])
                    Q[f][item] += alpha * (eui * P[user][f] - lambd * Q[f][item])
        alpha *= 0.9
    return P, Q

def Recommend(user, P, Q):
    rank = dict()
    for f, puf in P[user].items():
        for i, qfi in Q[f].items():
            if i not in rank:
                rank[i] = 0
            rank[i] += puf * qfi
    return rank


if __name__ == '__main__':
    P, Q = LatentFactorModel(ui, 3, 50, 0.02, 0.01)
    for u in USERS:
        print u, ":",  ui[u]
        print Recommend(u, P, Q)
        print '###############'
