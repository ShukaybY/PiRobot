import subprocess

def speak(text):
    subprocess.run([
        'espeak',
        '-v', 'en',
        text,
        '--stdout'
    ], stdout=subprocess.PIPE)

# Alternative direct aplay approach
def speak_v2(text):
    import subprocess
    tts = subprocess.Popen(
        ['espeak', '--stdout', text],
        stdout=subprocess.PIPE
    )
    play = subprocess.Popen(
        ['aplay', '-D', 'plughw:1,0', '-f', 'S16_LE', '-r', '22050', '-c', '1'],
        stdin=tts.stdout
    )
    play.wait()

speak_v2("hello I am your robot")
