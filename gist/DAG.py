def get_DAG(sentence):
    WORD_MAX = 8
    n = len(sentence)
    i,j = 0,0
    DAG = {}
    while i < n:
        for j in xrange(i, min(n,i+WORD_MAX), 1):
            if sentence[i:j+1] in FREQ:
                if not i in DAG:
                    DAG[i]=[]
                DAG[i].append(j)
        i += 1
        j = i
    for i in xrange(len(sentence)):
        if not i in DAG:
            DAG[i] =[i]
    return DAG
