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

call .\venv\Scripts\activate.bat
python main.py