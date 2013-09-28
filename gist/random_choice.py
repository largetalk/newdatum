#!/usr/bin/python

from random import choice
import string
import collections
from matplotlib.pyplot import plot, show, barh, yticks, xlabel, title, figure
import numpy as np

tables = string.ascii_letters + string.digits

counter = collections.Counter()

for _ in range(1000000):
    counter[choice(tables)] += 1

alphats = counter.keys()
y_pos = np.arange(len(alphats))
freq = counter.values()

figure(figsize=(100,100))
barh(y_pos, freq, align='edge', alpha=1, height=0.05)
yticks(y_pos, alphats)
xlabel('frequence')
title('random choice')

show()
