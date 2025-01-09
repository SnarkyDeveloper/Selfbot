set args=%*
if "%args%"=="" (
    set args=--no-args
)

@echo off
if "%args%"=="--no-args" (
    call .\venv\Scripts\activate.bat
    python "./setup/setup.py"
)
if "%args%"=="--no-pip" (
    echo skipping...
)
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