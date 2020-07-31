#!/bin/bash
if [[ $(screen -ls | grep . -c) = 2 ]]; then
  echo "No screens running, booting..."
  sudo pigpiod
  echo "Started PIGPIOD"
  screen -d -m python3 ~/SpacePointer/updater/main.py
  echo "Started updater"
  screen -d -m sudo python3 ~/SpacePointer/website/run.py
  echo Started website
  screen -d -m python3 ~/SpacePointer/pointer/main.py
  echo "Started pointer"
  echo "Finished booting!"
else
  echo "Space Pointer already running!"
fi
