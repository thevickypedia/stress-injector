from os import path

from setuptools import setup

from version import version_info

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Telecommunications Industry',
    'Operating System :: MacOS :: MacOS X',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.9',
    'Topic :: Communications :: Email :: Post-Office :: IMAP'
]


def read(name):
    """https://pythonhosted.org/an_example_pypi_project/setuptools.html#setting-up-setup-py - reference."""
    return open(path.join(path.dirname(__file__), name)).read()


setup(
    name='stress-injector',
    version='.'.join(str(c) for c in version_info),
    description='Python module, to inject memory and CPU stress.',
    long_description=read('README.md') + '\n\n' + read('CHANGELOG'),
    url='https://github.com/thevickypedia/stress_injector',
    author='Vignesh Sivanandha Rao',
    author_email='svignesh1793@gmail.com',
    License='MIT',
    classifiers=classifiers,
    keywords='stress-test, numpy-arrays, cpu-stress, memory-stress, multiprocessing',
    packages=['.stress-injector'],
    install_requires=['']
)
