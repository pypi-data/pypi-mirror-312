#!/bin/bash
./build.sh
python -m pytest -s --benchmark-histogram test/
