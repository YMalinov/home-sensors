#!/bin/bash

SECRET=`cat ../secret.txt`

curl -d "{\"ds18_short_temp\": 25.0, \"bme_temp\": 21.00, \"bme_pressure\": 945.85, \"bme_humidity\": 53.0, \"secret\": \"$SECRET\"}" -H "Content-Type: application/json" -X POST http://localhost:8080/update
