from setuptools import setup, find_packages

setup(
    name='pythonPrintAnimals',
    version='1.0.2',
    packages=find_packages(),
    install_requires=[
        'plotly',
    ],
    author='Uarlley Amorim',
    description='A simple python library that prints animals',
)