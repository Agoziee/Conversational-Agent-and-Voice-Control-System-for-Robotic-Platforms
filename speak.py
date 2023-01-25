import pyttsx3

engine = pyttsx3.init('espeak')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)


def say(Text):
    print("   ")
    print(f"Robot: {Text}")
    engine.say(text=Text)
    engine.runAndWait()
    print("   ")

