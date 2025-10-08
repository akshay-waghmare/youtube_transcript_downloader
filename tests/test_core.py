"""Tests for yttranscript core functionality."""

import pytest
from unittest.mock import Mock, patch
import time

from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
    YouTubeRequestFailed,
    RequestBlocked,
)

from yttranscript.core import TranscriptExtractor
from yttranscript.models import Transcript, TranscriptSegment
from yttranscript.exceptions import (
    TranscriptNotAvailableError,
    LanguageNotFoundError,
    NetworkError,
)


@pytest.fixture
def mock_transcript_data():
    """Mock transcript data from YouTube API."""
    return [
        {'text': 'Hello world', 'start': 0.0, 'duration': 2.5},
        {'text': 'This is a test', 'start': 2.5, 'duration': 3.0},
        {'text': 'Goodbye', 'start': 5.5, 'duration': 1.5},
    ]


@pytest.fixture
def mock_language_data():
    """Mock language data from YouTube API."""
    mock_transcript = Mock()
    mock_transcript.language_code = 'en'
    mock_transcript.language = 'English'
    mock_transcript.is_generated = False
    mock_transcript.is_translatable = True
    return [mock_transcript]


class TestTranscriptExtractor:
    """Test TranscriptExtractor class."""
    
    def test_init_default_retries(self):
        """Test extractor initialization with default retries."""
        extractor = TranscriptExtractor()
        assert extractor.max_retries == 3
    
    def test_init_custom_retries(self):
        """Test extractor initialization with custom retries."""
        extractor = TranscriptExtractor(max_retries=5)
        assert extractor.max_retries == 5
    
    @patch('yttranscript.core.YouTubeTranscriptApi.get_transcript')
    def test_extract_transcript_success_english(self, mock_get_transcript, mock_transcript_data):
        """Test successful transcript extraction in English."""
        mock_get_transcript.return_value = mock_transcript_data
        
        extractor = TranscriptExtractor()
        transcript = extractor.extract_transcript('test123')
        
        assert isinstance(transcript, Transcript)
        assert transcript.video_id == 'test123'
        assert transcript.language_code == 'en'
        assert len(transcript.segments) == 3
        assert transcript.segments[0].text == 'Hello world'
        mock_get_transcript.assert_called_once_with('test123', languages=['en'])
    
    @patch('yttranscript.core.YouTubeTranscriptApi.get_transcript')
    def test_extract_transcript_specific_language(self, mock_get_transcript, mock_transcript_data):
        """Test transcript extraction with specific language."""
        mock_get_transcript.return_value = mock_transcript_data
        
        extractor = TranscriptExtractor()
        transcript = extractor.extract_transcript('test123', language='es')
        
        assert transcript.language_code == 'es'
        mock_get_transcript.assert_called_once_with('test123', languages=['es'])
    
    @patch('yttranscript.core.YouTubeTranscriptApi.get_transcript')
    @patch('yttranscript.core.TranscriptExtractor._detect_language')
    def test_extract_transcript_fallback_language(self, mock_detect_lang, mock_get_transcript, mock_transcript_data):
        """Test transcript extraction with fallback to first available language."""
        # First call (English) fails, second call (any language) succeeds
        mock_get_transcript.side_effect = [NoTranscriptFound('test'), mock_transcript_data]
        mock_detect_lang.return_value = 'fr'
        
        extractor = TranscriptExtractor()
        transcript = extractor.extract_transcript('test123')
        
        assert transcript.language_code == 'fr'
        assert mock_get_transcript.call_count == 2
    
    @patch('yttranscript.core.YouTubeTranscriptApi.get_transcript')
    def test_extract_transcript_disabled(self, mock_get_transcript):
        """Test handling of disabled transcripts."""
        mock_get_transcript.side_effect = TranscriptsDisabled('test')
        
        extractor = TranscriptExtractor()
        with pytest.raises(TranscriptNotAvailableError, match="disabled"):
            extractor.extract_transcript('test123')
    
    @patch('yttranscript.core.YouTubeTranscriptApi.get_transcript')
    def test_extract_transcript_not_found_specific_language(self, mock_get_transcript):
        """Test handling of language not found."""
        mock_get_transcript.side_effect = NoTranscriptFound('test')
        
        extractor = TranscriptExtractor()
        with pytest.raises(LanguageNotFoundError, match="No transcript found for language 'es'"):
            extractor.extract_transcript('test123', language='es')
    
    @patch('yttranscript.core.YouTubeTranscriptApi.get_transcript')
    def test_extract_transcript_video_unavailable(self, mock_get_transcript):
        """Test handling of unavailable video."""
        mock_get_transcript.side_effect = VideoUnavailable('test')
        
        extractor = TranscriptExtractor()
        with pytest.raises(TranscriptNotAvailableError, match="unavailable"):
            extractor.extract_transcript('test123')
    
    @patch('yttranscript.core.YouTubeTranscriptApi.get_transcript')
    def test_extract_transcript_rate_limited(self, mock_get_transcript):
        """Test handling of rate limiting."""
        mock_get_transcript.side_effect = YouTubeRequestFailed('test')
        
        extractor = TranscriptExtractor()
        with pytest.raises(NetworkError, match="YouTube request failed"):
            extractor.extract_transcript('test123')
    
    @patch('yttranscript.core.YouTubeTranscriptApi.list_transcripts')
    def test_list_available_languages_success(self, mock_list_transcripts, mock_language_data):
        """Test successful language listing."""
        mock_list_transcripts.return_value = mock_language_data
        
        extractor = TranscriptExtractor()
        languages = extractor.list_available_languages('test123')
        
        assert len(languages) == 1
        assert languages[0]['language_code'] == 'en'
        assert languages[0]['language'] == 'English'
        assert languages[0]['is_generated'] is False
        assert languages[0]['is_translatable'] is True
    
    @patch('yttranscript.core.YouTubeTranscriptApi.list_transcripts')
    def test_list_available_languages_disabled(self, mock_list_transcripts):
        """Test language listing with disabled transcripts."""
        mock_list_transcripts.side_effect = TranscriptsDisabled('test')
        
        extractor = TranscriptExtractor()
        with pytest.raises(TranscriptNotAvailableError, match="disabled"):
            extractor.list_available_languages('test123')
    
    @patch('yttranscript.core.YouTubeTranscriptApi.list_transcripts')
    def test_list_available_languages_unavailable_video(self, mock_list_transcripts):
        """Test language listing with unavailable video."""
        mock_list_transcripts.side_effect = VideoUnavailable('test')
        
        extractor = TranscriptExtractor()
        with pytest.raises(TranscriptNotAvailableError, match="unavailable"):
            extractor.list_available_languages('test123')
    
    @patch('time.sleep')
    @patch('yttranscript.core.YouTubeTranscriptApi.get_transcript')
    def test_retry_logic_success_after_failure(self, mock_get_transcript, mock_sleep, mock_transcript_data):
        """Test retry logic succeeds after initial failures."""
        # Fail twice, then succeed
        mock_get_transcript.side_effect = [
            YouTubeRequestFailed('test'),
            YouTubeRequestFailed('test'), 
            mock_transcript_data
        ]
        
        extractor = TranscriptExtractor(max_retries=3)
        transcript = extractor.extract_transcript('test123')
        
        assert isinstance(transcript, Transcript)
        assert mock_get_transcript.call_count == 3
        assert mock_sleep.call_count == 2  # Two retries
    
    @patch('time.sleep')
    @patch('yttranscript.core.YouTubeTranscriptApi.get_transcript')
    def test_retry_logic_exhausted(self, mock_get_transcript, mock_sleep):
        """Test retry logic exhausted after max attempts."""
        mock_get_transcript.side_effect = YouTubeRequestFailed('test')
        
        extractor = TranscriptExtractor(max_retries=2)
        with pytest.raises(NetworkError):
            extractor.extract_transcript('test123')
        
        assert mock_get_transcript.call_count == 2
        assert mock_sleep.call_count == 1  # One retry
    
    @patch('yttranscript.core.YouTubeTranscriptApi.get_transcript')
    def test_retry_logic_no_retry_for_permanent_errors(self, mock_get_transcript):
        """Test that permanent errors are not retried."""
        mock_get_transcript.side_effect = TranscriptsDisabled('test')
        
        extractor = TranscriptExtractor(max_retries=3)
        with pytest.raises(TranscriptNotAvailableError):
            extractor.extract_transcript('test123')
        
        # Should not retry for permanent errors
        assert mock_get_transcript.call_count == 1
    
    @patch('yttranscript.core.YouTubeTranscriptApi.list_transcripts')
    def test_detect_language(self, mock_list_transcripts, mock_language_data):
        """Test language detection from transcript list."""
        mock_list_transcripts.return_value = mock_language_data
        
        extractor = TranscriptExtractor()
        lang_code = extractor._detect_language('test123')
        
        assert lang_code == 'en'
    
    @patch('yttranscript.core.YouTubeTranscriptApi.list_transcripts')
    def test_detect_language_error(self, mock_list_transcripts):
        """Test language detection handles errors gracefully."""
        mock_list_transcripts.side_effect = Exception('test error')
        
        extractor = TranscriptExtractor()
        lang_code = extractor._detect_language('test123')
        
        assert lang_code == 'unknown'
    
    def test_build_transcript(self, mock_transcript_data):
        """Test building transcript from raw data."""
        extractor = TranscriptExtractor()
        transcript = extractor._build_transcript('test123', 'en', mock_transcript_data)
        
        assert isinstance(transcript, Transcript)
        assert transcript.video_id == 'test123'
        assert transcript.language_code == 'en'
        assert len(transcript.segments) == 3
        
        # Check first segment
        segment = transcript.segments[0]
        assert segment.text == 'Hello world'
        assert segment.start == 0.0
        assert segment.duration == 2.5