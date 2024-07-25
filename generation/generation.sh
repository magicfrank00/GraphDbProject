#!/bin/bash

cp ./ingest.sh ./dataset_ingest/ingest.sh 
python3 ./generate_dataset.py

python3 ./ingest_pre.py
python3 ./ingest_pg.py


