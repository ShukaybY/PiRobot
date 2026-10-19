import os

API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
if not API_KEY:
    raise SystemExit("GEMINI_API_KEY is missing. Export it in your shell before running this script; see README.md.")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")

from google import genai
import subprocess
import base64

client = genai.Client(api_key=API_KEY)

def capture_image(path="capture.jpg"):
    subprocess.run([
        'rpicam-still',
        '-o', path,
        '--timeout', '500',
        '--nopreview',
        '-q', '85'
    ], capture_output=True)
    return os.path.exists(path)

def ask_gemini_vision(question, image_path):
    with open(image_path, 'rb') as f:
        image_bytes = f.read()

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=[
            {
                "parts": [
                    {
                        "text": (
                            "You are a small curious robot named fruit_box. "
                            "Respond in 1-2 short sentences. "
                            "Tag your emotion: [HAPPY] [ANGRY] [CURIOUS] [SAD] [SURPRISED]. "
                            f"The user asks: {question}"
                        )
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
    return response.text.strip()

print("Capturing image...")
if capture_image():
    print("Image captured.")
    question = input("Ask fruit_box something about what it sees: ")
    print("Thinking...")
    response = ask_gemini_vision(question, "capture.jpg")
    print(f"fruit_box: {response}")
else:
    print("Camera failed.")
