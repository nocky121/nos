#!/bin/bash
export SESSION_NAME=my_unique_session
mkdir -p /persistent
python monitor_telegram.py
