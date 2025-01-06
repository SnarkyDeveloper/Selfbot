import json
from Backend.utils import read_settings
import os, sys
import ctypes

class AdminStateUnknownError(Exception):
    pass

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
    os.system('python3 setup.py')
    exit()
if not is_user_admin():
    os.system('powershell -Command "Start-Process python -ArgumentList \'./setup.py\' -Verb RunAs"')
new_requirements = []
settings = read_settings()

class setup_ai:
    def __init__(self):
        self.requirements = new_requirements
        self.cuda = False
        self.reqs = ['diffusers==0.31.0', 'accelerate==1.1.1', 'huggingface-hub==0.26.3', 'ollama==0.4.2', 'tokenizers==0.20.3', 'transformers==4.46.3', 'torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118']
    def add_reqs(self):
        self.requirements += self.reqs
        with open('./requirements.txt', 'r+') as f:
            for line in f:
                new_requirements.append(line.strip())
        with open('../modules.json', 'r+') as m:
            data = json.load(m)
            data['ollama'] = True
            m.seek(0)
            json.dump(data, m, indent=4)
            m.truncate()

if settings.get("main").get("first_run") == "True":
    print("First run detected. Running setup...")
    
    print('Creating data directory...')
    
    ai = input('Do you want AI features enabled? Not recommended for low end computers/servers. Must have NVIDIA GPU (y/N):').lower()
    if ai != 'y':
        ai = 'n'
    if ai == 'y':
        setup_ai().add_reqs()
        print('AI features enabled.')
    os.system('pip3 install -r requirements.txt')
    id = input('Enter your user ID: ')
    name = input('Enter your username: ')
    os.system(f'python create_data.py {id} {name.lower()}')
    print('Data files created.')
    print('Setup complete.')
    print('Starting bot...')
    print('Ensure to run >setup after the bot starts to configure the bot.')
    
os.system('python main.py')