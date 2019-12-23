#!/bin/bash

# for internal testing purposes only
export ENVIRONMENT="local"

pip3 install -r requirements.txt
python3 main.py
