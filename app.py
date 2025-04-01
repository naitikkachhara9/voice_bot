import streamlit as st
import google.generativeai as genai
import speech_recognition as sr
from gtts import gTTS
import io
import sounddevice as sd
import numpy as np
import soundfile as sf
from io import BytesIO

# Configure your Gemini API key
genai.configure(api_key="AIzaSyCQ9Vype-aFxyYErN7lOMcNK4gjyiBwdwQ") # Replace with your actual Gemini API key
model = genai.GenerativeModel('gemini-2.0-flash')

# Function to interact with Gemini API
def ask_gemini(question):
    try:
        response = model.generate_content(question)
        return response.text.strip().lower()
    except Exception as e:
        st.error(f"Error interacting with Gemini API: {e}")
        return None

# Function to listen to user's voice input
def listen_to_user():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening for your question...")
        audio = recognizer.listen(source)
        try:
            query = recognizer.recognize_google(audio)
            return query
        except Exception as e:
            st.write("Sorry, I couldn't understand that.")
            return None

# Function for Text-to-Speech response (in-memory playback with sounddevice)
def speak_response(response):
    tts = gTTS(text=response, lang='en')
    mp3_fp = io.BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    try:
        data, samplerate = sf.read(BytesIO(mp3_fp.getvalue()))
        sd.play(data, samplerate)
        sd.wait() # waits until playback is finished.
    except Exception as e:
        st.error(f"Error playing audio: {e}")

# Streamlit UI
st.title("Voice Bot with Gemini")

# Input for voice recording button
if st.button("Record your question"):
    question = listen_to_user()
    if question:
        st.write(f"You asked: {question}")
        response = ask_gemini(question)
        if response:
            st.write(f"Bot says: {response}")
            speak_response(response)
        else:
            st.write("Gemini could not provide a response.")
    else:
        st.write("No question recognized. Please try again.")