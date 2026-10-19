# Configuration reference

Run from the repository root. No `.env` loader, automatic system configuration, or external settings parser is implemented. The reviewed [root example](../.env.example) and [config example](../config/environment.env.example) list environment variables only. Neither contains a key.

## Environment variables

| Variable | Used by | Behavior |
|---|---|---|
| `GEMINI_API_KEY` | robot, test_gemini, test_vision | Required nonempty shell variable; missing value exits with an explanatory error |
| `GEMINI_MODEL` | Same three scripts | Defaults to inherited `gemini-3.5-flash`; model availability/account access and audio/image support Need confirmation |
| `WAKEWORD_MODEL_PATH` | robot, test_wakeword | Optional ONNX classifier path; default is `resources/models/hey_jarvis_v0.1.onnx` inside the active openwakeword installation |

No Python package installation path is hardcoded to the old machine. Follow README's model download step to obtain shared feature models too. Both scripts select `inference_framework="onnx"` with `wakeword_models=[...]`. Detection is local, score >0.5, 1280-sample chunks at 16kHz mono int16. The wake phrase is Hey Jarvis; changing the robot's display name does not retrain a wake model.

## Audio: edit source after discovery

Use `python -m sounddevice` for PortAudio indexes, `arecord -l` for ALSA capture cards, and `aplay -l` for playback cards. PortAudio indexes and ALSA card numbers are different identifiers; defaults below are inherited, not portable guarantees.

| File / setting | Supplied value | Actual use |
|---|---|---|
| robot `MIC_INDEX` | 1 | Wake-word InputStream only |
| robot `record_audio()` | `device=1` | Conversation recording; edit separately from MIC_INDEX |
| robot `SAMPLE_RATE`, `DURATION` | 16000, 5 | Recording rate and seconds |
| robot `MIC_CARD`, `SPEAKER_CARD` | 1, 0 | Defined but unused; changing them alone does not reroute audio |
| robot `speak()` | `plughw:0,0` | ALSA playback device |
| test_wakeword `MIC_INDEX` | 1 | Local wake stream |
| test_gemini `speak()` | `plughw:1,0` | ALSA playback |
| test_tts `speak_v2()` | `plughw:1,0` | ALSA playback actually called |

Main TTS is `espeak --stdout -v en+f3 -s 195 -p 75 -a 190`, piped to aplay as S16_LE/22050Hz/mono. Diagnostic TTS options differ. No private ALSA configuration or udev rules are required by the repository; device routing needs local validation.

## GPIO, display and servo angles

`robot.py`, `test_servos.py`, and `test_arm_positions.py` use BCM12 (physical 32) for left signal and BCM13 (physical 33) for right signal. `RPi.GPIO.PWM` generates software PWM at 50Hz. Duty mapping is `2 + angle/18` percent, then zero after 0.4 seconds in robot / 0.5 seconds in diagnostics. These values are inherited, not calibrated safe travel limits.

Main program `ARM_ANGLES` uses the following left angle and mirrors the right to `180 - left`:

| Emotion | Left | Right |
|---|---|---|
| NEUTRAL | 160° | 20° |
| HAPPY | 120° | 60° |
| SAD | 180° | 0° |
| ANGRY | 0° | 180° |
| CURIOUS | 150° | 30° |
| SURPRISED | 90° | 90° |
| SLEEPY | 180° | 0° |

`test_servos.py` uses equal 0/90/180° angles on both channels, not the main mirrored poses. `test_arm_positions.py` accepts integer input without enforcing the 0–180 range. Confirm mechanical endpoints and power before execution; boot/listen/blink/shutdown can command movement. Do not change GPIO assignments without updating all three scripts and documentation.

OLED scripts use I2C bus 1 / address 0x3C and the SH1106 driver. `eye_lib.py` draws 128×64 images. The main camera and camera/vision diagnostics invoke `rpicam-still` with a 500ms timeout, no preview, JPEG quality 85, writing root `capture.jpg`. Temporary conversation WAVs use the OS temporary directory; successful transcription deletes them. Relative output paths follow the current working directory.

Planned sensor/motor GPIO entries are in [wiring](wiring.md); they are not active configuration in this code. Wake-word, camera, AI-model availability, servo limits and audio selection all require Pi-side checks.
