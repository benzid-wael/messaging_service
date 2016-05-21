#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


class MessagingServiceTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


requirements = [
    'pika==0.9.14',
    'gevent==1.0.1',
]

test_requirements = [
    'freezegun==0.3.1',
    'pytest==2.7.0',
]

setup(
    name='messaging_service',
    author='Wael BEN ZID',
    packages=[
        'service',
    ],
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    test_suite='tests',
    scripts=['bin/messaging-service'],
    tests_require=test_requirements,
    cmdclass={'test': MessagingServiceTest},
)
