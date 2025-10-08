"""Tests for yttranscript models."""

import pytest

from yttranscript.models import Video, TranscriptSegment, Transcript
from yttranscript.exceptions import InvalidUrlError


class TestVideo:
    """Test Video model."""
    
    def test_from_url_youtube_com_watch(self):
        """Test parsing standard YouTube watch URL."""
        url = "https://youtube.com/watch?v=dQw4w9WgXcQ"
        video = Video.from_url(url)
        assert video.video_id == "dQw4w9WgXcQ"
        assert video.url == url
    
    def test_from_url_youtube_com_with_www(self):
        """Test parsing YouTube URL with www."""
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        video = Video.from_url(url)
        assert video.video_id == "dQw4w9WgXcQ"
        assert video.url == url
    
    def test_from_url_youtube_com_with_extra_params(self):
        """Test parsing YouTube URL with additional parameters."""
        url = "https://youtube.com/watch?v=dQw4w9WgXcQ&t=30s&list=PLx"
        video = Video.from_url(url)
        assert video.video_id == "dQw4w9WgXcQ"
        assert video.url == url
    
    def test_from_url_youtu_be(self):
        """Test parsing YouTube short URL."""
        url = "https://youtu.be/dQw4w9WgXcQ"
        video = Video.from_url(url)
        assert video.video_id == "dQw4w9WgXcQ"
        assert video.url == url
    
    def test_from_url_youtu_be_with_params(self):
        """Test parsing YouTube short URL with parameters."""
        url = "https://youtu.be/dQw4w9WgXcQ?t=30"
        video = Video.from_url(url)
        assert video.video_id == "dQw4w9WgXcQ"
        assert video.url == url
    
    def test_from_url_embed_format(self):
        """Test parsing YouTube embed URL."""
        url = "https://youtube.com/embed/dQw4w9WgXcQ"
        video = Video.from_url(url)
        assert video.video_id == "dQw4w9WgXcQ"
        assert video.url == url
    
    def test_from_url_embed_with_params(self):
        """Test parsing YouTube embed URL with parameters."""
        url = "https://youtube.com/embed/dQw4w9WgXcQ?start=30"
        video = Video.from_url(url)
        assert video.video_id == "dQw4w9WgXcQ"
        assert video.url == url
    
    def test_from_url_bare_video_id(self):
        """Test parsing bare 11-character video ID."""
        video_id = "dQw4w9WgXcQ"
        video = Video.from_url(video_id)
        assert video.video_id == video_id
        assert video.url == f"https://youtube.com/watch?v={video_id}"
    
    def test_from_url_bare_video_id_with_special_chars(self):
        """Test parsing bare video ID with special characters."""
        video_id = "dQw4w9WgX-Q"  # Contains hyphen
        video = Video.from_url(video_id)
        assert video.video_id == video_id
        assert video.url == f"https://youtube.com/watch?v={video_id}"
    
    def test_from_url_invalid_domain(self):
        """Test invalid domain raises exception."""
        with pytest.raises(InvalidUrlError, match="Invalid YouTube URL format"):
            Video.from_url("https://vimeo.com/123456789")
    
    def test_from_url_no_video_id(self):
        """Test URL without video ID raises exception."""
        with pytest.raises(InvalidUrlError, match="Could not extract valid video ID"):
            Video.from_url("https://youtube.com/watch")
    
    def test_from_url_invalid_video_id_length(self):
        """Test invalid video ID length raises exception."""
        with pytest.raises(InvalidUrlError, match="Could not extract valid video ID"):
            Video.from_url("https://youtube.com/watch?v=short")
    
    def test_from_url_bare_id_wrong_length(self):
        """Test bare ID with wrong length raises exception."""
        with pytest.raises(InvalidUrlError):
            Video.from_url("shortid")
    
    def test_str_representation(self):
        """Test string representation of Video."""
        video = Video(video_id="dQw4w9WgXcQ", url="https://youtube.com/watch?v=dQw4w9WgXcQ")
        assert str(video) == "Video(dQw4w9WgXcQ)"


class TestTranscriptSegment:
    """Test TranscriptSegment model."""
    
    def test_segment_creation(self):
        """Test creating a transcript segment."""
        segment = TranscriptSegment(text="Hello world", start=0.0, duration=2.5)
        assert segment.text == "Hello world"
        assert segment.start == 0.0
        assert segment.duration == 2.5
    
    def test_segment_end_property(self):
        """Test end time calculation."""
        segment = TranscriptSegment(text="Hello", start=10.0, duration=2.5)
        assert segment.end == 12.5
    
    def test_segment_end_property_no_duration(self):
        """Test end time when duration is None."""
        segment = TranscriptSegment(text="Hello", start=10.0)
        assert segment.end is None
    
    def test_segment_end_property_no_start(self):
        """Test end time when start is None."""
        segment = TranscriptSegment(text="Hello", duration=2.5)
        assert segment.end is None
    
    def test_format_timestamp(self):
        """Test timestamp formatting."""
        segment = TranscriptSegment(text="Hello", start=3665.0)  # 1h 1m 5s
        assert segment.format_timestamp() == "[01:01:05]"
    
    def test_format_timestamp_no_start(self):
        """Test timestamp formatting when start is None."""
        segment = TranscriptSegment(text="Hello")
        assert segment.format_timestamp() == ""
    
    def test_format_timestamp_zero(self):
        """Test timestamp formatting at zero."""
        segment = TranscriptSegment(text="Hello", start=0.0)
        assert segment.format_timestamp() == "[00:00:00]"
    
    def test_format_timestamp_rounding(self):
        """Test timestamp formatting with fractional seconds."""
        segment = TranscriptSegment(text="Hello", start=65.7)  # Should round down
        assert segment.format_timestamp() == "[00:01:05]"


class TestTranscript:
    """Test Transcript model."""
    
    def test_transcript_creation(self):
        """Test creating a transcript."""
        segments = [
            TranscriptSegment(text="Hello", start=0.0, duration=1.0),
            TranscriptSegment(text="World", start=1.0, duration=1.0),
        ]
        transcript = Transcript(
            video_id="dQw4w9WgXcQ",
            language_code="en",
            segments=segments
        )
        assert transcript.video_id == "dQw4w9WgXcQ"
        assert transcript.language_code == "en"
        assert len(transcript.segments) == 2
    
    def test_transcript_full_text(self):
        """Test full text property."""
        segments = [
            TranscriptSegment(text="Hello"),
            TranscriptSegment(text="World"),
        ]
        transcript = Transcript(
            video_id="test",
            language_code="en",
            segments=segments
        )
        assert transcript.full_text == "Hello World"
    
    def test_transcript_length(self):
        """Test transcript length."""
        segments = [
            TranscriptSegment(text="One"),
            TranscriptSegment(text="Two"),
            TranscriptSegment(text="Three"),
        ]
        transcript = Transcript(
            video_id="test",
            language_code="en",
            segments=segments
        )
        assert len(transcript) == 3
    
    def test_total_duration(self):
        """Test total duration calculation."""
        segments = [
            TranscriptSegment(text="Hello", start=0.0, duration=1.0),
            TranscriptSegment(text="World", start=1.0, duration=2.0),
        ]
        transcript = Transcript(
            video_id="test",
            language_code="en",
            segments=segments
        )
        assert transcript.total_duration == 3.0
    
    def test_total_duration_no_timing(self):
        """Test total duration when timing info is missing."""
        segments = [
            TranscriptSegment(text="Hello"),
            TranscriptSegment(text="World"),
        ]
        transcript = Transcript(
            video_id="test",
            language_code="en",
            segments=segments
        )
        assert transcript.total_duration is None