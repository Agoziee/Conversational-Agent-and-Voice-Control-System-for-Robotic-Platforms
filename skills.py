import speak
import datetime




def Time():
    time = datetime.datetime.now().strftime("%H:%M")
    speak.say(time)

def Date():
    date = datetime.date.today()
    speak.say(date)

def NonInputExecution(query):
    query = str(query)

    if "time" in query:
        Time()

    elif "date" in query:
        Date()




    