# setup.py

from setuptools import setup, find_packages

setup(
    name='pypyterminal', 
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'click',  # For creating command-line interfaces
        'virtualenv',  # For managing virtual environments
        'jupyter',  # For running Jupyter notebooks
    ],
    author='Abdullah',
    author_email='abdullahashik2001@gmail.com',
    description='A library to automate and shorten terminal commands for Python development on Ubuntu',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)