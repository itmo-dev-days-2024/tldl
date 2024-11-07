from shutil import copyfile
from tldl.logic.base import AbstractHandler, TldlContext


class CopyFileHandler(AbstractHandler):
    def handle(self, context: TldlContext) -> TldlContext:
        old_file, old_ext = context.source_filename.split(".", 2)
        new_filename = f"{old_file}-cleaned.{old_ext}"
        copyfile(context.source_filename, new_filename)

        context.source_filename = new_filename
        return super().handle(context)
