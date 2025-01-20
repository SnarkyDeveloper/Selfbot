# Snarky's Selfbot

![Project LOC](https://tokei.rs/b1/github/SnarkyDeveloper/Selfbot) ![GitHub Repo stars](https://img.shields.io/github/stars/SnarkyDeveloper/Selfbot?style=flat)

This is my selfbot i made as a side project, it is probably going to stay maintained for a while.

## FAQ

#### Can my discord account be ban for this?

Yes, automating user accounts is against discord TOS, a normal bot rewrite is soon

#### Where can I contact you?

@SnarkyDev on discord


<details close>
<summary><h3>Features</h3></summary>
<!--All you need is a blank line-->

- [✅] Music Bot
  
   * Play
   * Pause
   * Resume
   * Stop
   * Loop
   * Queue

- [✅] Moderation

  * Kick
  * Ban
  
- [✅] Fun Commands
  * Reactions | Kiss, Hug, Slap, Bite, Tickle
  * Quote
  * Fake tweet
  * PetPet
  * Lyrics
 
- [✅] Utility
    * Avatar
    * AI Chat and Image Generation
    * Full permissions system
    * Message snipe
    * Bot Stats

- [✅] Economy
  * Balance
  * Work
  * Daily
  * Steal
  * Stripper
  * Mafia
  * Gambling
    * Roulette
    * Coinflip
    * Dice
- [✅] Misc
  * Reverse Image Searching [❌]
  * QOTD
  * Polls
  * Github info
- [❌] Spotify and music integration
  * Control Currently playing music
  * Get current song
</details>

## Coming Up

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

Rename settings.example.json to settings.json and add your desired settings

Start the bot

```bash
  # Either python main.py
  # or 
.\start.bat 
.\start.sh
```

### Setup

Use a server of your own or create one and run prefixsetup, (I. E. !setup) in the channel you want your webhook messages sent.

## Contributing

Contributions are always welcome!

Just open a pull request!

## Authors

- [@SnarkyDev](https://github.com/SnarkyDev)
- Looking for more! Please DM me on discord if you want to help!

## License

[MIT](https://choosealicense.com/licenses/mit/)
