#!/usr/bin/env python3

import argparse
import os
import queue
import sounddevice as sd
import vosk
import sys
import json

import random
import json
import torch
from speak import say
from skills import NonInputExecution

from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

device = torch.device('cuda'if torch.cuda.is_available() else 'cpu')

q = queue.Queue()

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    '-f', '--filename', type=str, metavar='FILENAME',
    help='audio file to store recording to')
parser.add_argument(
    '-m', '--model', type=str, metavar='MODEL_PATH',
    help='Path to the model')
parser.add_argument(
    '-d', '--device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-r', '--samplerate', type=int, help='sampling rate')
args = parser.parse_args(remaining)

try:
    if args.model is None:
        args.model = "model"
    if not os.path.exists(args.model):
        print ("Please download a model for your language from https://alphacephei.com/vosk/models")
        print ("and unpack as 'model' in the current folder.")
        parser.exit(0)
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        # soundfile expects an int, sounddevice provides a float:
        args.samplerate = int(device_info['default_samplerate'])

    model_sr = vosk.Model(args.model)

    if args.filename:
        dump_fn = open(args.filename, "wb")
    else:
        dump_fn = None

    with open('intents.json', 'r') as json_data:
        intents = json.load(json_data)
    FILE = "processor.pth"
    data = torch.load(FILE)

    input_size = data["input_size"]
    hidden_size = data["hidden_size"]
    output_size = data["output_size"]
    all_words = data['all_words']
    tags = data['tags']
    model_state = data["model_state"]

    model_nlp = NeuralNet(input_size, hidden_size, output_size).to(device)
    model_nlp.load_state_dict(model_state)
    model_nlp.eval()

    with sd.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device, dtype='int16',
                            channels=1, callback=callback):
            print('#' * 80)
            print('Press Ctrl+C to stop the recording')
            print('#' * 80)

            bot_name = "Robot"
            print(f"Hey I'm {bot_name}, let's talk!")
            #say(f"Hey I'm {bot_name}, let's talk!")

            rec = vosk.KaldiRecognizer(model_sr, args.samplerate)
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    res = json.loads(rec.Result())
                    sentence = (res['text'])
                    result = str(sentence)
                    print(res['text'])                    
                    if sentence == "quit":
                        break

                    sentence = tokenize(sentence)
                    X = bag_of_words(sentence, all_words)
                    X = X.reshape(1, X.shape[0])
                    X = torch.from_numpy(X).to(device)

                    output = model_nlp(X)
                    _, predicted = torch.max(output, dim=1)

                    tag = tags[predicted.item()]

                    probs = torch.softmax(output, dim=1)
                    prob = probs[0][predicted.item()]
                    if prob.item() > 0.85:
                        for intent in intents['intents']:
                            if tag == intent["tag"]: 
                                reply = (f" {random.choice(intent['responses'])}")

                                if "time" in reply:
                                    NonInputExecution(reply)

                                elif "date" in reply:
                                    NonInputExecution(reply)

                                else:
                                    say(reply)
                else:
                    rec.PartialResult()
                if dump_fn is not None:
                    dump_fn.write(data)

except KeyboardInterrupt:
    print('\nDone')
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
