#!/bin/bash

python log_tracker.py &
python ../lerobot/lerobot/scripts/control_docking_test8.py --config /home/nam/Lekiwi_ws/src/lerobot/lerobot/configs/lekiwi11.yaml &
wait
