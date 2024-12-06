#!/bin/bash

rm -rf build dist
./update-resources.sh
pyinstaller mxr-ui.spec
pyinstaller mxr.spec
