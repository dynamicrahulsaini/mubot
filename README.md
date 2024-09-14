# mubot

## commands

- generic commands
    - `!ping` - test if the bot is responding

- music commands
    - `!join` - join the voice channel
    - `!play <url>` - play the audio from the given YouTube URL
    - `!leave` - leave the voice channel

## todo

- `!pause` - pause the audio
- `!resume` - resume the audio
- `!stop` - stop the audio
- `!skip` - skip the current audio
- `!queue` - show the current queue

## development

create a virtual environment and install the dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

create a `.env` file with the following variables or add the variables to your environment:

```bash
DISCORD_TOKEN=<discord bot token>
DISCORD_APP_ID=<discord app id>
DISCORD_PUBLIC_KEY=<discord public key>
```

run the bot:

```bash
python main.py
```