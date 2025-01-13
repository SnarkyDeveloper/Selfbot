import json
import os, sys
import subprocess
import ctypes
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
class AdminStateUnknownError(Exception):
    pass
if os.path.exists(f'{path}/settings.example.json') and not os.path.exists(f'{path}/settings.json'):
    os.rename(f'{path}/settings.example.json', f'{path}/settings.json')
def read_settings():
    with open(f'{path}/settings.json', 'r') as f:
        data = json.load(f)
        f.close()
        return data

def is_user_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        pass
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() == 1
    except AttributeError:
        raise AdminStateUnknownError

args = sys.argv
if '--no-setup' in args:
    print('Skipping setup...')
    exit()
if '--setup' in args:
    print('Running setup...')
    subprocess.run(['python3', 'setup.py'])
    exit()
if not is_user_admin():
    if os.name == 'nt':
        os.system('powershell', '-Command', 'Start-Process python -ArgumentList \'./setup.py\' -Verb RunAs')
new_requirements = []
settings = read_settings()

class setup_ai:
    def __init__(self):
        self.requirements = new_requirements
        self.reqs = ['diffusers==0.31.0', 'accelerate==1.1.1', 'huggingface-hub==0.26.3', 'tokenizers==0.20.3', 'transformers==4.46.3', 'torch==2.5.1', 'torchaudio==2.5.1', 'torchvision==0.20.1', 'sentencepiece==0.2.0']
    def add_reqs(self):
        self.requirements += self.reqs
        with open('./requirements.txt', 'r+') as f:
            for line in f:
                new_requirements.append(line.strip())
        with open('../modules.json', 'r+') as m:
            data = json.load(m)
            data['ai'] = True
            m.seek(0)
            json.dump(data, m, indent=4)
            m.truncate()

if settings.get("main").get("first_run") == True:
    print("First run detected. Running setup...")
    if os.path.exists(f'{path}/venv'):
        print('Venv already exists.')
    else:
        print('Creating venv...')
        try:
            subprocess.run(['python3', '-m', 'venv', 'venv'])
            print('Venv created.')
        except Exception as e: 
            print(f'Error creating venv: {e}')
    print('Creating data directory...')
    
    ai = input('Do you want AI features enabled? Not recommended for low end computers/servers. Must have NVIDIA GPU (y/N):').lower()
    if ai != 'y':
        ai = 'n'
    if ai == 'y':
        setup_ai().add_reqs()
        print('AI features enabled.')
    subprocess.run(['pip3', 'install', '-r', 'requirements.txt'])
    id = input('Enter your user ID: ')
    name = input('Enter your username: ')
    subprocess.run(['python', 'create_data.py', id, name.lower()])
    print('Data files created.')
    print('Setup complete.')
    print('Starting bot...')
    print('Ensure to run >setup after the bot starts to configure the bot.')
    
subprocess.run(['python', 'main.py'])
