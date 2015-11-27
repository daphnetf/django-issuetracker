import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        errno = tox.cmdline(args=args)
        sys.exit(errno)

version = __import__('issuetracker').get_release()

with open("requirements.txt") as f:
    required = [l for l in f.read().splitlines() if not l.startswith("#")]

setup(
    name="issuetracker",
    version=version,
    author="",
    author_email="",
    description=(""),
    license="BSD",
    keywords="",
    url="",
    packages=find_packages(),
    install_requires=required,
    # long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD",
    ],
    zip_safe=False,
    tests_require=['tox'],
    cmdclass={'test': Tox},
)
