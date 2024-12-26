import os
import json
path = os.path.dirname(os.path.abspath(__file__))
if json.load(open(f'{path}/settings.json')).get('main').get('first_run') == 'True':
    def create_users():
        try:
            os.makedirs(f'{path}/data/users', exist_ok=True)
            with open(f'{path}/data/users/users.json', 'w') as f:
                data = {
                    "users": [
                        {
                            "id": '',
                            "name": ''
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
            input('Users file created. Enter your id and username in name#0 (all lowercase) fomrat and press enter to continue.')
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
    def change_run():
        try:
            with open(f'{path}/settings.json', 'w') as f:
                data = json.loads(f)
                data.get('main').get('first_run') = "False"
                json.dump(data, f, indent=4)
                f.close()
        except Exception as e:
            print(f'Error creating run file: {e}')
    if __name__ == '__main__':
        try:
            create_punishments()
            create_messages()
            create_economy()
            create_users()
            print('Data files created.')
        except Exception as e:
            print(f'Error creating data files: {e}')
else:
    print('Skipping data creation. Files already exist. Change first_run to True in settings.json to recreate data files.')