#!/bin/sh

cd $(realpath $(dirname $0))

python3.7 ./app.py || exit $?
