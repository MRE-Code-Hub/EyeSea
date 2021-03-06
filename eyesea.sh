#!/bin/bash

# kill any currently running instances
kill -9 $(ps aux | grep '[p]ython eyesea_server.py' | awk '{print $2}')
kill -9 $(ps aux | grep '[n]ode' | awk '{print $2}')

# run the eyesea server and client
EYESEA_ROOT=$HOME/EyeSea
CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh

cd $EYESEA_ROOT/server
conda activate eyesea-server
nohup python eyesea_server.py >/dev/null 2>$HOME/eyesea.server.log &

cd $EYESEA_ROOT/uclient
conda activate eyesea-client
nohup yarn start >/dev/null 2>$HOME/eyesea.client.log &


