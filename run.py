#!/usr/bin/env python3
import sys
import subprocess
import socket
import time

# -L -t 4 -s -I -S -o 33554432 -c 33554432
tests = sys.argv[1:]
if not tests:
    tests = []
    tests += ["-o 33554432 -t 4 -T -I -S -L -C 0"] # read, baseline
    tests += ["-o 33554432 -t 4 -T -I -S -L -C 0 -s 0 -n {}".format(2**n) for n in range(0, 13)] # read, reuse
    tests += [
        "-o 33554432 -t 5 -T -I -S -L -C 1", # read, warmup
        "-o 33554432 -t 4 -T -I -S -L -C 2", # read, wbinvd
    ]
    tests += ["-o 33554432 -t 5 -T -I -S -L -C 0"] # write, baseline
    tests += ["-o 33554432 -t 5 -T -I -S -L -C 0 -s 0 -n {}".format(2**n) for n in range(0, 13)] # write, reuse
    tests += [
        "-o 33554432 -t 5 -T -I -S -L -C 1", # write, warmup
        "-o 33554432 -t 5 -T -I -S -L -C 2", # write, wbinvd
    ]

for test in tests:
    raw_args = test.split()
    args = []
    for token in raw_args:
        if token.isdigit():
            args[-1] = (args[-1][0], token)
        else:
            args.append((token, ""))

    encode_args = "".join([arg[0][1:] + arg[1] for arg in args])

    log_name = "{}-{}-{}.log".format(socket.gethostname(), int(time.time()), encode_args)
    cmd = ["./rtm-bench"]
    cmd.extend(raw_args)
    print("{} > {}".format(" ".join(cmd), log_name))
    with open(log_name, "w") as fd:
        subprocess.run(cmd, stdout = fd)
