#!/bin/bash

export SCD_DVP=/mnt/c/Users/cosmi/Desktop/FACULTATE/AN4/SCD/tema3/volumes
chmod 777 $SCD_DVP
docker stack deploy -c stack.yml scd3
