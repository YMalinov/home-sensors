#!/bin/bash

# for internal testing purposes only
export ENVIRONMENT="local"

pip install -r requirements.txt
python3 main.py
