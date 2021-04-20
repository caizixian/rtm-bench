import subprocess
import socket
import time

def run_tests(tests):
    for test in tests:
        raw_args = test.split()
        args = []
        for token in raw_args:
            if token.isdigit():
                args[-1] = (args[-1][0], token)
            else:
                args.append((token, ""))

        encode_args = "_".join([arg[0][1:] + arg[1] for arg in args])

        log_name = "{}-{}-{}.log".format(socket.gethostname(), int(time.time()), encode_args)
        cmd = ["./rtm-bench"]
        cmd.extend(raw_args)
        print("{} > {}".format(" ".join(cmd), log_name))
        with open(log_name, "w") as fd:
            subprocess.run(cmd, stdout = fd)
