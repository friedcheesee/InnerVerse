import speech_recognition as sr
r = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        print("Talk")
        audio_text = r.listen(source)
        print("Time over, thanks")
        try:
            print("Text: "+r.recognize_google(audio_text))
        except:
            print("Sorry, I did not get that")
    return r.recognize_google(audio_text)
