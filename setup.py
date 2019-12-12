from setuptools import setup

setup(
    name='rireki',
    version='0.0.1',
    packages=['rireki'],
    install_requires=['click', 'toml'],
    entry_points={
        'console_scripts': ['rireki = rireki.cli:cli'],
    },
)
