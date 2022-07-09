#!/usr/bin/bash

for i in *.png; do
    echo $i
    python3 ./mazesolve.py $i
    echo
done