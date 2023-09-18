#!/usr/bin/env bash

ray start --head --port 32400 --include-dashboard False --block &
PID1=$!

ray start --head --port 32401 --include-dashboard False --block &
PID2=$!

trap "kill $PID1 $PID2" SIGINT

wait $PID1 $PID2
