#!/bin/bash

docker run -it -v /Users/kwonl/projects/skt/meetus-audio:/data jonashaag/visqol:v3 \
  --degraded_file /data/padding.wav \
  --reference_file /data/havard.wav \
  --verbose
