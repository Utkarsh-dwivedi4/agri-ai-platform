from gtts import gTTS
import os
from pydub import AudioSegment

def text_to_speech(text: str, lang: str = "hi"):
    """
    Convert text to speech in Hindi or English
    lang = "hi" for Hindi, "en" for English
    """
    tts = gTTS(text=text, lang=lang)
    file_path = "output.mp3"
    tts.save(file_path)

    # Convert mp3 to wav (optional, for better browser support)
    sound = AudioSegment.from_mp3(file_path)
    wav_path = "output.wav"
    sound.export(wav_path, format="wav")
    return wav_path
