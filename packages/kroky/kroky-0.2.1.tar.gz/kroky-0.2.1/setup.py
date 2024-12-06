# setup.py
import bs4
import requests
from setuptools import setup, find_packages

setup(
    name='kroky',                    # The name of your package
    version='0.2.1',                        # Package version
    packages=find_packages(),             # Automatically find your packages
    install_requires=[                    # Dependencies (if any)
        "bs4", "requests"
    ],
    test_suite='tests',                   # Specify where your tests are
    long_description=open('readme.md').read(),  # Long description from README
    long_description_content_type='text/markdown',  # Format of long description
    author='Jon Pecar',
    author_email='your-email@example.com',
    description='A short description of the package',
    url='https://github.com/Jonontop/kroky-library',  # URL for your project (optional)
    classifiers=[                          # PyPI classifiers
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
