#!/usr/bin/env sh

# abort on errors
set -e

# build
python setup.py sdist bdist_wheel

# upload to test repository
twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# upload to real repository
twine upload dist/*
