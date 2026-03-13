#!/bin/bash

export VERSION=2.0.36
export SCANS=/mnt/localscratch/lauracools/scans
export VERTEBRA=T4
export OUTPUT=/mnt/localscratch/lauracools/output

docker run --rm \
    -v "${SCANS}":/data/scans \
    -v "${OUTPUT}":/data/output \
    brecheisen/mosamatic2-cli:${VERSION} selectslicefromscans \
        --scans /data/scans --vertebra ${VERTEBRA} --output /data/output --overwrite true