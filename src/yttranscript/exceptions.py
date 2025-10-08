"""Custom exceptions for yttranscript."""


class YttranscriptError(Exception):
    """Base exception for yttranscript."""
    pass


class InvalidUrlError(YttranscriptError):
    """Invalid YouTube URL provided."""
    pass


class TranscriptNotAvailableError(YttranscriptError):
    """No transcript available for video."""
    pass


class LanguageNotFoundError(YttranscriptError):
    """Requested language not available."""
    pass


class NetworkError(YttranscriptError):
    """Network operation failed."""
    pass


class FileOutputError(YttranscriptError):
    """File output operation failed."""
    pass