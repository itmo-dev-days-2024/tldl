from faster_whisper import WhisperModel
from dataclasses import dataclass

@dataclass 
class TranscribeToken:
    segment_start: float
    segment_finish: float
    segment_text: str
    def __str__ (self):
        return f'''[{self.segment_start:.2f}s -> {self.segment_finish:.2f}s] {self.segment_text} \n'''

def transcribe(source_filename) -> list[TranscribeToken]:

    model_size = "large-v3"
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    segments, info = model.transcribe(source_filename, language="ru", beam_size=5)

    result_list = []
    
    for segment in segments:
        tt = TranscribeToken(round(segment.start, 2) , round(segment.end, 2), segment.text)
        result_list.append(tt)
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

    return result_list
