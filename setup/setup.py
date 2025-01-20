import json
import os, sys
import subprocess
import ctypes
from pathlib import Path

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(path)
base_dir = Path(__file__).parent.absolute()
create_data_path = os.path.join(base_dir, 'setup', 'create_data.py')
class AdminStateUnknownError(Exception):
    pass

if os.path.exists(f'{path}/settings.example.json') and not os.path.exists(f'{path}/settings.json'):
    os.rename(f'{path}/settings.example.json', f'{path}/settings.json')

def read_settings():
    with open(f'{path}/settings.json', 'r') as f:
        data = json.load(f)
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

def create_venv():
    venv_path = os.path.join(path, 'venv')
    python_executable = 'python'
    
    try:
        subprocess.run([python_executable, '-m', 'venv', str(venv_path)], check=True)
        print('Venv created successfully')
        return True
    except subprocess.CalledProcessError:
        try:
            subprocess.run(['py', '-m', 'venv', str(venv_path)], check=True)
            print('Venv created successfully using py command')
            return True
        except subprocess.CalledProcessError:
            print('Failed to create venv with both python and py commands')
            return False

args = sys.argv
if '--no-setup' in args:
    print('Skipping setup...')
    exit()
if '--setup' in args:
    print('Running setup...')
    subprocess.run(['python', 'setup.py'])
    exit()

if not is_user_admin():
    if os.name == 'nt':
        subprocess.run(['powershell', '-Command', 'Start-Process', 'python', '-ArgumentList', './setup.py', '-Verb', 'RunAs'])

new_requirements = []
settings = read_settings()

class setup_ai:
    def __init__(self):
        self.requirements = new_requirements
        self.reqs = ['diffusers==0.31.0', 'accelerate==1.1.1', 'huggingface-hub==0.26.3', 'tokenizers==0.20.3', 'transformers==4.46.3', 'torch==2.5.1', 'torchaudio==2.5.1', 'torchvision==0.20.1', 'sentencepiece==0.2.0']
    
    def add_reqs(self):
        self.requirements += self.reqs
        requirements_path = base_dir / 'requirements.txt'
        with open(requirements_path, 'r+') as f:
            for line in f:
                new_requirements.append(line.strip())
        
        modules_path = base_dir.parent / 'modules.json'
        with open(modules_path, 'r+') as m:
            data = json.load(m)
            data['ai'] = True
            m.seek(0)
            json.dump(data, m, indent=4)
            m.truncate()

if settings.get("main").get("first_run") == True:
    print("First run detected. Running setup...")
    print(settings["main"].get("first_run"))
    venv_path = os.path.join(path, 'venv')
    if os.path.exists(venv_path):
        print('Venv already exists.')
    else:
        print('Creating venv...')
        create_venv()

    print('Creating data directory...')
    os.makedirs(path+'data', exist_ok=True)
    
    ai = input('Do you want AI features enabled? Not recommended for low end computers/servers. Must have NVIDIA GPU (y/N):').lower()
    if ai != 'y':
        ai = 'n'
    if ai == 'y':
        setup_ai().add_reqs()
        print('AI features enabled.')
    
    requirements_path = base_dir / 'requirements.txt'
    if requirements_path.exists():
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', str(requirements_path)])
    
    id = input('Enter your user ID: ')
    name = input('Enter your username: ')
    subprocess.run([sys.executable, os.path.join(base_dir, 'create_data.py'), id, name.lower()])
    print('Data files created.')
    print('Setup complete.')
    print('Starting bot...')
    print('Ensure to run >setup after the bot starts to configure the bot.')

subprocess.run([sys.executable, 'main.py'])
