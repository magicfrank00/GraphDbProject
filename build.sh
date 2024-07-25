#!/bin/bash

if [ ! -d "dataset" ]; then
    ./setup_neo.sh
fi

docker compose up --build
