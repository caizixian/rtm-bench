#!/usr/bin/env python3
import pathlib
import sys
import subprocess

pattern = sys.argv[1]
for log in pathlib.Path(".").glob(pattern):
    print(log)
    basename = log.stem
    plot_name = "{}.pdf".format(basename)
    log_plot_name = "{}-log.pdf".format(basename)
    subprocess.run(["./rtm-graphs.py", str(log), plot_name])
    subprocess.run(["./rtm-graphs.py", str(log), log_plot_name, "log"])
