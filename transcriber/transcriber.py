from faster_whisper import WhisperModel
from dataclasses import dataclass

@dataclass 
class TranscribeToken:
    segment_start: float
    segment_finish: float
    segment_text: str

def transcribe(source_filename) -> list[TranscribeToken]:

    model_size = "large-v3"
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    segments, info = model.transcribe(source_filename, language="ru", beam_size=5)

    result_list = []

    for segment in segments:
        result_list.append(TranscribeToken(round(segment.start, 2) , round(segment.end, 2), segment.text))
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
    return result_list