#!/bin/bash

SECRET=`cat ../secret.txt`

curl -d "{\"mq7_carb_mono\": 30, \"secret\": \"$SECRET\"}" -H "Content-Type: application/json" -X POST http://localhost:8080/update
