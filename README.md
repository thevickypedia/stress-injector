[![Pypi-version](https://img.shields.io/pypi/v/stress-injector)](https://pypi.org/project/stress-injector)
[![Pypi-py-version](https://img.shields.io/pypi/pyversions/stress-injector)](https://pypi.org/project/stress-injector)

![docs](https://github.com/thevickypedia/stress_injector/actions/workflows/docs.yml/badge.svg)
![pypi](https://github.com/thevickypedia/stress_injector/actions/workflows/python-publish.yml/badge.svg)

[![Pypi-format](https://img.shields.io/pypi/format/stress-injector)](https://pypi.org/project/stress-injector/#files)
[![Pypi-status](https://img.shields.io/pypi/status/stress-injector)](https://pypi.org/project/stress-injector)

![Maintained](https://img.shields.io/maintenance/yes/2021)
[![GitHub Repo created](https://img.shields.io/date/1599432310)](https://api.github.com/repos/thevickypedia/stress_injector)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/y/thevickypedia/stress_injector)](https://api.github.com/repos/thevickypedia/stress-injector)
[![GitHub last commit](https://img.shields.io/github/last-commit/thevickypedia/stress_injector)](https://api.github.com/repos/thevickypedia/stress-injector)

# Stress Injector
Python module, to inject memory and CPU stress

## Insights:

### CPU Stress:
* To achieve CPU stress, I have used multiprocess, looped for the # of logical cores, triggering an infinite loop on
  each core.
* The infinite loop will run for a given # of seconds provided by user.
* Mean-while the `cpu_percent` from `psutil` runs (dedicated thread) in an infinite loop with kill signal set to `False`
  calculating the current CPU utilization on each CPU core.
* Once the given # of seconds have passed, the `kill_signal` is set to `True` and some painful steps to _gracefully_
  stop the `multiprocess` and multi-thread.

### Memory Stress:
* In this script, I have used `numpy.random.bytes` which are sampled from uniform distribution.
* Generating these random bytes induces a stress on the machine's memory usage.
* I have then used `getrusage` (get resource usage) for `SELF` to get the memory consumed only by the current script.
* The `size_converter` converts the bytes from resource usage to a human understandable format.



## Pypi Module
https://pypi.org/project/gmail-connector/

### Usage
`pip install stress-injector`

<br>

[CPU Stress](https://github.com/thevickypedia/stress_injector/blob/main/stressinjector/cpu.py)
```python
from stressinjector.cpu import cpu_stress

cpu_stress()
```

[Memory Stress](https://github.com/thevickypedia/stress_injector/blob/main/stressinjector/memory.py)
```python
from stressinjector.memory import memory_stress

memory_stress()
```

### Coding Standards:
Docstring format: [`Google`](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) <br>
Styling conventions: [`PEP 8`](https://www.python.org/dev/peps/pep-0008/) <br>
Clean code with pre-commit hooks: [`flake8`](https://flake8.pycqa.org/en/latest/) and 
[`isort`](https://pycqa.github.io/isort/)

### Pre-Commit
`pre-commit` will run `flake8` and `isort` to ensure proper coding standards along with [docs_generator](gen_docs.sh) 
to update the [runbook](#Runbook)
> `pre-commit run --all-files`

### Runbook:
https://thevickypedia.github.io/stress_injector/

> Generated using [`sphinx-autogen`](https://www.sphinx-doc.org/en/master/man/sphinx-autogen.html)

## License & copyright

&copy; Vignesh Sivanandha Rao

Licensed under the [MIT License](LICENSE)
