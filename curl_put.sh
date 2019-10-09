#!/bin/bash

SECRET=`cat secret.txt`

curl -d "{\"in\": 26.0, \"out\": 25.0, \"secret\": \"$SECRET\"}" -H "Content-Type: application/json" -X POST http://localhost:8080/update
