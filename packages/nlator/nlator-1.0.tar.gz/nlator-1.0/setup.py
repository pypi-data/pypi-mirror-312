from setuptools import setup, find_packages
from pathlib import Path

here = Path(__file__).parent
long_description = (here / "README.md").read_text(encoding='utf-8')

setup(
    name='nlator',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'googletrans==4.0.0-rc1',
    ],
    description='A simple translator package for multiple languages.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='NihadKerimli',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)