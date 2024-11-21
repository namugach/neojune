#!/bin/bash

mkdir -p /root/app

cd /root/work/src/install/dev/setup

./airflow_init.sh
./prometheus/install.sh
./grafana/install.sh