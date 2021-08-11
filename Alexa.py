import speech_recognition as sr #para alexa compreender a minha voz
import pyttsx3  #alexa speaks to me
import pywhatkit 
import datetime
import wikipedia 

listener = sr.Recognizer() #reconhece a minha voz
engine = pyttsx3.init() #iniciar o engine
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()
    
def take_command():  
    try: #microfone pode nao funcionar
        with sr.Microphone() as source: #microfone passa a designar-se source
            print('listening...') #para saber quando posso falar
            voice = listener.listen(source)
            command = listener.recognize_google(voice) #convert voice to text usando google API, google devolve o texto
            command = command.lower()
            if 'alexa' in command:
                command = command.replace('alexa', '') #remover alexa da string
            
    except:
        pass #ignora
    return command

def run_alexa():
    command = take_command()
    print(command)
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song, use_api=True)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%H:%M')
        talk('Current time is ' + time)
    elif 'search' in command:
        wiki = command.replace('Search ', '')
        info = wikipedia.summary(wiki, 1)
        print(info)
        talk(info)
    elif 'Alexa go to sleep' in command:
        talk('It was a pleasure to serve you my lord, have a good day')
        quit()
    else:
        talk('Please say the command again')

while True:
    run_alexa()