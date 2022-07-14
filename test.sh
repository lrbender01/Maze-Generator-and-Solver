#!/usr/bin/bash

for i in *.png; do
    echo $i
    time python3 ./mazesolve.py $i
    echo
done