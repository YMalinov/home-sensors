#!/bin/bash

SECRET=`cat ../secret.txt`

curl -d "{\"ds18_long_temp\": 22.0, \"secret\": \"$SECRET\"}" -H "Content-Type: application/json" -X POST http://localhost:8080/update
