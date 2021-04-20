#!/usr/bin/env python3
from run_base import run_tests
import sys
from pathlib import Path

base_args = "-o 33554432 -t 4 -T -I -S -L {}"

tests = []

for arg in sys.argv[1:]:
    if arg == "HugeTLB":
        base_args = base_args.format("-H {}")
        if not Path("/proc/cmdline").exists():
            raise RuntimeError("Only Linux is supported")
        with open("/proc/cmdline") as fd:
            content = fd.read()
            if "hugepagesz=1G hugepages=" not in content:
                raise RuntimeError("Need to allocate huge pages")
    if arg == "Baseline":
        # Baseline configuration
        # figure 2
        # no cache related operation
        tests += [base_args.format("-C 0")]
    elif arg == "Reuse":
        # Reuse configuration
        # figure 3
        # no cache related operation
        # vary the number of transactions for each size
        tests += [base_args.format("-C 0 -s 0 -n {}".format(2**n)) for n in range(0, 13)]
    elif arg == "Invalidation":
        # Invalidation
        # figure 4
        # invalidate cache
        # cap the number of transactions for each size (wbinvd is expensive)
        if not Path("/proc/wbinvd").exists():
            raise RuntimeError("Need to insert wbinvd kernel module")
        with open("/proc/wbinvd") as fd:
            content = fd.read()
            assert "WBINVD executed from CPU" in content
        tests += [base_args.format("-C 2")]
    elif arg == "Warmup":
        # Warmup
        # figure 5
        # warmup cache
        warmup_count = 5
        if not Path("/proc/cpuinfo").exists():
            raise RuntimeError("Only Linux is supported")
        with open("/proc/cpuinfo") as fd:
            content = fd.read()
            if "i7-4770" in content:
                warmup_count = 128
        tests += [base_args.format("-C 1 -w {}".format(warmup_count))]
    elif arg == "WarmupIter":
        # Sufficient warmup count
        # figure 6
        # Cap the number of txns to 16, the experiment is very expensive
        tests += [base_args.format("-C 1 -w {} -n 16".format(2**n)) for n in range(0, 9)]

print("Execute the following tests?")
for test in tests:
    print(test)
answer = input("y/n? ")
if answer == "y" or answer == "Y":
    run_tests(tests)
