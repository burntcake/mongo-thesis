import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from collections import Counter
from sys import argv

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
		if (t >= start + 20000 and op in ("U", "W")):
			lat = int(float(line[3]))
			counts[lat] += 1
	return counts
print(argv[1])
print(argv[2])
w1 = open(argv[1])
w1j = open(argv[2])

w1_c = getCounts(w1)
w1j_c = getCounts(w1j)


x = range(1,1000)

y1 = [w1_c[i] for i in x]
y2 = [w1j_c[i] for i in x]

plt.plot(x, y1, label="Primary write concern")
plt.plot(x, y2, label="Journaled write concern")

format = argv[3]
if len(argv) > 4:
	w1m = open(argv[3])
	w1m_c = getCounts(w1m)
	y3 = [w1m_c[i] for i in x]
	plt.plot(x, y3, label="Majority write concern")
	format = argv[4]

plt.ylabel("Number of operations")
plt.xlabel("Latency (in milliseconds)")
plt.legend()


plt.savefig("{}latencies.png".format(format))
