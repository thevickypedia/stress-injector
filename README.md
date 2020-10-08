# stress_injector
Simple python script to inject stress using numpy and calculate the amount of memory consumed

Memory stress can be induced using so many ways. In this script I have used numpy random bytes which are sampled from uniform distribution.

Generating these random bytes induces a stress on the machine's memory usage. I have then used get resource usage for SELF to get the memory consumed by this particular script.