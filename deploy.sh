#!/bin/bash

cd game_server
./deploy.sh
cd ../game && ./deploy.sh
cd ..
