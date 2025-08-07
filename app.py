import streamlit as st
import speech_recognition as sr
import pywhatkit
import webbrowser
import requests

# --- CONFIGURATION ---
GEMINI_API_KEY = 'AIzaSyDrXz-F9WebSOw8OmYnfR_FWoF505bUDtk'
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

def listen_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info('🎧 Listening...')
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        st.success(f'🗣️ You said: {text}')
        return text
    except Exception:
        st.error('❌ Sorry, could not recognize your voice.')
        return ''

def ask_gemini(prompt):
    headers = {'Content-Type': 'application/json'}
    payload = {"contents":[{"parts":[{"text": prompt}]}]}
    try:
        resp = requests.post(GEMINI_API_URL, headers=headers, json=payload)
        resp.raise_for_status()
        return resp.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f'❌ Gemini error: {str(e)}'

def google_search(query):
    webbrowser.open_new_tab(f'https://www.google.com/search?q={query.replace(" ", "+")}')
    st.info(f'🔍 Searching Google for: {query}')

def play_youtube_song(song):
    if not song.strip():
        st.warning("⚠️ Please specify a song name.")
    else:
        st.info(f'🎵 Playing on YouTube: {song}')
        try:
            pywhatkit.playonyt(song)
        except Exception as e:
            st.error(f'❌ Failed to play song: {e}')

def set_bg():
    bg_url = 'https://static.vecteezy.com/system/resources/previews/021/477/545/non_2x/artificial-intelligence-chat-bot-concept-free-vector.jpg'
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url('{bg_url}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .stInfo, .stSuccess, .stWarning, .stError {{
        background-color: rgba(255, 255, 255, 0.95) !important;
        color: #000 !important;
        font-weight: 600;
        border-radius: 10px;
        font-size: 1rem;
        padding: 1rem 1.2rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.25);
        z-index: 2;
    }}
    .stSuccess {{ border-left: 6px solid #28a745 !important; }}
    .stInfo    {{ border-left: 6px solid #007bff !important; }}
    .stWarning {{ border-left: 6px solid #ffc107 !important; }}
    .stError   {{ border-left: 6px solid #dc3545 !important; }}
    .main-title {{
        color: #fff;
        font-size: 2.8rem;
        font-weight: bold;
        text-shadow: 2px 2px 8px #000;
        z-index: 2;
    }}
    .subtitle {{
        color: #ffffffdd;
    font-size: 1.4rem;
    font-weight: 500;
    text-shadow: 2px 2px 6px #00000099;
    margin-top: -0.5rem;
    margin-bottom: 2rem;
    position: relative;
    z-index: 2;
    }}
    .gemini-response {{
        background: rgba(255,255,255,0.9);
        border-radius: 12px;
        padding: 1em;
        margin-top: 1.5em;
        font-size: 1.1rem;
        color: #111;
        border-left: 6px solid #6c63ff;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        z-index: 2;
    }}
    </style>
    """, unsafe_allow_html=True)

def main():
    set_bg()
    st.markdown('<div class="main-title">🤖 Smart Voice Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">✨ Venkatesh_Voice_Assistant · Google · YouTube · </div>', unsafe_allow_html=True)


    user_input = st.text_input('✍️ Type a command or press mic below:')
    if st.button('🎙️ Speak'):
        user_input = listen_speech()

    if user_input:
        query = user_input.lower()
        if 'exit' in query or 'quit' in query:
            st.warning("👋 Goodbye!")
        elif 'youtube' in query and 'play' in query:
            song = query.replace('play', '').replace('on youtube', '').strip()
            play_youtube_song(song)
        elif 'search' in query or 'google' in query:
            search_term = query.replace('search', '').replace('on google', '').strip()
            google_search(search_term)
        else:
            response = ask_gemini(query)
            st.markdown(f'<div class="gemini-response"><b>Venkatesh:</b> {response}</div>', unsafe_allow_html=True)

if __name__ == '__main__':
    main()
