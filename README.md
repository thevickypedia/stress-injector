# Stress Injector
Python script, to inject memory and CPU stress

## Runbook:

### Memory Stress:
* In this script, I have used `numpy.random.bytes` which are sampled from uniform distribution.
* Generating these random bytes induces a stress on the machine's memory usage.
* I have then used `getrusage` (get resource usage) for `SELF` to get the memory consumed only by the current script.
* The `size_converter` converts the bytes from resource usage to a human understandable format.

### CPU Stress:
* To achieve CPU stress, I have used multiprocess, looped for the # of logical cores, triggering an infinite loop on each core.
* The infinite loop will run for a given # of seconds provided by user.
* Mean-while the `cpu_percent` from `psutil` runs (dedicated thread) in an infinite loop with kill signal set to `False` calculating the current CPU utilization on each CPU core.
* Once the given # of seconds have passed, the `kill_signal` is set to `True` and some painful steps to _gracefully_ stop the `multiprocess` and multi-thread.

## License & copyright

&copy; Vignesh Sivanandha Rao

Licensed under the [MIT License](LICENSE)
