#!/usr/bin/env bash

pwd=$(PWD)
docker run -it -v $PWD:/tmp/virtuscale tensorflow/tensorflow:2.15.0

# then run
# apt-get update && apt-get install -y vim
