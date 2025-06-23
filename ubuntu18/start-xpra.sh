#!/bin/bash

xpra start-desktop :100 \
  --bind-tcp=0.0.0.0:14500 \
  --html=on \
  --start-child="mate-session" \
  --resize-display=yes \
  --desktop-scaling=1920x1080 \
  --exit-with-children \
  --clipboard=yes \
  --notifications=no \
  --compress=9 \
  --bell=no \
  --quality=50 \
  --speed=50 \
  --encoding=jpeg \
  --daemon=no