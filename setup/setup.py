import json
from Backend.utils import read_settings
import os, sys
args = sys.argv
if args == ['--no-setup']:
    print('Skipping setup...')
    exit()
if args == ['--setup']:
    print('Running setup...')
    os.system('python3 setup.py')
    exit()
new_requirements = []
settings = read_settings()
with open ('./requirements.txt', 'r+') as f:
    for line in f:
        new_requirements.append(line.strip())
class setup_ai:
    def __init__(self):
        self.requirements = new_requirements
        self.cuda = False
        self.reqs = ['diffusers==0.31.0', 'accelerate==1.1.1', 'huggingface-hub==0.26.3', 'ollama==0.4.2', 'tokenizers==0.20.3', 'transformers==4.46.3', 'pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118']
    def add_reqs(self):
        self.requirements += self.reqs
        with open('../modules.json', 'r+') as m:
            data = json.load(f)
            data['ollama'] = True
            m.close()
if settings.get("main").get("first_run") == "True":
    print("First run detected. Running setup...")
    
    print('Creating data directory...')
    
    ai = input('Do you want AI features enabled? Not recommended for low end commputers/servers. Must have NVIDIA GPU (Y/n):').lower()
    if ai != 'n':
        ai = 'y'
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