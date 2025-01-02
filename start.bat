set args=%*
timeout /t 2 /nobreak > nul

python ./setup/setup.py %args%