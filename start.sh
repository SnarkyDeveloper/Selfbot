#!/bin/bash
source ./venv/bin/activate
args="$@"

if [ -z "$args" ]; then
    pip install -r requirements.txt -q -q -q --exists-action i
fi

if [ "$args" == "--verbose" ]; then
    pip install -r requirements.txt --exists-action i
fi

if [ "$args" == "--no-pip" ]; then
    echo "Skipping installation..."
fi

sleep 2
@echo on
if ollama list | grep -q "llama3.2:latest"; then
    source ./venv/bin/activate
    nohup ollama serve > /dev/null & python main.py 
else
    ollama pull llama3.2:latest 
    source ./venv/bin/activate
    nohup ollama serve > /dev/null & python main.py
fi