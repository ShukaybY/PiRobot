import os

API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
if not API_KEY:
    raise SystemExit("GEMINI_API_KEY is missing. Export it in your shell before running this script; see README.md.")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")

from pathlib import Path
import openwakeword
from google import genai
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from openwakeword.model import Model as WakeWordModel
import expressions
import sounddevice as sd
import scipy.io.wavfile as wav
import subprocess
import tempfile
import time
import threading
import base64
import RPi.GPIO as GPIO

client = genai.Client(api_key=API_KEY)

MIC_INDEX = 1
SAMPLE_RATE = 16000
DURATION = 5
MIC_CARD = 1
SPEAKER_CARD = 0

# Wake word setup
WAKEWORD_MODEL_PATH = os.environ.get("WAKEWORD_MODEL_PATH", str(Path(openwakeword.__file__).parent / "resources" / "models" / "hey_jarvis_v0.1.onnx"))
if not Path(WAKEWORD_MODEL_PATH).is_file():
    raise SystemExit("Wake-word model is missing. Download openWakeWord models as described in README.md.")

wakeword_model = WakeWordModel(wakeword_models=[WAKEWORD_MODEL_PATH], inference_framework="onnx")
WAKEWORD_CHUNK = 1280

SYSTEM_PROMPT = (
    "You are a small curious robot named fruit_box. "
    "Respond in 1-2 short sentences. "
    "You speak in Gen-Z slang"
    "Tag your emotion at the end: [HAPPY] [ANGRY] [CURIOUS] [SAD] [SURPRISED] [SLEEPY]. "
    "Never break character."
)

# OLED setup
serial = i2c(port=1, address=0x3C)
device = sh1106(serial)

current_emotion = "NEUTRAL"
blink_thread_running = True

def show(img):
    device.display(img.convert(device.mode))

def show_emotion(emotion):
    global current_emotion
    current_emotion = emotion
    if emotion == "HAPPY":
        show(expressions.happy())
    elif emotion == "ANGRY":
        show(expressions.angry())
    elif emotion == "CURIOUS":
        show(expressions.curious_look("left"))
    elif emotion == "SAD":
        show(expressions.sad())
    elif emotion == "SURPRISED":
        show(expressions.surprised())
    elif emotion == "SLEEPY":
        show(expressions.sleepy())
    else:
        show(expressions.neutral())
    set_arms(emotion)

def blink_loop():
    while blink_thread_running:
        time.sleep(4)
        show(expressions.blink())
        time.sleep(0.15)
        show_emotion(current_emotion)

def record_audio():
    show(expressions.curious_look("left"))
    print("Listening...")
    audio = sd.rec(
        int(DURATION * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype='int16',
        device=1
    )
    sd.wait()
    print("Done listening.")
    tmp = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    wav.write(tmp.name, SAMPLE_RATE, audio)
    return tmp.name

def transcribe(wav_path):
    with open(wav_path, 'rb') as f:
        audio_bytes = f.read()
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=[
            {
                "parts": [
                    {"text": "Transcribe this audio exactly as spoken. Return only the transcribed text, nothing else."},
                    {"inline_data": {"mime_type": "audio/wav", "data": base64.b64encode(audio_bytes).decode()}}
                ]
            }
        ]
    )
    return response.text.strip()

def capture_image(path="capture.jpg"):
    subprocess.run([
        'rpicam-still',
        '-o', path,
        '--timeout', '500',
        '--nopreview',
        '-q', '85'
    ], capture_output=True)
    return os.path.exists(path)

def ask_gemini(user_text):
    image_path = "capture.jpg"
    has_image = capture_image(image_path)

    if has_image:
        with open(image_path, 'rb') as f:
            image_bytes = f.read()
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=[
                {
                    "parts": [
                        {
                            "text": f"{SYSTEM_PROMPT}\nUser says: {user_text}"
                        },
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": base64.b64encode(image_bytes).decode()
                            }
                        }
                    ]
                }
            ]
        )
    else:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=f"{SYSTEM_PROMPT}\nUser says: {user_text}"
        )
    return response.text.strip()

def clean_response(text):
    for tag in ['[HAPPY]', '[ANGRY]', '[CURIOUS]', '[SAD]',
                '[SURPRISED]', '[SLEEPY]']:
        text = text.replace(tag, '')
    return text.strip()

def handle_emotion(text):
    if '[HAPPY]' in text:
        print('>> Emotion: HAPPY')
        show_emotion('HAPPY')
    elif '[ANGRY]' in text:
        print('>> Emotion: ANGRY')
        show_emotion('ANGRY')
    elif '[CURIOUS]' in text:
        print('>> Emotion: CURIOUS')
        show_emotion('CURIOUS')
    elif '[SAD]' in text:
        print('>> Emotion: SAD')
        show_emotion('SAD')
    elif '[SURPRISED]' in text:
        print('>> Emotion: SURPRISED')
        show_emotion('SURPRISED')
    elif '[SLEEPY]' in text:
        print('>> Emotion: SLEEPY')
        show_emotion('SLEEPY')
    else:
        show_emotion('NEUTRAL')

def speak(text):
    tts = subprocess.Popen(
        ['espeak', '--stdout', '-v', 'en+f3', '-s', '195', '-p', '75', '-a', '190', text],
        stdout=subprocess.PIPE
    )
    play = subprocess.Popen(
        ['aplay', '-D', 'plughw:0,0', '-f', 'S16_LE', '-r', '22050', '-c', '1'],
        stdin=tts.stdout
    )
    play.wait()

# Servo setup
LEFT_SERVO = 12
RIGHT_SERVO = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(LEFT_SERVO, GPIO.OUT)
GPIO.setup(RIGHT_SERVO, GPIO.OUT)

left_pwm = GPIO.PWM(LEFT_SERVO, 50)
right_pwm = GPIO.PWM(RIGHT_SERVO, 50)

left_pwm.start(0)
right_pwm.start(0)

# Arm angles per emotion
ARM_ANGLES = {
    "NEUTRAL":   160,
    "HAPPY":     120,
    "SAD":       180,
    "ANGRY":     0,
    "CURIOUS":   150,
    "SURPRISED": 90,
    "SLEEPY":    180,
}

def set_angle(servo, angle):
    duty = 2 + (angle / 18)
    servo.ChangeDutyCycle(duty)
    time.sleep(0.4)
    servo.ChangeDutyCycle(0)

def set_arms(emotion):
    angle = ARM_ANGLES.get(emotion, 160)
    set_angle(left_pwm, angle)
    set_angle(right_pwm, 180 - angle)

# Start blink thread
blink_thread = threading.Thread(target=blink_loop, daemon=True)
blink_thread.start()

# Boot animation
print("fruit_box booting...")
show(expressions.sleepy())
time.sleep(0.5)
show(expressions.neutral())
time.sleep(0.3)
show(expressions.happy())
time.sleep(0.5)
show(expressions.neutral())

print("fruit_box is online. Press Ctrl+C to stop.")
print("="*40)

print("fruit_box is online. Say 'Hey Jarvis' to wake up.")
print("="*40)

def listen_for_wakeword():
    with sd.InputStream(
        samplerate=16000,
        channels=1,
        dtype='int16',
        blocksize=WAKEWORD_CHUNK,
        device=MIC_INDEX
    ) as stream:
        while True:
            audio_chunk, _ = stream.read(WAKEWORD_CHUNK)
            audio_flat = audio_chunk.flatten()
            prediction = wakeword_model.predict(audio_flat)
            for word, score in prediction.items():
                if score > 0.5:
                    return

while True:
    try:
        show(expressions.neutral())
        set_arms("NEUTRAL")
        print("Waiting for wake word...")
        listen_for_wakeword()

        print("Wake word detected!")
        show(expressions.surprised())
        set_arms("SURPRISED")
        speak("Yeah?")

        wav_path = record_audio()

        print("Transcribing...")
        user_text = transcribe(wav_path)
        print(f"You said: {user_text}")
        os.unlink(wav_path)

        if not user_text or len(user_text) < 2:
            print("Didn't catch that.")
            show_emotion("NEUTRAL")
            continue

        print("Thinking...")
        show(expressions.blink())
        response = ask_gemini(user_text)
        print(f"fruit_box: {response}")

        handle_emotion(response)
        speak(clean_response(response))
        print("="*40)

    except KeyboardInterrupt:
        blink_thread_running = False
        print("\nfruit_box going offline.")
        show(expressions.sad())
        set_arms("SAD")
        time.sleep(1)
        left_pwm.stop()
        right_pwm.stop()
        GPIO.cleanup()
        device.cleanup()
        break
