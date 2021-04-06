#!/bin/bash
# Just in case some odd exception occurs, this script is used to continually
# restart the batch programming script upon failure

while [[ "1" ]]
do
    python3 BatchPather.py
done
