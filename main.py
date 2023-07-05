import asyncio
import tempfile
import time
import sounddevice as sd
from pydub import AudioSegment
from shazamio import Shazam
from scipy.io.wavfile import write

RATE = 44100
DURATION = 15

def record_audio(wav_file_path):
    rec = sd.rec(int(DURATION * RATE), samplerate=RATE, channels=1)
    sd.wait()
    write(wav_file_path, RATE, rec)

def convert_to_mp3(wav_file_path, mp3_file_path):
    sound = AudioSegment.from_wav(wav_file_path)
    sound.export(mp3_file_path, format='mp3')

async def recognize_mp3(mp3_file_path):
    shazam = Shazam()
    out = await shazam.recognize_song(mp3_file_path)
    return out

def recognize_song():
    temp_wav = tempfile.NamedTemporaryFile(suffix='.wav')
    temp_mp3 = tempfile.NamedTemporaryFile(suffix='.mp3')
    record_audio(temp_wav.name)
    convert_to_mp3(temp_wav.name, temp_mp3.name)
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(recognize_mp3(temp_mp3.name))

if __name__ == '__main__':
    while True:
        recognized_song = recognize_song()
        if not recognized_song['matches']:
            print('No song recognized, waiting 5 seconds...')
            time.sleep(5)
        else:
            print('Song recognized!')
            print("Artist: ", recognized_song['track']['subtitle'])
            print("Artist: ", recognized_song['track']['title'])
            print('Waiting 30 seconds for next song...')
            time.sleep(5)
