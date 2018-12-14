#! /usr/bin/env python3
import matplotlib

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from collections import Counter, defaultdict
from sys import argv, exit
from config import *
if argv[1] == 'r':
	read = True
elif argv[1] == 'w':
	read = False
else:
	exit(1)



times = input().split(',')
fail_time = int(times[0])//1000
fix_time = int(times[1])//1000
wlatencies = defaultdict(list)
rlatencies = defaultdict(list)
errors = Counter()

while True:
    try:
        text = input()
    except EOFError:
        break

    data = text.split(',')
    time = int(data[-1])
    latency = float(data[-2])
    if data[0] == "ERR":
        errors[time//1000] += 1
    elif data[0] == "R":
        rlatencies[time//1000].append(latency)
    else:
        wlatencies[time//1000].append(latency)



x = sorted(list(rlatencies.keys()))
if read:
#	latY = [len(rlatencies[i]) for i in x]
	latY = [min(2000,sum(rlatencies[i])/(len(rlatencies[i])+1)) for i in x]
	#latY = [errors[i] for i in x]
else:
	#latY = [len(wlatencies[i]) for i in x]
	latY = [min(2000, sum(wlatencies[i])/(len(wlatencies[i])+1)) for i in x]
x = [t - x[0] for t in x]
t = [i for i in latY if i != 2000]
avg = sum(t)/len(t)
avgY = [avg for i in x]


text = "reads" if read else "writes"
plt.plot(x,latY)
#plt.plot(x, avgY, label="Average latency of {}".format(text))

plt.xlabel("Time of experiment (in seconds)")
plt.ylabel("Latency of {} (in milliseconds)".format(text))
plt.legend()

#plt.show()
plt.savefig("{}.png".format(argv[2]))
