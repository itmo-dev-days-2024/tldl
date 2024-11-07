import os
from shutil import copyfile
from tempfile import NamedTemporaryFile
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from pydub.silence import detect_leading_silence
from tldl.logic.base import AbstractHandler, TldlContext


def detect_leading_and_trailing_silence(audio_file, silence_threshold):
    audio = AudioSegment.from_file(audio_file)

    leading_silence_duration = detect_leading_silence(
        audio, silence_threshold=silence_threshold
    )

    reversed_audio = audio.reverse()
    trailing_silence_duration = detect_leading_silence(
        reversed_audio, silence_threshold=silence_threshold
    )

    return leading_silence_duration, trailing_silence_duration


def trim_video(infile, outfile, leading_silence_duration, trailing_silence_duration):
    video = VideoFileClip(infile)

    start_time = leading_silence_duration / 1000
    end_time = video.duration - (trailing_silence_duration / 1000)

    trimmed_video = video.subclip(start_time, end_time)

    trimmed_video.write_videofile(outfile, codec="libx264", audio_codec="aac")


def cut_silences(infile, outfile, silence_threshold=-30):
    audio_file = "audio.wav"
    video = VideoFileClip(infile)
    video.audio.write_audiofile(audio_file)

    leading_silence_duration, trailing_silence_duration = (
        detect_leading_and_trailing_silence(audio_file, silence_threshold)
    )

    trim_video(infile, outfile, leading_silence_duration, trailing_silence_duration)

    os.remove(audio_file)


class SilenceCutHandler(AbstractHandler):

    def handle(self, context: TldlContext) -> TldlContext:
        with NamedTemporaryFile("w", suffix=".mp4") as silence_file:
            cut_silences(context.source_filename, silence_file.name)
            copyfile(silence_file.name, context.source_filename)
        return super().handle(context)
