import os
import json
import sys
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args = sys.argv
if sys.argv:
    id = args[1]
    name = args[2]
def get_run():
    with open(f'{path}/settings.json', 'r') as f:
        data = json.load(f)
        f.close()
    return data.get('main').get('first_run')
if get_run() == True:
    def create_users():
        try:
            os.makedirs(f'{path}/data/users', exist_ok=True)
            with open(f'{path}/data/users/users.json', 'w') as f:
                data = {
                    "users": [
                        {
                            "id": id,
                            "name": f'{name}#0',
                        }
                    ]
                }
                json.dump(data, f, indent=4)
                f.close()
            with open(f'{path}/data/users/afk.json', 'w') as f:
                f.write('{}')
                f.close()
        except Exception as e:
            print(f'Error creating users file: {e}')
        finally:
            input('Users file created. Hit enter to continue...')
    def create_punishments():
        try:
            os.makedirs(f'{path}/data/punishments', exist_ok=True)
            with open(f'{path}/data/punishments/punishments.json', 'w') as f:
                data = {
                    "punishments": [
                        
                    ]
                }
                json.dump(data, f, indent=4)
                f.close()
        except Exception as e:
            print(f'Error creating punishments file: {e}')

    def create_messages():
        try:
            os.makedirs(f'{path}/data/messages', exist_ok=True)
            with open(f'{path}/data/messages/messages.json', 'w') as f:
                data = {
                    "messages": [

                    ]
                }
                json.dump(data, f, indent=4)
                f.close()
        except Exception as e:
            print(f'Error creating messages file: {e}')
    def create_economy():
        try:
            os.makedirs(f'{path}/data/economy', exist_ok=True)
            with open(f'{path}/data/economy/eco.json', 'w') as f:
                data = {
                    "users": [
                    ]
                }
                json.dump(data, f, indent=4)
                f.close()
        except Exception as e:
            print(f'Error creating economy file: {e}')
    def create_webhook():
        try:
            with open(f'{path}/data/webhook.json', 'w') as f:
                data = {
                    "webhook_url": ""
                }
                json.dump(data, f, indent=4)
                f.close()
        except Exception as e:
            print(f'Error creating webhook file: {e}')
    def change_run():
        try:
            with open(f'{path}/settings.json', 'r') as f:
                data = json.load(f)
            data['main']['first_run'] = False
            with open(f'{path}/settings.json', 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f'Error creating run file: {e}')    
if __name__ == '__main__' and get_run() == True:
        try:
            create_punishments()
            create_messages()
            create_economy()
            create_webhook()
            change_run()
            create_users()
            print('Data files created.')
        except Exception as e:
            print(f'Error creating data files: {e}')
else:
    print('Skipping data creation. Files already exist. Change first_run to true in settings.json to recreate data files.')