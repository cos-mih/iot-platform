#!/bin/bash

echo $SCD_DVP
echo $DEBUG_DATA_FLOW
chmod 777 $SCD_DVP
docker build . -t mqtt-to-db-adaptor
docker stack deploy -c stack.yml scd3
