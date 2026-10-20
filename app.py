import streamlit as st
import os
import whisper
from gtts import gTTS
from deep_translator import GoogleTranslator

st.set_page_config(page_title="DesiDub AI", page_icon="🎬")

st.title("🎬 DesiDub AI - वीडियो डबिंग ऐप")
st.write("विदेशी भाषा के वीडियो को आसानी से हिंदी आवाज़ में बदलें!")

uploaded_file = st.file_uploader("यहाँ अपनी वीडियो फाइल चुनें (MP4)", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    st.video(uploaded_file)
    
    if st.button("हिंदी में डब करें (Dub Now)"):
        with st.spinner("वीडियो प्रोसेस हो रहा है, कृपया प्रतीक्षा करें..."):
            # वीडियो सेव करना
            video_path = "temp_video.mp4"
            with open(video_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # ऑडियो अलग करना
            audio_path = "temp_audio.mp3"
            os.system(f"ffmpeg -y -i {video_path} -q:a 0 -map a {audio_path}")
            
            # व्हिस्पर से ट्रांसक्राइब करना
            model = whisper.load_model("base")
            result = model.transcribe(audio_path, task="translate")
            english_text = result["text"]
            
            # हिंदी अनुवाद
            hindi_text = GoogleTranslator(source='auto', target='hi').translate(english_text)
            
            st.subheader("📝 हिंदी अनुवाद:")
            st.write(hindi_text)
            
            # हिंदी ऑडियो बनाना
            output_audio = "hindi_output.mp3"
            tts = gTTS(text=hindi_text, lang='hi', slow=False)
            tts.save(output_audio)
            
            st.subheader("🔊 हिंदी डब ऑडियो:")
            st.audio(output_audio)
