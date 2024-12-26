
# Snarky's Selfbot

![Project LOC](https://tokei.rs/b1/github/SnarkyDeveloper/Selfbot) ![GitHub Repo stars](https://img.shields.io/github/stars/SnarkyDeveloper/Selfbot?style=flat)

This is my selfbot i made as a side project, it is probably going to stay maintained for a while.

## FAQ

#### Can my discord account be ban for this?

Yes, automating user accounts is against discord TOS, a normal bot rewrite is soon

#### Where can I contact you?

@SnarkyDev on discord

## Features

- Reverse image searching (Broken, fixing)
- Music Bot
- Message Sniping
- Moderation
- Economy
- AI features (Image Generation & Text Generation)
- Fun commands!
  
# Coming Up

- Spotify Integration for playback controls (Will require seperate flask server)

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`token=your_token` (This exact format)

## Run Locally

Clone the project

```bash
  git clone https://github.com/SnarkyDeveloper/Selfbot
```

Go to the project directory

```bash
  cd Selfbot
```

Create your venv

```python
    python -m venv venv
    #(Ensure its called venv or start script won't work)
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Configure your settings

```text
    Just add your desired settings in settings.json
```

Start the bot

```bash
  Either python main.py
  or 
  .\start.bat 
  .\start.sh
```

## Contributing

Contributions are always welcome!

Just open a pull request!

## Authors

- [@SnarkyDev](https://github.com/SnarkyDev)
- Looking for more! Please DM me on discord if you want to help!

## License

[MIT](https://choosealicense.com/licenses/mit/)
