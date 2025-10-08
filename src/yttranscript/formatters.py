"""Output formatting for transcripts."""

from typing import Protocol
from enum import Enum

from .models import Transcript


class FormatType(Enum):
    """Supported output formats."""
    PLAIN = "plain"
    MARKDOWN = "markdown"
    JSON = "json"  # Deferred P3 feature for machine-readable output


class Formatter(Protocol):
    """Interface for transcript formatters."""
    
    def format(self, transcript: Transcript, include_timestamps: bool = False) -> str:
        """Format transcript according to this formatter's rules.
        
        Args:
            transcript: Transcript to format
            include_timestamps: Whether to include timestamp information
            
        Returns:
            Formatted transcript string
        """
        ...


class PlainFormatter:
    """Plain text formatter."""
    
    def format(self, transcript: Transcript, include_timestamps: bool = False) -> str:
        """Format transcript as plain text.
        
        Args:
            transcript: Transcript to format
            include_timestamps: Whether to include timestamps
            
        Returns:
            Plain text formatted transcript
        """
        lines = []
        for segment in transcript.segments:
            line = ""
            if include_timestamps and segment.start is not None:
                line += f"{segment.format_timestamp()} "
            line += segment.text
            lines.append(line)
        return "\n".join(lines)


class MarkdownFormatter:
    """Markdown bullet-point formatter."""
    
    def format(self, transcript: Transcript, include_timestamps: bool = False) -> str:
        """Format transcript as Markdown with bullet points.
        
        Args:
            transcript: Transcript to format
            include_timestamps: Whether to include timestamps
            
        Returns:
            Markdown formatted transcript with bullet points
        """
        lines = []
        for segment in transcript.segments:
            line = "- "
            if include_timestamps and segment.start is not None:
                line += f"**{segment.format_timestamp()}** "
            line += segment.text
            lines.append(line)
        return "\n".join(lines)


def get_formatter(format_type: FormatType) -> Formatter:
    """Get formatter instance for the specified format type.
    
    Args:
        format_type: Type of formatter to create
        
    Returns:
        Formatter instance
        
    Raises:
        ValueError: If format type is not supported
    """
    if format_type == FormatType.PLAIN:
        return PlainFormatter()
    elif format_type == FormatType.MARKDOWN:
        return MarkdownFormatter()
    elif format_type == FormatType.JSON:
        raise ValueError("JSON format is not yet implemented (P3 feature)")
    else:
        raise ValueError(f"Unsupported format type: {format_type}")