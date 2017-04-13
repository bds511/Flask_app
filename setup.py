from setuptools import setup, find_packages

setup(
    name='Board_App',
    version='1.0',
    long_description=__doc__,
    packages=['Board_App'],
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask'],
    setup_requires=['pytest-runner',],
    tests_require=['pytest',],
)