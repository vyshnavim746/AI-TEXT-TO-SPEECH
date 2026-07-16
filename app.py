import os
from dotenv import load_dotenv
import streamlit as st
from elevenlabs.client import ElevenLabs 

load_dotenv()

api_key = os.getenv("ELEVENLABS_API_KEY")

st.set_page_config(page_title="ElevenLabs Text to Speech", page_icon="🔊")

st.title("🔊 ElevenLabs Text-to-Speech")

if not api_key:
    st.error("ELEVENLABS_API_KEY not found in .env")
    st.stop()

client = ElevenLabs(api_key=api_key) 

text = st.text_area("Enter text", height=180)

voice_id = st.text_input(
    "Voice ID",
    value="JBFqnCBsd6RMkjVDRZzb"
)

if st.button("Generate Speech"):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        audio = client.text_to_speech.convert(
            voice_id=voice_id,
            model_id="eleven_multilingual_v2",
            text=text
        )  

        out_path = "output/output.mp3"
        with open(out_path, "wb") as f:  
            for chunk in audio:
                f.write(chunk)

        st.success("Speech generated!")
        st.audio(out_path)
        with open(out_path, "rb") as f:
            st.download_button("Download MP3", f, file_name="speech.mp3")