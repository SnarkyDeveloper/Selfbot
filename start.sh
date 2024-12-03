source ./venv/bin/activate

# Start ollama in background and redirect output to temp file
ollama serve > /tmp/ollama.log 2>&1 &

# Wait a moment for ollama to start
sleep 2

# Check if model exists and start python script
if ollama list | grep -q "llama3.2:latest"; then
    python main.py
else
    ollama pull llama:3.2s
    python main.py
fi