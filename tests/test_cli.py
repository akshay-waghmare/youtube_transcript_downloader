"""Tests for yttranscript CLI."""

import pytest
from click.testing import CliRunner
from unittest.mock import patch, Mock

from yttranscript.cli import main
from yttranscript.models import Transcript, TranscriptSegment
from yttranscript.exceptions import (
    InvalidUrlError,
    TranscriptNotAvailableError,
    LanguageNotFoundError,
    NetworkError,
)


@pytest.fixture
def runner():
    """Create CLI test runner."""
    return CliRunner()


@pytest.fixture
def sample_transcript():
    """Create sample transcript for testing."""
    segments = [
        TranscriptSegment(text="Hello world", start=0.0, duration=2.5),
        TranscriptSegment(text="This is a test", start=2.5, duration=3.0),
    ]
    return Transcript(
        video_id="dQw4w9WgXcQ",
        language_code="en",
        segments=segments
    )


class TestCLIBasic:
    """Test basic CLI functionality."""
    
    def test_help_option(self, runner):
        """Test --help option."""
        result = runner.invoke(main, ['--help'])
        assert result.exit_code == 0
        assert 'Extract transcript from YouTube video' in result.output
        assert 'Usage:' in result.output
    
    def test_version_option(self, runner):
        """Test --version option."""
        result = runner.invoke(main, ['--version'])
        assert result.exit_code == 0
        assert '0.1.0' in result.output
    
    def test_no_url_argument(self, runner):
        """Test CLI without URL argument."""
        result = runner.invoke(main, [])
        assert result.exit_code == 2  # Click error for missing argument
        assert 'Usage:' in result.output


class TestCLIURLValidation:
    """Test URL validation in CLI."""
    
    def test_invalid_url(self, runner):
        """Test invalid URL handling."""
        result = runner.invoke(main, ['https://vimeo.com/123456'])
        assert result.exit_code == 1
        assert 'Error:' in result.output
        assert 'Invalid YouTube URL format' in result.output
    
    def test_valid_youtube_url_format(self, runner):
        """Test that valid URL format passes validation."""
        with patch('yttranscript.cli.TranscriptExtractor') as mock_extractor:
            mock_instance = Mock()
            mock_extractor.return_value = mock_instance
            mock_instance.extract_transcript.side_effect = NetworkError("Test error for validation")
            
            result = runner.invoke(main, ['https://youtube.com/watch?v=dQw4w9WgXcQ'])
            assert result.exit_code == 2  # Network error, not URL validation error


class TestCLIListLanguages:
    """Test --list-languages functionality."""
    
    def test_list_languages_success(self, runner):
        """Test successful language listing."""
        mock_languages = [
            {'language_code': 'en', 'language': 'English', 'is_generated': False},
            {'language_code': 'es', 'language': 'Spanish', 'is_generated': True},
        ]
        
        with patch('yttranscript.cli.TranscriptExtractor') as mock_extractor:
            mock_instance = Mock()
            mock_extractor.return_value = mock_instance
            mock_instance.list_available_languages.return_value = mock_languages
            
            result = runner.invoke(main, ['dQw4w9WgXcQ', '--list-languages'])
            assert result.exit_code == 0
            assert 'Available languages:' in result.output
            assert 'en (English)' in result.output
            assert 'es (Spanish) (auto-generated)' in result.output
    
    def test_list_languages_with_conflicting_options(self, runner):
        """Test --list-languages with conflicting options."""
        result = runner.invoke(main, ['dQw4w9WgXcQ', '--list-languages', '--output', 'test.txt'])
        assert result.exit_code == 1
        assert 'cannot be used with other output options' in result.output
    
    def test_list_languages_no_languages_available(self, runner):
        """Test language listing when no languages available."""
        with patch('yttranscript.cli.TranscriptExtractor') as mock_extractor:
            mock_instance = Mock()
            mock_extractor.return_value = mock_instance
            mock_instance.list_available_languages.return_value = []
            
            result = runner.invoke(main, ['dQw4w9WgXcQ', '--list-languages'])
            assert result.exit_code == 1
            assert 'No transcript languages available' in result.output


class TestCLITranscriptExtraction:
    """Test transcript extraction via CLI."""
    
    def test_basic_extraction_stdout(self, runner, sample_transcript):
        """Test basic transcript extraction to stdout."""
        with patch('yttranscript.cli.TranscriptExtractor') as mock_extractor:
            mock_instance = Mock()
            mock_extractor.return_value = mock_instance
            mock_instance.extract_transcript.return_value = sample_transcript
            
            result = runner.invoke(main, ['dQw4w9WgXcQ'])
            assert result.exit_code == 0
            assert 'Hello world' in result.output
            assert 'This is a test' in result.output
    
    def test_markdown_format(self, runner, sample_transcript):
        """Test markdown format output."""
        with patch('yttranscript.cli.TranscriptExtractor') as mock_extractor:
            mock_instance = Mock()
            mock_extractor.return_value = mock_instance
            mock_instance.extract_transcript.return_value = sample_transcript
            
            result = runner.invoke(main, ['dQw4w9WgXcQ', '--format', 'markdown'])
            assert result.exit_code == 0
            assert '- Hello world' in result.output
            assert '- This is a test' in result.output
    
    def test_with_timestamps(self, runner, sample_transcript):
        """Test output with timestamps."""
        with patch('yttranscript.cli.TranscriptExtractor') as mock_extractor:
            mock_instance = Mock()
            mock_extractor.return_value = mock_instance
            mock_instance.extract_transcript.return_value = sample_transcript
            
            result = runner.invoke(main, ['dQw4w9WgXcQ', '--timestamps'])
            assert result.exit_code == 0
            assert '[00:00:00] Hello world' in result.output
            assert '[00:00:02] This is a test' in result.output


class TestCLIFileOutput:
    """Test file output functionality."""
    
    def test_file_output_success(self, runner, sample_transcript, tmp_path):
        """Test successful file output."""
        output_file = tmp_path / "transcript.txt"
        
        with patch('yttranscript.cli.TranscriptExtractor') as mock_extractor:
            mock_instance = Mock()
            mock_extractor.return_value = mock_instance
            mock_instance.extract_transcript.return_value = sample_transcript
            
            result = runner.invoke(main, ['dQw4w9WgXcQ', '--output', str(output_file)])
            assert result.exit_code == 0
            assert f"Transcript saved to '{output_file}'" in result.output
            
            # Check file contents
            content = output_file.read_text(encoding='utf-8')
            assert 'Hello world' in content
            assert 'This is a test' in content
    
    def test_file_overwrite_confirmation(self, runner, sample_transcript, tmp_path):
        """Test file overwrite confirmation."""
        output_file = tmp_path / "existing.txt"
        output_file.write_text("existing content")
        
        with patch('yttranscript.cli.TranscriptExtractor') as mock_extractor:
            mock_instance = Mock()
            mock_extractor.return_value = mock_instance
            mock_instance.extract_transcript.return_value = sample_transcript
            
            # Test declining overwrite
            result = runner.invoke(main, ['dQw4w9WgXcQ', '--output', str(output_file)], input='n\n')
            assert result.exit_code == 0
            assert 'Operation cancelled' in result.output
    
    def test_file_overwrite_force(self, runner, sample_transcript, tmp_path):
        """Test file overwrite with --force flag."""
        output_file = tmp_path / "existing.txt"
        output_file.write_text("existing content")
        
        with patch('yttranscript.cli.TranscriptExtractor') as mock_extractor:
            mock_instance = Mock()
            mock_extractor.return_value = mock_instance
            mock_instance.extract_transcript.return_value = sample_transcript
            
            result = runner.invoke(main, ['dQw4w9WgXcQ', '--output', str(output_file), '--force'])
            assert result.exit_code == 0
            assert f"Transcript saved to '{output_file}'" in result.output
            
            # Check file was overwritten
            content = output_file.read_text(encoding='utf-8')
            assert 'Hello world' in content
            assert 'existing content' not in content


class TestCLIErrorHandling:
    """Test CLI error handling."""
    
    def test_transcript_not_available(self, runner):
        """Test transcript not available error."""
        with patch('yttranscript.cli.TranscriptExtractor') as mock_extractor:
            mock_instance = Mock()
            mock_extractor.return_value = mock_instance
            mock_instance.extract_transcript.side_effect = TranscriptNotAvailableError("Test error")
            
            result = runner.invoke(main, ['dQw4w9WgXcQ'])
            assert result.exit_code == 2
            assert 'Error: Test error' in result.output
    
    def test_language_not_found(self, runner):
        """Test language not found error."""
        with patch('yttranscript.cli.TranscriptExtractor') as mock_extractor:
            mock_instance = Mock()
            mock_extractor.return_value = mock_instance
            mock_instance.extract_transcript.side_effect = LanguageNotFoundError("Language not found")
            
            result = runner.invoke(main, ['dQw4w9WgXcQ', '--language', 'xx'])
            assert result.exit_code == 3
            assert 'Error: Language not found' in result.output
    
    def test_network_error(self, runner):
        """Test network error handling."""
        with patch('yttranscript.cli.TranscriptExtractor') as mock_extractor:
            mock_instance = Mock()
            mock_extractor.return_value = mock_instance
            mock_instance.extract_transcript.side_effect = NetworkError("Network failed")
            
            result = runner.invoke(main, ['dQw4w9WgXcQ'])
            assert result.exit_code == 2
            assert 'Error: Network failed' in result.output


class TestCLILanguageOptions:
    """Test language-related CLI options."""
    
    def test_specific_language_request(self, runner, sample_transcript):
        """Test requesting specific language."""
        with patch('yttranscript.cli.TranscriptExtractor') as mock_extractor:
            mock_instance = Mock()
            mock_extractor.return_value = mock_instance
            mock_instance.extract_transcript.return_value = sample_transcript
            
            result = runner.invoke(main, ['dQw4w9WgXcQ', '--language', 'es'])
            assert result.exit_code == 0
            mock_instance.extract_transcript.assert_called_once_with('dQw4w9WgXcQ', 'es')