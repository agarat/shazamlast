import sounddevice as sd
from scipy.io.wavfile import write
import asyncio
from shazamio import Shazam
from pydub import AudioSegment
import tempfile

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
    print(out)


if __name__ == '__main__':
    temp_wav = tempfile.NamedTemporaryFile(suffix='.wav')
    print(temp_wav.name)
    temp_mp3 = tempfile.NamedTemporaryFile(suffix='.mp3')
    print(temp_mp3.name)
    record_audio(temp_wav.name)
    convert_to_mp3(temp_wav.name, temp_mp3.name)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(recognize_mp3(temp_mp3.name))
