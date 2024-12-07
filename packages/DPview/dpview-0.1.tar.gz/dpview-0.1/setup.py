from setuptools import setup, find_packages

setup(
    name='DPview',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'selenium',  # or playwright, depending on the browser automation tool
        'requests',
        'beautifulsoup4',
    ],
    test_suite='tests',
    description='Advanced Python library for web browser automation and complex UI features',
    author='kkkppmm',
    
)

