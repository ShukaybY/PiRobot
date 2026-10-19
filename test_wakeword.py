from pathlib import Path
import openwakeword
import os
from openwakeword.model import Model
import sounddevice as sd
import numpy as np

MODEL_PATH = os.environ.get("WAKEWORD_MODEL_PATH", str(Path(openwakeword.__file__).parent / "resources" / "models" / "hey_jarvis_v0.1.onnx"))

if not Path(MODEL_PATH).is_file():
    raise SystemExit("Wake-word model is missing. Download openWakeWord models as described in README.md.")

model = Model(wakeword_models=[MODEL_PATH], inference_framework="onnx")

CHUNK = 1280
MIC_INDEX = 1

print("Listening for 'Hey Jarvis'... say it to test.")
print("Press Ctrl+C to stop.")

with sd.InputStream(
    samplerate=16000,
    channels=1,
    dtype='int16',
    blocksize=CHUNK,
    device=MIC_INDEX
) as stream:
    while True:
        audio_chunk, _ = stream.read(CHUNK)
        audio_flat = audio_chunk.flatten()
        prediction = model.predict(audio_flat)

        for word, score in prediction.items():
            if score > 0.5:
                print(f"Wake word detected! '{word}' score: {score:.2f}")
