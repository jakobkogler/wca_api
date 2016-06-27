from setuptools import setup

setup(
    name='wca_api',
    version='0.1dev',
    setup_requires=['pytest-runner', ],
    tests_require=['pytest', ],
    packages=['wca_api', ],
    license='MIT License',
    author='Jakob Kogler',
    description='API for the WCA database',
    classifiers=['Programming Language :: Python :: 3', ],
)
