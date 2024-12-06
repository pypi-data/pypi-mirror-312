from setuptools import setup, find_packages

setup(
    name='nlator',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'googletrans==4.0.0-rc1',
    ],
    description='A simple translator package for multiple languages.',
    author='NihadKerimli',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)