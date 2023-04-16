Release Notes
=============

0.3.6 (04/16/2023)
------------------
- Remove echo and use logging to print
- Move variables to object members in url
- Update badges and startup instructions
- Bump version

0.3.5 (04/15/2023)
------------------
- Remove retry logic and add more logs
- Run assert on condition basis
- Improve logging and log format
- Remove function call to trigger

0.3.4 (04/13/2023)
------------------
- Use `requests` module to support all `http` methods
- Release a stable version 0.4

0.3.3 (04/13/2023)
------------------
- Reconstruct `stress-injector` to support Linux
- Add URL stress testing using threadpool
- Use pyproject.toml to upload package to pypi
- Create a new module for custom print statements

0.3.2 (05/23/2022)
------------------
- Fix imports
- Update docs

0.3.1 (01/19/2022)
------------------
- Flush screen output before carriage return

0.3.0 (01/18/2022)
------------------
- Update README.md on CPU stress usage
- Remove prompt and use default values instead
- Make some methods to be private

0.2.9 (01/10/2022)
------------------
- Update name of the repo

0.2.8 (01/10/2022)
------------------
- Update broken links in docstrings
- Match version as per the number of commits

0.2.7 (01/10/2022)
------------------
- Upgrade packages in requirements.txt
- Update maintenance year to 2022
- Generate CHANGELOG in LIFO manner
- Update docs big time

0.2.6 (08/14/2021)
------------------
- Stop the thread that measures CPU usage during a manual interrupt
- Previously CPUStress measurement used to run until the current time reaches 3 seconds in addition to the user input.
- Since the measurement runs in a dedicated thread this, stopping stress never stopped the usage display.
- Now CPUStress measurement will stop when a manual interrupt is received using a stop_flag variable.
- Update docs and README.md internal link.

0.2.5 (08/11/2021)
------------------
- Bug fix
- Fix broken CPU stress because of global variable
- Wrap everything inside a class
- Add an option to pass the user input when the class is initialized
- Update dependencies, docs and readme
- Update variable names to right convention

0.2.4 (08/04/2021)
------------------
- Update README.md and docs

0.2.3 (08/04/2021)
------------------
- Mark methods as internal
- Update dependencies and readme

0.2.2 (08/04/2021)
------------------
- Roll back module name
- Update badges in README.md

0.2.1 (08/04/2021)
------------------
- Update docs
- Change module name
- Fix broken references
- Bump version

0.2.0 (08/04/2021)
------------------
- Onboard to pypi

0.1.9 (08/04/2021)
------------------
- auto upload to pypi when tagged a release version

0.1.8 (08/04/2021)
------------------
- auto gen docs

0.1.7 (07/18/2021)
------------------
- Add hyperlinks to docstrings

0.1.6 (07/18/2021)
------------------
- Onboard sphinx documentation generator
- Split `memory` and `CPU` stress into individual files
- Add LICENSE
- Update README.md

0.1.5 (07/18/2021)
------------------
- Onboard sphinx documentation generator
- Split `memory` and `CPU` stress into individual files
- Add LICENSE
- Update README.md

0.1.4 (07/17/2021)
------------------
- add LICENSE

0.1.3 (04/05/2021)
------------------
- show each core's max utilization and handle manual interrupts

0.1.2 (04/05/2021)
------------------
- update README.md

0.1.1 (02/20/2021)
------------------
- add CPU stress injector using multiprocessing and multithreading
- update README.md
- add requirements.txt
- update .gitignore

0.1.0 (10/19/2020)
------------------
- get user input for stress limit

0.0.9 (10/08/2020)
------------------
- add windows support for stress injector

0.0.8 (10/08/2020)
------------------
- use tqdm to add a progress bar

0.0.7 (10/07/2020)
------------------
- maintain coding standards

0.0.6 (10/07/2020)
------------------
- update README.md

0.0.5 (10/07/2020)
------------------
- convert to human readable format

0.0.4 (10/07/2020)
------------------
- get memory consumption in bytes

0.0.3 (10/07/2020)
------------------
- basic script to induce stress

0.0.2 (10/07/2020)
------------------
- initial commit

0.0.1 (10/07/2020)
------------------
- Initial commit
