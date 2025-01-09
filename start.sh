#!/bin/bash
source ./venv/bin/activate
ARGS=$@
if [ -z "$ARGS" ]
then
    ARGS="--no-args"
fi

if [ "$ARGS" == "--no-args" ]
then
    source ./venv/bin/activate
    python ./setup/setup.py
fi

if [ "$ARGS" == "--no-pip" ]
then
    echo "skipping..."
fi

sleep 2

if ollama list | grep -q "llama3.2:latest"
then
    source ./venv/bin/activate
    python main.py
else
    ollama run llama3.2
    source ./venv/bin/activate
    python main.py
fi

# Obama
# - Typera, 2024