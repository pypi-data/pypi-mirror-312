#!/usr/bin/env python

from setuptools import setup
import pathlib
import os

HERE = pathlib.Path(__file__).parent
long_description = (HERE / "README.md").read_text()

setup(
    name='vizu',
    version=os.getenv("VERSION_TAG", "v0.0.3").lstrip("v"),
    description='Visualization of data files',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Jesper Halkjær Jensen',
    author_email='mail@jeshj.com',
    url='https://github.com/gedemagt/vizer',
    packages=['vizer', 'vizer.assets'],
    entry_points={
        'console_scripts': [
            'vizu = vizer.main:run',
        ],
    },
    license="MIT",
    python_requires='>=3.6',
    install_requires=[
        "flask>=3.0.0",
        "pandas>=2.0.0",
        "scipy>=1.14.0",
        "dash>=2.15.0",
        "dash-extensions>=1.0.0",
        "dash-bootstrap-components==1.6.0",
        "dash-table==5.0.0",
        "watchdog>=5.0.0"
    ]
)
