"""Core transcript extraction logic."""

import time
import random
from typing import List, Optional, Dict, Any

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
    YouTubeRequestFailed,
    RequestBlocked,
)

from .models import Video, Transcript, TranscriptSegment
from .exceptions import (
    TranscriptNotAvailableError,
    LanguageNotFoundError,
    NetworkError,
)


class TranscriptExtractor:
    """Extracts transcripts from YouTube videos."""
    
    def __init__(self, max_retries: int = 3):
        """Initialize extractor with retry configuration.
        
        Args:
            max_retries: Maximum number of retry attempts for network operations
        """
        self.max_retries = max_retries
        self.api = YouTubeTranscriptApi()
    
    def extract_transcript(
        self, 
        video_id: str, 
        language: Optional[str] = None
    ) -> Transcript:
        """Extract transcript for a video.
        
        Args:
            video_id: YouTube video ID
            language: Preferred language code (defaults to English, then first available)
            
        Returns:
            Transcript object with segments
            
        Raises:
            TranscriptNotAvailableError: No transcript available
            LanguageNotFoundError: Requested language not found
            NetworkError: Network operation failed
        """
        try:
            transcript_list = self._fetch_with_retry(
                lambda: self.api.list(video_id)
            )
            
            if language:
                # Try to find the specific language
                transcript = transcript_list.find_transcript([language])
                transcript_data = transcript.fetch()
                return self._build_transcript(video_id, language, transcript_data)
            else:
                # Try English first, then any available language
                try:
                    transcript = transcript_list.find_transcript(['en'])
                    transcript_data = transcript.fetch()
                    return self._build_transcript(video_id, 'en', transcript_data)
                except NoTranscriptFound:
                    # Fallback to first available language
                    if transcript_list:
                        first_transcript = list(transcript_list)[0]
                        transcript_data = first_transcript.fetch()
                        return self._build_transcript(video_id, first_transcript.language_code, transcript_data)
                    else:
                        raise TranscriptNotAvailableError(f"No transcripts available for video {video_id}")
                    
        except TranscriptsDisabled:
            raise TranscriptNotAvailableError(
                f"Transcripts are disabled for video {video_id}. "
                f"The video may be private or have transcripts turned off."
            )
        except NoTranscriptFound:
            if language:
                raise LanguageNotFoundError(
                    f"No transcript found for language '{language}' in video {video_id}. "
                    f"Use --list-languages to see available options."
                )
            else:
                raise TranscriptNotAvailableError(
                    f"No transcript available for video {video_id}. "
                    f"The video may not have transcripts or may be private."
                )
        except VideoUnavailable:
            raise TranscriptNotAvailableError(
                f"Video {video_id} is unavailable. "
                f"It may be private, deleted, or region-restricted."
            )
        except YouTubeRequestFailed as e:
            raise NetworkError(
                f"YouTube request failed. Please wait and try again later. "
                f"Original error: {str(e)}"
            )
        except RequestBlocked as e:
            raise NetworkError(
                f"Request blocked by YouTube. Please wait and try again later. "
                f"Original error: {str(e)}"
            )
        except Exception as e:
            raise NetworkError(f"Network error occurred: {str(e)}")
    
    def list_available_languages(self, video_id: str) -> List[Dict[str, str]]:
        """List all available transcript languages for a video.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            List of language dictionaries with 'language' and 'language_code' keys
            
        Raises:
            TranscriptNotAvailableError: No transcripts available
            NetworkError: Network operation failed
        """
        try:
            transcript_list = self._fetch_with_retry(
                lambda: self.api.list(video_id)
            )
            
            languages = []
            for transcript in transcript_list:
                languages.append({
                    'language_code': transcript.language_code,
                    'language': transcript.language,
                    'is_generated': transcript.is_generated,
                    'is_translatable': bool(transcript.translation_languages),
                })
            
            return languages
            
        except TranscriptsDisabled:
            raise TranscriptNotAvailableError(
                f"Transcripts are disabled for video {video_id}"
            )
        except VideoUnavailable:
            raise TranscriptNotAvailableError(
                f"Video {video_id} is unavailable"
            )
        except Exception as e:
            raise NetworkError(f"Failed to list languages: {str(e)}")
    
    def _fetch_with_retry(self, fetch_func) -> Any:
        """Execute fetch function with exponential backoff retry logic.
        
        Args:
            fetch_func: Function to call for fetching data
            
        Returns:
            Result from fetch_func
            
        Raises:
            Various exceptions from fetch_func after retry exhaustion
        """
        last_exception = None
        
        for attempt in range(self.max_retries):
            try:
                return fetch_func()
            except (YouTubeRequestFailed, RequestBlocked) as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    # Exponential backoff with jitter
                    delay = (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(delay)
                    continue
                raise
            except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable):
                # Don't retry these - they won't succeed
                raise
            except Exception as e:
                last_exception = e
                if attempt < self.max_retries - 1:
                    # Exponential backoff with jitter for network errors
                    delay = (2 ** attempt) + random.uniform(0, 1)
                    time.sleep(delay)
                    continue
                raise
        
        # This should not be reached, but just in case
        raise last_exception
    
    def _detect_language(self, video_id: str) -> str:
        """Detect the actual language code from transcript list.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Language code of first available transcript
        """
        try:
            transcript_list = self.api.list(video_id)
            for transcript in transcript_list:
                return transcript.language_code
        except Exception:
            pass
        return 'unknown'
    
    def _build_transcript(
        self, 
        video_id: str, 
        language_code: str, 
        transcript_data: List[Any]
    ) -> Transcript:
        """Build Transcript object from raw transcript data.
        
        Args:
            video_id: YouTube video ID
            language_code: Language code of the transcript
            transcript_data: Raw transcript data from API
            
        Returns:
            Transcript object with segments
        """
        segments = []
        for item in transcript_data:
            # Handle both dict format (old API) and object format (new API)
            if hasattr(item, 'text'):
                # New API format with attributes
                segment = TranscriptSegment(
                    text=item.text.strip(),
                    start=getattr(item, 'start', None),
                    duration=getattr(item, 'duration', None)
                )
            else:
                # Old API format with dict
                segment = TranscriptSegment(
                    text=item['text'].strip(),
                    start=item.get('start'),
                    duration=item.get('duration')
                )
            segments.append(segment)
        
        return Transcript(
            video_id=video_id,
            language_code=language_code,
            segments=segments
        )