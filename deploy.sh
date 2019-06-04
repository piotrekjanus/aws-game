#!/bin/bash

cd game-server && \
./deploy.sh && \
cd ../game && \
./deploy.sh && \
cd ..
