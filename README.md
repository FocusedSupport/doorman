# doorman
Why hire a doorman when you can build one?

[![PyPI version](https://badge.fury.io/py/thedoorman.svg)](https://badge.fury.io/py/thedoorman)

## How to Install
```
pip install thedoorman
```

## Configuration
Edit `slackbot_settings.py`:

1. Update `team_name` as appropriate
2. Update `bot_name` as appropriate
3. Either uncomment and include your bot's API token or identify it in your environment via the variable `SLACKBOT_API_TOKEN`
4. Set the environment variable DOORBELL_SOUND to the path to a mp3 file to be played when the doorbell rings.
5. Set the environment variable $SPEECH_SCRIPT to a script which does text to speech.   Several examples are in the misc directory.  

## To Run
`python run.py`

## To Run on boot

1. Edit start-doorman.sh, setting the python3 interpreter and install directory if necessary, and setting any environment variables needed.
2. Edit doorman.service, adjusting the paths as necessary.
3. Install doorman.service:
    % sudo cp doorman.service /lib/systemd/system/
    % sudo chmod 644 /lib/systemd/system/doorman.service
    % sudo systemctl daemon-reload
    % sudo systemctl enable doorman
4. Reboot


