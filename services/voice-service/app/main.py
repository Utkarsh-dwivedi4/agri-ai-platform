from fastapi import FastAPI, UploadFile, File, Form
import speech_recognition as sr
import pyttsx3
from gtts import gTTS
import os
import uuid

app = FastAPI(title="Voice Assistant Service")

# 🎙 Speech-to-Text Endpoint
@app.post("/stt/")
async def speech_to_text(file: UploadFile = File(...)):
    recognizer = sr.Recognizer()
    with open("temp_audio.wav", "wb") as f:
        f.write(await file.read())

    with sr.AudioFile("temp_audio.wav") as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio, language="hi-IN")  # Hindi by default
            return {"text": text}
        except sr.UnknownValueError:
            return {"error": "Could not understand audio"}
        except sr.RequestError as e:
            return {"error": f"API unavailable {e}"}

# 🗣 Text-to-Speech Endpoint (pyttsx3 local voice)
@app.post("/tts/local/")
async def text_to_speech_local(text: str = Form(...)):
    engine = pyttsx3.init()
    engine.save_to_file(text, "output_voice.mp3")
    engine.runAndWait()
    return {"message": "Generated voice", "file": "output_voice.mp3"}

# 🗣 Text-to-Speech Endpoint (Google gTTS, multilingual)
@app.post("/tts/google/")
async def text_to_speech_google(text: str = Form(...), lang: str = Form("en")):
    filename = f"voice_{uuid.uuid4().hex}.mp3"
    tts = gTTS(text=text, lang=lang)
    tts.save(filename)
    return {"message": "Generated voice", "file": filename}
