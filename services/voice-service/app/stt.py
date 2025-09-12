import speech_recognition as sr

def speech_to_text(audio_file: str, lang: str = "hi-IN"):
    """
    Convert speech audio file into text.
    lang = "hi-IN" for Hindi, "en-US" for English
    """
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio, language=lang)
    except Exception as e:
        return f"Error: {str(e)}"
