#!/bin/bash

if [ -z "$SCD_DVP" ]; then
    export SCD_DVP=/var/lib/docker/volumes
fi
sudo chmod 777 $SCD_DVP
docker build . -t mqtt-to-db-adaptor
docker stack deploy -c stack.yml scd3
