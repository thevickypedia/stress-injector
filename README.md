[![Pypi-version](https://img.shields.io/pypi/v/stress-injector)](https://pypi.org/project/stress-injector)
[![Pypi-py-version](https://img.shields.io/pypi/pyversions/stress-injector)](https://pypi.org/project/stress-injector)

![docs](https://github.com/thevickypedia/stress-injector/actions/workflows/docs.yml/badge.svg)
![pypi](https://github.com/thevickypedia/stress-injector/actions/workflows/python-publish.yml/badge.svg)

[![Pypi-format](https://img.shields.io/pypi/format/stress-injector)](https://pypi.org/project/stress-injector/#files)
[![Pypi-status](https://img.shields.io/pypi/status/stress-injector)](https://pypi.org/project/stress-injector)

![Maintained](https://img.shields.io/maintenance/yes/2023)
[![GitHub Repo created](https://img.shields.io/date/1599432310)](https://api.github.com/repos/thevickypedia/stress-injector)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/y/thevickypedia/stress-injector)](https://api.github.com/repos/thevickypedia/stress-injector)
[![GitHub last commit](https://img.shields.io/github/last-commit/thevickypedia/stress-injector)](https://api.github.com/repos/thevickypedia/stress-injector)

# Stress Injector
Python module, to inject memory and CPU stress

<details>
<summary><strong>Insights about <a href="https://github.com/thevickypedia/stress-injector/blob/main/stressinjector/cpu.py">CPU Stress</a></strong></summary>

* To achieve CPU stress, I have used multiprocess, looped for the number of logical cores, triggering an infinite loop on
  each core.
* The infinite loop will run for a given number of seconds provided by user.
* Mean-while the `cpu_percent` from `psutil` runs (dedicated thread) in an infinite loop calculating the current CPU 
  utilization on each CPU core.
* The dedicated thread runs for 3 seconds in addition to the number of seconds provided by the user.
* Once the given number of seconds have passed, the `multiprocess` and `thread` that was initiated to monitor CPU usage are stopped.
</details>
<br>
<details>
<summary><strong>Insights about <a href="https://github.com/thevickypedia/stress-injector/blob/main/stressinjector/memory.py">Memory Stress</a></strong></summary>

* In this script, I have used `numpy.random.bytes` which are sampled from uniform distribution.
* Generating these random bytes induces a stress on the machine's memory usage.
* I have then used `getrusage` (get resource usage) for `SELF` to get the memory consumed only by the current script.
* The `size_converter` converts the bytes from resource usage to a human understandable format.
</details>
<br>
<details>
<summary><strong>Insights about <a href="https://github.com/thevickypedia/stress-injector/blob/main/stressinjector/onus.py">URL Stress</a></strong></summary>

* In this script, I have used threadpools to make concurrent requests.
* The script uses `requests` module to make calls.
* Takes arguments
  * **rate**: Number of calls to make. _Defaults to 100K_
  * **timeout**: Timeout for each request. _Defaults to 0.5_
  * **retry_limit**: Retry limit if the system is unable to spinup more threads. _Defaults to 5_
  * **circuit_break**: Wait time in seconds between retries. _Defaults to 5_
  * **request_type**: Function from `requests` module.

</details>

### Usage
`pip install stress-injector`

[CPU Stress](https://github.com/thevickypedia/stress-injector/blob/main/stressinjector/cpu.py)
```python
import stressinjector as injector


if __name__ == '__main__':
    injector.CPUStress(seconds=300)
```

[Memory Stress](https://github.com/thevickypedia/stress-injector/blob/main/stressinjector/memory.py)
```python
import stressinjector as injector


if __name__ == '__main__':
    injector.MemoryStress(gigabytes=2_000).run()
```

[URL Stress](https://github.com/thevickypedia/stress-injector/blob/main/stressinjector/url.py)
```python
import os
import stressinjector as injector


if __name__ == '__main__':
    injector.URLStress(url='http://0.0.0.0:5002/')  # Stress test GET calls

    # Stress test POST calls, also supports PUT, and DELETE
    sample_data = {'headers': {'Authorization': 'Bearer %s' % os.environ.get('TOKEN')}}
    injector.URLStress(
      url='http://0.0.0.0:5002/',
      request_type=injector.RequestType.post,
      **sample_data
    )
```

#### Coding Standards
Docstring format: [`Google`](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) <br>
Styling conventions: [`PEP 8`](https://www.python.org/dev/peps/pep-0008/) <br>
Clean code with pre-commit hooks: [`flake8`](https://flake8.pycqa.org/en/latest/) and 
[`isort`](https://pycqa.github.io/isort/)

#### [Release Notes](https://github.com/thevickypedia/stress-injector/blob/main/release_notes.rst)
**Requirement**
```shell
python -m pip install changelog-generator
```

**Usage**
```shell
changelog reverse -f release_notes.rst -t 'Release Notes'
```

#### Linting
`PreCommit` will ensure linting, and the doc creation are run on every commit.

**Requirement**
<br>
```bash
pip install --no-cache sphinx==5.1.1 pre-commit recommonmark
```

**Usage**
<br>
```bash
pre-commit run --all-files
```

### Pypi Package
[![pypi-module](https://img.shields.io/badge/Software%20Repository-pypi-1f425f.svg)](https://packaging.python.org/tutorials/packaging-projects/)

[https://pypi.org/project/stress-injector/](https://pypi.org/project/stress-injector/)

### Runbook
[![made-with-sphinx-doc](https://img.shields.io/badge/Code%20Docs-Sphinx-1f425f.svg)](https://www.sphinx-doc.org/en/master/man/sphinx-autogen.html)

[https://thevickypedia.github.io/stress-injector/](https://thevickypedia.github.io/stress-injector/)

## License & copyright

&copy; Vignesh Sivanandha Rao

Licensed under the [MIT License](https://github.com/thevickypedia/stress-injector/blob/main/LICENSE)
