from dataclasses import dataclass
from abc import ABCMeta, abstractmethod
from typing import Optional


@dataclass
class TranscribeToken:
    segment_start: float
    segment_finish: float
    segment_text: str

    def __str__(self):
        return "[%.2fs -> %.2fs] %s \n" % (
            self.segment_start,
            self.segment_finish,
            self.segment_text,
        )


@dataclass
class Chapter:
    title: str
    description: str
    # expressed in 1/1000 timebase
    start_pts: int
    end_pts: int

    def __str__(self):
        return f"[{self.start_pts} - {self.end_pts}] - {self.title}: {self.description}"


@dataclass
class TldlContext:
    """
    Holds all needed variables and info about processing pipeline
    """

    source_filename: str = ""
    transcribed_text: list[TranscribeToken] = None
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
