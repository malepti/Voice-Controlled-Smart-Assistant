
# Smart Assistant using Speech Recognition, Gemini 2.5 Flash, Google Search, and YouTube
import speech_recognition as sr
import pywhatkit
import webbrowser
import requests

# --- CONFIGURATION ---
GEMINI_API_KEY = 'AIzaSyDrXz-F9WebSOw8OmYnfR_FWoF505bUDtk'  # Replace with your Gemini 2.5 Flash API key
GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=' + GEMINI_API_KEY

def listen_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f'You said: {text}')
        return text
    except Exception as e:
        print('Sorry, could not recognize your voice.')
        return ''

def ask_gemini(prompt):
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    response = requests.post(GEMINI_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        try:
            return result['candidates'][0]['content']['parts'][0]['text']
        except Exception:
            return 'Sorry, I could not process that.'
    else:
        return 'Error contacting Gemini API.'

def google_search(query):
    # Simple Google search using webbrowser
    url = f'https://www.google.com/search?q={query.replace(" ", "+")}'
    webbrowser.open(url)
    print(f'Searching Google for: {query}')

def play_youtube_song(song):
    print(f'Playing on YouTube: {song}')
    pywhatkit.playonyt(song)

def main():
    print('Smart Assistant is running. Say something!')
    while True:
        user_input = listen_speech()
        if not user_input:
            continue
        # Check for exit
        if 'exit' in user_input.lower() or 'quit' in user_input.lower():
            print('Goodbye!')
            break
        # Play song
        elif 'play' in user_input.lower() and 'youtube' in user_input.lower():
            song = user_input.lower().replace('play', '').replace('on youtube', '').strip()
            play_youtube_song(song)
        # Google search
        elif 'search' in user_input.lower() or 'google' in user_input.lower():
            query = user_input.lower().replace('search', '').replace('on google', '').strip()
            google_search(query)
        # Otherwise, ask Gemini
        else:
            response = ask_gemini(user_input)
            print('Gemini:', response)

if __name__ == '__main__':
    main()
