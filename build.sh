#!/bin/sh

# build and upload
# PACKAGE_DIR=ApplyLlm
PACKAGE_DIR=src
REPO_NAME=gitlab-lrz
pushd ${PACKAGE_DIR};
python3 -m build;
python3 -m twine upload --verbose --repository ${REPO_NAME} dist/*
popd;


