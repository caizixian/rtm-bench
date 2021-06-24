# rtm-bench
This repo contains the code used to produce the results reported in our [ISMM 2021 paper](https://doi.org/10.1145/3459898.3463901) "Understanding and Utilizing Hardware Transactional Memory Capacity". You can watch the talk on [YouTube](https://www.youtube.com/watch?v=IIETZja3ops).

We extended the [original work](https://github.com/perlfu/rtm-bench) by Carl Ritson.

## Build
Simply run `make`.

## Usage
To reproduce our results reported in the paper, run `./run_ismm21.py Baseline Reuse Invalidation Warmup WarmupIter`.
To enable huge page support, run `./run_ismm21.py HugeTLB Baseline Reuse Invalidation Warmup WarmupIter`.

You can select which tests to run by only passing certain configuration names to `run_ismm21.py`.

## Requirements
### Huge page support
Add `hugepagesz=1G hugepages=<n>` to your kernel's command-line parameters, where `<n>` is a number that is big enough to meet the benchmarks allocation requirement.
The amount of memory to be allocated is printed at the beginning of the benchmark.

### Invalidation
Install kernel module [`wbinvd`](https://github.com/caizixian/wbinvd) and make sure that `/proc/wbinvd` is readable by the user running the benchmark.

## Notes
The some of the parameters are machine dependent. For example, the warmup iteration used for our Haswell machine is 128.
The `run_ismm21.py` will choose the right parameters for each machine by reading the CPU model names from `/proc/cpuinfo`.
If you use a different CPU than what we evaluated, you are very welcome to use this tool.
You will first need to run experiments to figure out the correct parameters for your particular machine, and then change the `run_ismm21.py` script accordingly.

For technical questions directly related to the code, please contact Zixian Cai directly.
