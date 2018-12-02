#! /usr/bin/env python3

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

while True:
    try:
        text = input()
    except EOFError:
        break

    fields = text.split(',')

    time = int(fields[-1])

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
        ops.append(("R", doc, duration, state))
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
        ops.append(("U", doc, duration, state))

        docs[doc] = (val, state)

    if op == "W":
        doc, val, duration, time = fields[1:]
        val = int(val)
        duration = float(duration)
        time = int(time)
        ops.append(("W", doc, duration, state))
        docs[doc] = (val, state)

    if op == "ERR":
        err_op, id, val, lat, time = fields[1:]
        val = int(val)
        errors.add((err_op, id, val, state))
        if err_op in {"W", "U"}:
            if id not in errored_writes:
                errored_writes[id] = []
            errored_writes[id].insert(0, (val, state))


print("Total ops:", len(ops))
print("Errors:", len(errors))
print("Missing Writes:", len(docs_missing_writes))
print()
print("Missing on:", len({d[0] for d in docs_missing_writes}), "documents")

print("Unconfirmed writes:", len(unack_writes))
print("Unconfirmed on:", len({d[0] for d in unack_writes}), "documents")

print("-----")

for i in range(3):
    if i == 0:
        print("Normal")
    if i == 1:
        print("Failure")
    if i == 2:
        print("Recovery")

    errors_seg = [e for e in errors if e[3] == i]
    miss_seg = [d for d in docs_missing_writes if d[2] == i]
    unack_seg = [u for u in unack_writes if u[2] == i]

    print("Ops:", len([ o for o in ops if o[-1] == i ]))
    print("Errors: ", len(errors_seg))
    print("Missing: ", len(miss_seg))
    print("Unacknowledged: ", len(unack_seg))
    print("-----")

