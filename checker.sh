#!/bin/bash
for pid in $(pidof -x checker.sh); do
    if [ $pid != $$ ]; then
        exit 1
    fi 
done
python3 script.py