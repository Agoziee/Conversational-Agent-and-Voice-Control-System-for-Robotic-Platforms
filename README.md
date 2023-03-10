# Conversational-Agent-and-Voice-Control-System-for-Robotic-Platforms
Conversational AI project developed using speech recognition technology, NLP techniques and neural networks

The application is designed to run on most computer systems that have a microphone and a speaker.
It can also function offline and isn't reliant on an internet connection.

The application uses VOSK, an offline tool as the speech recognition engine
To start the application, run the application file by running command - 'python main.py'.


------Installation-------

dependencies
Install Vosk. Take note of the requirements. Check here >> https://alphacephei.com/vosk/install

Create an environment (e.g. venv)

mkdir myproject

$ cd myproject $ python3 -m venv venv Activate it Mac / Linux:

. venv/bin/activate Windows:

venv\Scripts\activate

Install PyTorch and dependencies For Installation of PyTorch see official website.

You also need nltk:

pip install nltk If you get an error during the first run, 
you also need to install nltk.tokenize.punkt: Run this once in your terminal:

$ python

>>>import nltk nltk.download('punkt') Usage Run

Download Vosk speech recognition model from vosk model - https://github.com/alphacep/vosk-api/releases/, 
rename as model and save in file path. 

$ python train.py This will dump 'processor.pth' file. And then run

$ python main.py. 

To Customize, Have a look at intents.json. You can customize it according to your own use case. 
Just define a new tag, possible patterns, and possible responses for the system. You have to re-run the training 
whenever this file is modified.

{ "intents": [ { "tag": "greeting", "patterns": [ "Hi", "Hey", "How are you", "Is anyone there?", "Hello", "Good day" ], 
"responses": [ "Hey :-)", "Hello, thanks for visiting", "Hi there, what can I do for you?", "Hi there, how can I help?" ] }, ... 
] }

To implement skills, Have a look at skills.py
