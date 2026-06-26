#!/bin/bash

echo "Starting CVBS camera preview..."
sleep 3

rpicam-hello \
  --fullscreen \
  --timeout 0 \
  --width 720 \
  --height 480