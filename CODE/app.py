from transformers import pipeline
import streamlit as st
from PIL import Image
import os
from app_funcs import *
import pandas as pd


st.set_page_config(
    page_title="Emotion Detector",
    page_icon="😉",
    layout="centered",
    initial_sidebar_state="auto",
)

upload_path = "uploads/"
download_path = "downloads/"
st.title("😲 Deep Emotion Detector 😄")
st.subheader('_EmoRoBERTa_ Model from _Huggingface_ Transformers',)

# if format_type == "Plain Text 📝":
text = st.text_area("Enter your text here: 🎯", height=300)

if st.button("Find Emotion ✨") and (text or len(text) != 0):
    with st.spinner(f"Finding Emotion... 💫"):
        emotion_output, emotion_score = emotion_generate(text)

        emotion_attached_text = f"{text} <{emotion_output}>"
        data = {'Emotion-Attached Text': [emotion_attached_text]}
        df1 = pd.DataFrame(data)

            # Append the DataFrame to the CSV file
        with open('real-time_emotion_predictions.csv', 'a') as f:
            df1.to_csv(f, header=False, index=False)
        
    if emotion_output and emotion_score:
        st.success("✅ " + emotion_output.title())
        if (emotion_score*100 > 60):
            st.success("score: "+str(emotion_score*100))
        download_success()
else:
    st.warning("Please enter the text and choose \"Find Emotion ✨\"")

