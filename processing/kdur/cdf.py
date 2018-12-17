import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from collections import Counter
from sys import argv, setrecursionlimit

setrecursionlimit(1500)

def getCounts(f):
	for l in f:
		break
	start = 0
	for l in f:
		start = int(l.split(',')[-1])
		break

	counts = Counter()
	for l in f:
		line = l.split(',')
		t = int(line[-1])
		op = line[0]
		if (t >= start + 20000 and op in ("U","W")):
			lat = int(float(line[3]))
			if lat < 2000:
				counts[lat] += 1
	return counts

cumsum = lambda X: X[:1] + cumsum([X[0]+X[1]] + X[2:]) if X[1:] else X


w1 = open(argv[1])
w1j = open(argv[2])

w1_c = getCounts(w1)
w1j_c = getCounts(w1j)

x = range(1,1000)

w1_avg = sum((w1_c[a]*a for a in x))/sum((w1_c[a] for a in x))
w1j_avg = sum((w1j_c[a]*a for a in x))/sum((w1j_c[a] for a in x))
kdur = w1j_avg - w1_avg
print("time to disk =", kdur)

kdur = int(kdur)
x = range(0, 1000)

w1_y = [w1_c[a] for a in x]
kd_y = [w1j_c[a] for a in x]

w1_cum = cumsum(w1_y)
kd_cum = cumsum(kd_y)

w1_cum = [a/w1_cum[-1] for a in w1_cum]
kd_cum = [a/kd_cum[-1] for a in kd_cum]

plt.ylabel("Fraction of writes")
plt.xlabel("Latency (in milliseconds)")
plt.plot(x, w1_cum, label="Primary write concern")
plt.plot(x, kd_cum, label="Estimated as durable")
plt.legend()

plt.savefig("{}cum.png".format(argv[3]))
