#! /usr/bin/env python3
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
from config import *
from sys import argv

docs = {}
errored_writes = {}

ops = []

state = 0

errors = set()
docs_missing_writes = set()
unack_writes = set()

stats_line = input().split(',')
fail_time = int(stats_line[0])
fix_time = int(stats_line[1])
first = True

while True:
    try:
        text = input()
    except EOFError:
        break
    

    fields = text.split(',')

    time = int(fields[-1])

    if first:
        first = False
        start_time = time

    if (time > fix_time):
        state = 2

    elif (time > fail_time):
        state = 1

    op = fields[0]

    if op == "R":
        doc, actual, duration, time = fields[1:]
        expected = docs[doc][0]
        actual = int(actual)
        duration = float(duration)
        time = int(time)
        ops.append(("R", doc, duration, state, time))
        if actual != expected:
            if doc in errored_writes:
                for v,s in errored_writes[doc]:
                    if actual == v:
                        docs[doc] = (v,s)
                        break
                del errored_writes[doc]
                unack_writes.add((doc, *docs[doc]))
            else:
                docs_missing_writes.add((doc, *docs[doc]))

    if op == "U":
        doc, val, duration, time = fields[1:]
        val = int(val)
        duration = float(duration)
        time = int(time)
        ops.append(("U", doc, duration, state, time))

        docs[doc] = (val, state, time)

    if op == "W":
        doc, val, duration, time = fields[1:]
        val = int(val)
        duration = float(duration)
        time = int(time)
        ops.append(("W", doc, duration, state, time))
        docs[doc] = (val, state)

    if op == "ERR":
        err_op, id, val, lat, time = fields[1:]
        val = int(val)
        time = int(time)
        errors.add((err_op, id, val, state, time))
        if err_op in {"W", "U"}:
            if id not in errored_writes:
                errored_writes[id] = []
            errored_writes[id].insert(0, (val, time))


	

print(docs_missing_writes)
print(start_time)
start_time = start_time//1000
finish_time = ops[-1][-1]//1000
dur = finish_time - start_time

missing_count = Counter()
error_count = Counter()
for e in errors:
	t = e[-1]//1000 - start_time
	error_count[t] += 1

for d in docs_missing_writes:
	t = d[-1]//1000 - start_time
	missing_count[t] += 1

x = range(dur)
y = [missing_count[i] for i in x]
y2 = [error_count[i] for i in x]

plt.plot(x,y)
plt.xlabel("Time of experiment (in seconds)")
plt.ylabel("Number of writes lost")
plt.savefig("{}{}_graph.png".format(PROCESSING_FAILURES_RESULT_PATH, argv[1]))
