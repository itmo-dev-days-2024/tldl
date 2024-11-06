import sys
import subprocess
from shutil import copyfile
from dataclasses import dataclass
from abc import ABCMeta, abstractmethod, abstractproperty
from typing import Optional
from tempfile import NamedTemporaryFile
from silence_cutter import cut_silences


@dataclass
class Chapter:
    title: str
    description: str
    # expressed in 1/1000 timebase
    start_pts: int
    end_pts: int


@dataclass
class TldlContext:
    """
    Holds all needed variables and info about processing pipeline
    """

    source_filename: str = ""
    transcribed_text: str = ""
    summary: str = ""
    chapters: list[Chapter] = None


class TldlHandler:
    __metaclass__ = ABCMeta

    @abstractmethod
    def set_next(self, next: any) -> any:
        pass

    @abstractmethod
    def handle(self, context: TldlContext) -> TldlContext:
        pass


class AbstractHandler(TldlHandler):
    _next_handler: Optional[TldlHandler] = None

    def set_next(self, next: TldlHandler) -> TldlHandler:
        self._next_handler = next
        return self

    def handle(self, context: TldlContext) -> TldlContext:
        if self._next_handler:
            return self._next_handler.handle(context)
        return context


class CopyFileHandler(AbstractHandler):
    def handle(self, context: TldlContext) -> TldlContext:
        old_file, old_ext = context.source_filename.split(".", 2)
        new_filename = f"{old_file}-cleaned.{old_ext}"
        copyfile(context.source_filename, new_filename)

        context.source_filename = new_filename
        return super().handle(context)


class SilenceCutHandler(AbstractHandler):

    def handle(self, context: TldlContext) -> TldlContext:
        with NamedTemporaryFile("w", suffix=".mp4") as silence_file:
            cut_silences(context.source_filename, silence_file.name, dB=-30)
            copyfile(silence_file.name, context.source_filename)
        return super().handle(context)


class TranscriberHandler(AbstractHandler):

    def handle(self, context: TldlContext) -> TldlContext:
        # here context gets populated by full text transcribtion
        context.transcribed_text = "..."
        return super().handle(context)


class SummarizerHandler(AbstractHandler):

    def handle(self, context: TldlContext) -> TldlContext:
        # here context gets populated for Chapters
        context.summary = "This lection introduces us to c++ language..."
        context.chapters = [
            Chapter("Introduction", "...", 0, 60 * 11),
            Chapter("Syntax", "...", 60 * 12, 60 * 24),
            Chapter("Course Schedule", "...", 60 * 30, 60 * 40),
        ]
        return super().handle(context)


class ChaptersHandler(AbstractHandler):

    def handle(self, context: TldlContext) -> TldlContext:
        with NamedTemporaryFile("w", suffix=".txt") as meatadata_file:
            meatadata_file.write(";FFMETADATA1\n")
            for chapter in context.chapters:
                meatadata_file.write(
                    f"[CHAPTER]\nTIMEBASE=1/1000\nSTART={chapter.start_pts}\nEND={chapter.end_pts}\ntitle={chapter.title}\n\n"
                )
            meatadata_file.flush()

            with NamedTemporaryFile("w", suffix=".mp4") as output_file:
                command = [
                    "ffmpeg",
                    "-y", # Override files without asking
                    "-i",
                    context.source_filename,
                    "-i",
                    meatadata_file.name,  # Chapter metadata file
                    "-map_metadata",
                    "1",  # Map metadata from the chapters file (second input)
                    "-codec",
                    "copy",
                    output_file.name,  # Output MP4 file
                ]
                try:
                    subprocess.run(command, check=True)
                    output_file.flush()
                    copyfile(output_file.name, context.source_filename)
                    print(f"Chapters added successfully!")
                except subprocess.CalledProcessError as e:
                    print(f"Error occurred: {e}")
        return context


def main():
    handler = SilenceCutHandler().set_next(
        TranscriberHandler().set_next(SummarizerHandler().set_next(ChaptersHandler()))
    )

    context = TldlContext()
    context.source_filename = sys.argv[1]

    finish_context = handler.handle(context)
    if finish_context is None:
        print("Failed :c")
        exit(-1)

    print("Finished, filename: ", finish_context.source_filename)


if __name__ == "__main__":
    main()
