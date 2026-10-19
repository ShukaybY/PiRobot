import os

API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
if not API_KEY:
    raise SystemExit("GEMINI_API_KEY is missing. Export it in your shell before running this script; see README.md.")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")

from google import genai
import subprocess

client = genai.Client(api_key=API_KEY)

def speak(text):
    tts = subprocess.Popen(
        ['espeak', '--stdout', text],
        stdout=subprocess.PIPE
    )
    play = subprocess.Popen(
        ['aplay', '-D', 'plughw:1,0', '-f', 'S16_LE', '-r', '22050', '-c', '1'],
        stdin=tts.stdout
    )
    play.wait()

def clean_response(text):
    tags = ['[HAPPY]', '[ANGRY]', '[CURIOUS]', '[SAD]']
    for tag in tags:
        text = text.replace(tag, '')
    return text.strip()

def handle_emotion(text):
    if '[HAPPY]' in text:
        print('Emotion: HAPPY')
    elif '[ANGRY]' in text:
        print('Emotion: ANGRY')
    elif '[CURIOUS]' in text:
        print('Emotion: CURIOUS')
    elif '[SAD]' in text:
        print('Emotion: SAD')

def ask_robot(question):
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=f"You are a small curious robot named fruit_box. "
                 f"Respond in 1-2 short sentences. "
                 f"Tag your emotion: [HAPPY] [ANGRY] [CURIOUS] [SAD]. "
                 f"User says: {question}"
    )
    return response.text

print("Robot is thinking...")
response = ask_robot("What is the square root of 81?")
print(f"Response: {response}")
handle_emotion(response)
speak(clean_response(response))
