from setuptools import setup

setup(
    name='rireki',
    version='0.0.2',
    author='Noel De Martin',
    author_email='noeldemartin@gmail.com',
    description='CLI backup tool.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/noeldemartin/rireki',
    license='MIT',
    packages=[
        'rireki',
        'rireki.commands',
        'rireki.core',
        'rireki.drivers',
        'rireki.stores',
        'rireki.utils',
    ],
    install_requires=['click', 'toml', 'boto3'],
    entry_points={
        'console_scripts': ['rireki = rireki.cli:cli'],
    },
)
