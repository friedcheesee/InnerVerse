from googletrans import Translator

def translate_text(text,lang):
    dest1=" "
    translator = Translator()
    if lang == "English":
        return text
    elif lang== "Hindi":
        dest1='hi'
    elif lang== "Gujarati":
        dest1='gu'    
    elif lang=="Kannada":
        dest1='kn'    
    elif lang=="tamil":
        dest1="ta"    
    result = translator.translate(text, dest1)
    return result.text



