from shutil import copyfile
import subprocess
from tempfile import NamedTemporaryFile
from tldl.logic.base import AbstractHandler, TldlContext


class ChaptersHandler(AbstractHandler):

    def handle(self, context: TldlContext) -> TldlContext:
        if context.chapters == None:
            return super().handle(context)
        with NamedTemporaryFile("w", suffix=".txt") as meatadata_file:
            meatadata_file.write(";FFMETADATA1\n")
            for chapter in context.chapters:
                meatadata_file.write(
                    f"[CHAPTER]\nTIMEBASE=1/1000\nSTART={chapter.start_pts * 1000}\nEND={chapter.end_pts * 1000}\ntitle={chapter.title}\n\n"
                )
            meatadata_file.flush()

            with NamedTemporaryFile("w", suffix=".mp4") as output_file:
                command = [
                    "ffmpeg",
                    "-y",  # Override files without asking
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
        return super().handle(context)
