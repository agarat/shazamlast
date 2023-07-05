import sounddevice as sd
from scipy.io.wavfile import write
from ShazamAPI import Shazam
from pydub import AudioSegment
import tempfile

RATE = 44100
DURATION = 10

def record_audio(wav_file_path):
    rec = sd.rec(int(duration * RATE), samplerate=RATE, channels=2)
    sd.wait()
    write(wav_file_path, RATE, rec)

def convert_to_mp3(wav_file_path, mp3_file_path):
    sound = AudioSegment.from_wav(wav_file_path)
    sound.export(mp3_file_path, format='mp3')

def recognize_mp3(mp3_file_path):
    mp3_file = open(mp3_file_path, 'rb').read()
    shazam = Shazam(mp3_file)
    recognize_generator = shazam.recognizeSong()
    return recognize_generator

if __name__ == '__main__':
    temp_wav = tempfile.TemporaryFile(suffix='.wav')
    temp_mp3 = tempfile.TemporaryFile(suffix='.mp3')
    record_audio(temp_wav)
    convert_to_mp3(temp_wav, temp_mp3)
    print(next(recognize_mp3(temp_mp3)))
