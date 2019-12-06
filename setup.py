from setuptools import setup, find_packages

setup(
    name='rireki',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        rireki=rireki.main:cli
    ''',
)
