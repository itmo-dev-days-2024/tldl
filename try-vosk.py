import os
import sys
import wave
import json
from vosk import Model, KaldiRecognizer

model_path = "/Users/aalim/Downloads/vosk-model-small-ru-0.22"

if not os.path.exists(model_path):
    print(f"Please download the model and unpack it to the current folder.")
    sys.exit(1)

model = Model(model_path)
audio_filepath = "out.wav"

# Open the wave file
wf = wave.open(audio_filepath, "rb")

if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
    print("Audio file must be WAV format, mono, and 16kHz.")
    sys.exit(1)

recognizer = KaldiRecognizer(model, wf.getframerate())

transcription = []

while True:
    data = wf.readframes(4000)
    if len(data) == 0:  # end of file
        break
    if recognizer.AcceptWaveform(data):
        result = recognizer.Result()
        result_dict = json.loads(result)
        transcription.append(result_dict.get('text', ''))

final_result = recognizer.FinalResult()
final_dict = json.loads(final_result)
transcription.append(final_dict.get('text', ''))

wf.close()

final_transcription = ' '.join(transcription)
print("Final transcription:")
print(final_transcription)