"""Tests for yttranscript formatters."""

import pytest

from yttranscript.formatters import (
    PlainFormatter, 
    MarkdownFormatter, 
    FormatType, 
    get_formatter
)
from yttranscript.models import Transcript, TranscriptSegment


@pytest.fixture
def sample_transcript():
    """Create a sample transcript for testing."""
    segments = [
        TranscriptSegment(text="Hello world", start=0.0, duration=2.5),
        TranscriptSegment(text="This is a test", start=2.5, duration=3.0),
        TranscriptSegment(text="Goodbye", start=5.5, duration=1.5),
    ]
    return Transcript(
        video_id="test123",
        language_code="en",
        segments=segments
    )


@pytest.fixture
def transcript_no_timing():
    """Create a transcript without timing information."""
    segments = [
        TranscriptSegment(text="Hello world"),
        TranscriptSegment(text="This is a test"),
        TranscriptSegment(text="Goodbye"),
    ]
    return Transcript(
        video_id="test123",
        language_code="en",
        segments=segments
    )


class TestPlainFormatter:
    """Test PlainFormatter."""
    
    def test_format_without_timestamps(self, sample_transcript):
        """Test plain formatting without timestamps."""
        formatter = PlainFormatter()
        result = formatter.format(sample_transcript, include_timestamps=False)
        
        expected = "Hello world\nThis is a test\nGoodbye"
        assert result == expected
    
    def test_format_with_timestamps(self, sample_transcript):
        """Test plain formatting with timestamps."""
        formatter = PlainFormatter()
        result = formatter.format(sample_transcript, include_timestamps=True)
        
        expected = "[00:00:00] Hello world\n[00:00:02] This is a test\n[00:00:05] Goodbye"
        assert result == expected
    
    def test_format_no_timing_info(self, transcript_no_timing):
        """Test plain formatting when segments have no timing."""
        formatter = PlainFormatter()
        result = formatter.format(transcript_no_timing, include_timestamps=True)
        
        expected = "Hello world\nThis is a test\nGoodbye"
        assert result == expected
    
    def test_format_empty_transcript(self):
        """Test formatting empty transcript."""
        empty_transcript = Transcript(
            video_id="empty",
            language_code="en",
            segments=[]
        )
        formatter = PlainFormatter()
        result = formatter.format(empty_transcript)
        assert result == ""


class TestMarkdownFormatter:
    """Test MarkdownFormatter."""
    
    def test_format_without_timestamps(self, sample_transcript):
        """Test markdown formatting without timestamps."""
        formatter = MarkdownFormatter()
        result = formatter.format(sample_transcript, include_timestamps=False)
        
        expected = "- Hello world\n- This is a test\n- Goodbye"
        assert result == expected
    
    def test_format_with_timestamps(self, sample_transcript):
        """Test markdown formatting with timestamps."""
        formatter = MarkdownFormatter()
        result = formatter.format(sample_transcript, include_timestamps=True)
        
        expected = "- **[00:00:00]** Hello world\n- **[00:00:02]** This is a test\n- **[00:00:05]** Goodbye"
        assert result == expected
    
    def test_format_no_timing_info(self, transcript_no_timing):
        """Test markdown formatting when segments have no timing."""
        formatter = MarkdownFormatter()
        result = formatter.format(transcript_no_timing, include_timestamps=True)
        
        expected = "- Hello world\n- This is a test\n- Goodbye"
        assert result == expected
    
    def test_format_empty_transcript(self):
        """Test formatting empty transcript."""
        empty_transcript = Transcript(
            video_id="empty",
            language_code="en",
            segments=[]
        )
        formatter = MarkdownFormatter()
        result = formatter.format(empty_transcript)
        assert result == ""


class TestGetFormatter:
    """Test get_formatter function."""
    
    def test_get_plain_formatter(self):
        """Test getting plain formatter."""
        formatter = get_formatter(FormatType.PLAIN)
        assert isinstance(formatter, PlainFormatter)
    
    def test_get_markdown_formatter(self):
        """Test getting markdown formatter."""
        formatter = get_formatter(FormatType.MARKDOWN)
        assert isinstance(formatter, MarkdownFormatter)
    
    def test_get_json_formatter_not_implemented(self):
        """Test that JSON formatter raises not implemented error."""
        with pytest.raises(ValueError, match="JSON format is not yet implemented"):
            get_formatter(FormatType.JSON)
    
    def test_invalid_format_type(self):
        """Test handling of invalid format type."""
        # This would only happen if we bypass the enum
        class InvalidFormat:
            pass
        
        with pytest.raises(ValueError, match="Unsupported format type"):
            get_formatter(InvalidFormat())


class TestFormatType:
    """Test FormatType enum."""
    
    def test_format_type_values(self):
        """Test format type enum values."""
        assert FormatType.PLAIN.value == "plain"
        assert FormatType.MARKDOWN.value == "markdown"
        assert FormatType.JSON.value == "json"
    
    def test_format_type_from_string(self):
        """Test creating format type from string."""
        assert FormatType("plain") == FormatType.PLAIN
        assert FormatType("markdown") == FormatType.MARKDOWN
        assert FormatType("json") == FormatType.JSON
    
    def test_format_type_invalid_string(self):
        """Test invalid format type string."""
        with pytest.raises(ValueError):
            FormatType("invalid")