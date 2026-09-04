#!/usr/bin/env sh

# abort on errors
set -e

# build
rm build -rf
rm dist -rf
python3 -m build

# upload to test repository
twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# upload to real repository
twine upload dist/*
