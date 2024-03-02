import streamlit as st
import speech_recognition as sr
import openai
import os
from gtts import gTTS
from openai import OpenAI
import time

st.set_page_config(page_title="Voice-Assisted Chatbot 🎙️", page_icon=":microphone:")
st.title('Voice-Assisted Chatbot 🎙️')

st.write('Ask Question, I am Listening...')

# Add a text input field in the sidebar for the OpenAI API key
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

if api_key:
    client = OpenAI(api_key=api_key)
else:
    st.warning("Please enter your OpenAI API Key in the sidebar.")
    st.stop()

if 'generated' not in st.session_state:
  st.session_state['generated'] = []

def get_text():
  r = sr.Recognizer()
  with sr.Microphone() as source:
    audio = r.listen(source)
  try:
    return r.recognize_google(audio)
  except:
    return ""

def get_response(text):
  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "user", "content": text}
    ]
  )
  return response.choices[0].message.content

def text_to_speech(text):
  tts = gTTS(text)
  filename = "voice.mp3"
  tts.save(filename)
  return filename

while True:
  with st.spinner("Listening..."):
    user_text = get_text()

  if user_text:
    st.session_state.generated.append("🙋: " + user_text)
    st.markdown("<p style='font-size:18px;'>🙋: " + user_text + "</p>", unsafe_allow_html=True)

    with st.spinner("Generating response..."):
      ai_text = get_response(user_text)

    st.session_state.generated.append("🤖: " + ai_text)
    st.markdown("<p style='font-size:18px;'>🤖: " + ai_text + "</p>", unsafe_allow_html=True)

    voice_file = text_to_speech(ai_text)
    st.audio(voice_file)

for line in st.session_state['generated']:
  st.write(line)
