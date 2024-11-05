from dataclasses import dataclass
from abc import ABCMeta, abstractmethod, abstractproperty


@dataclass
class Chapter:
    name: str
    description: str
    offset_seconds: int


@dataclass
class TldlContext:
    """
    Holds all needed variables and info about processing pipeline
    """

    source_filename: str
    transcribed_text: str
    summary: str
    chapters: list[Chapter]


class TldlHandler:
    __metaclass__ = ABCMeta

    @abstractmethod
    def set_next(self, next: TldlHandler) -> TldlHandler:
        pass

    @abstractmethod
    def handle(self, context: TldlContext) -> TldlContext:
        pass


class AbstractHandler(TldlHandler):
    _next_handler: TldlHandler = None

    def set_next(self, next: TldlHandler) -> TldlHandler:
        self._next_handler = next
        return next

    def handle(self, context: TldlContext) -> TldlContext:
        if self._next_handler:
            return self._next_handler(context)
        return context


class SilenceCutHandler(AbstractHandler):

    def handle(self, context: TldlContext) -> TldlContext:
        # here goes cutting and copying to new file
        return super().handle(context)


class TranscriberHandler(AbstractHandler):

    def handle(self, context: TldlContext) -> TldlContext:
        # here context gets populated by full text transcribtion
        context.transcribed_text = "..."


class SummarizerHandler(AbstractHandler):

    def handle(self, context: TldlContext) -> TldlContext:
        # here context gets populated for Chapters
        context.summary = "This lection introduces us to c++ language..."
        context.chapters = [
            Chapter("Introduction", "...", 60),
            Chapter("Syntax", "...", 60 * 12),
            Chapter("Course Schedule", "...", 60 * 30),
        ]
        return super().handle(context)


def main():
    handler = SilenceCutHandler().set_next(
        TranscriberHandler().set_next(SummarizerHandler())
    )

    context = TldlContext()
    context.source_filename = sys.argv[1]


if __name__ == "__main__":
    main()
