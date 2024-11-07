from faster_whisper import WhisperModel

from tldl.logic.base import TranscribeToken, AbstractHandler, TldlContext


def transcribe(source_filename) -> list[TranscribeToken]:

    model_size = "large-v3"
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    segments, _ = model.transcribe(source_filename, language="ru", beam_size=5)

    result_list = []

    for segment in segments:
        result_list.append(
            TranscribeToken(
                round(segment.start, 2), round(segment.end, 2), segment.text
            )
        )
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
    return result_list


class TranscriberHandler(AbstractHandler):

    def handle(self, context: TldlContext) -> TldlContext:
        # here context gets populated by full text transcribtion
        transcribe_result = transcribe(context.source_filename)
        context.transcribed_text = transcribe_result
        return super().handle(context)
