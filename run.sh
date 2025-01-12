#!/bin/bash

if [ -z "$SCD_DVP" ]; then
    export SCD_DVP=$PWD/volumes
fi
mkdir -p $SCD_DVP/influxdb $SCD_DVP/grafana
docker build . -t mqtt-to-db-adaptor
docker pull grafana/grafana:latest
docker pull influxdb:1.11.8
docker pull eclipse-mosquitto:2.0.20
docker stack deploy -c stack.yml scd3
