targets = rtm-bench
cc = gcc -O2 -Wall
link = -lpthread -lrt
GIT_VERSION := "$(shell git describe --abbrev=8 --dirty --always --tags)"
# remove -lrt to compile on OS X

all: $(targets)

rtm-bench: rtm-bench.c rtm.h
	$(cc) rtm-bench.c -o rtm-bench -DGIT_VERSION=\"$(GIT_VERSION)\" $(link)

clean:
	rm -f rtm-bench

