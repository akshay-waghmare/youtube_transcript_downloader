"""YouTube Transcript Downloader CLI tool.

A minimal Python CLI tool for extracting YouTube video transcripts.
"""

__version__ = "0.1.0"
__author__ = "YouTube Transcript Downloader Team"

from .core import TranscriptExtractor
from .exceptions import (
    YttranscriptError,
    InvalidUrlError,
    TranscriptNotAvailableError,
    LanguageNotFoundError,
    NetworkError,
    FileOutputError,
)
from .models import Video, Transcript, TranscriptSegment

__all__ = [
    "TranscriptExtractor",
    "Video",
    "Transcript", 
    "TranscriptSegment",
    "YttranscriptError",
    "InvalidUrlError",
    "TranscriptNotAvailableError",
    "LanguageNotFoundError",
    "NetworkError",
    "FileOutputError",
]