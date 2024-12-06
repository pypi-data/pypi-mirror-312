# setup.py
from setuptools import setup, find_packages

setup(
    name='cost_estimation_analyser',
    version='0.1.1',
    description='It is a reusable estimated cost analyser library for insurance claim estimation analyser tool',
    author='Deepak',
    license='MIT',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
