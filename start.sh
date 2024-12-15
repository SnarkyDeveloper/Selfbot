#!/bin/bash
source ./venv/bin/activate
# Capture all arguments
args="$@"

# If no arguments are provided, set args to --no-args
if [ -z "$args" ]; then
    pip install -r requirements.txt -q -q -q --exists-action i
fi

# Install dependencies if --verbose is passed
if [ "$args" == "--verbose" ]; then
    pip install -r requirements.txt --exists-action i
fi

# If --no-pip is passed, skip installation
if [ "$args" == "--no-pip" ]; then
    echo "Skipping installation..."
fi

# Wait for 2 seconds
sleep 2
@echo on
# Check if 'llama3.2:latest' exists using ollama
if ollama list | grep -q "llama3.2:latest"; then
    # If found, activate the virtual environment and run the script
    ollama serve
    source ./venv/bin/activate
    python main.py
else
    # If not found, run ollama to get llama3.2 and then activate venv
    ollama pull llama3.2:latest 
    ollama serve
    source ./venv/bin/activate
    python main.py
fi