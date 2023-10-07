import streamlit as st
import speech_recognition as sr
import openai
import os
from gtts import gTTS

st.title('Voice-Assisted Chatbot')

st.write('Ask Question, I am Listening...')

openai.api_key = os.environ["OPENAI_API_KEY"] 

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
  response = openai.Completion.create(
    engine="text-curie-001", 
    prompt=text,
    max_tokens=100
  )
  return response.choices[0].text

def text_to_speech(text):
  tts = gTTS(text)
  filename = "voice.mp3"
  tts.save(filename)
  return filename

while True:

  user_text = get_text()

  if user_text:
    st.session_state.generated.append("You: " + user_text)
    st.write("You: ", user_text)

    ai_text = get_response(user_text)
    st.session_state.generated.append("Bot: " + ai_text)
    st.write("Bot: ", ai_text)

    voice_file = text_to_speech(ai_text)
    st.audio(voice_file)

for line in st.session_state['generated']:
  st.write(line)