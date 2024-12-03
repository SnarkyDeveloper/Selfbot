set args=%*
if "%args%"=="" (
    set args=--no-args
)

@echo off
if "%args%"=="--no-args" (
    python -m pip install -r requirements.txt -q -q -q --exists-action i
)
if "%args%"=="--verbose" (
    python -m pip install -r requirements.txt --exists-action i
)
start /min cmd /k "ollama serve"

timeout /t 2 /nobreak > nul

ollama list | findstr "llama3.2:latest" > nul
if %errorlevel% equ 0 (
    call .\venv\Scripts\activate.bat
    python main.py
) else (
    ollama run llama3.2
    call .\venv\Scripts\activate.bat
    python main.py
)