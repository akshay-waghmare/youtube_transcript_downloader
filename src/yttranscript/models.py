"""Data models for yttranscript."""

from dataclasses import dataclass
from typing import List, Optional
from urllib.parse import urlparse, parse_qs

from .exceptions import InvalidUrlError


@dataclass
class Video:
    """YouTube video with transcript metadata."""
    
    video_id: str
    url: str
    title: Optional[str] = None
    duration: Optional[int] = None  # seconds
    available_languages: Optional[List[str]] = None
    
    @classmethod
    def from_url(cls, url: str) -> 'Video':
        """Extract video ID from YouTube URL or bare video ID."""
        # Handle bare video ID (11 characters, alphanumeric)
        if len(url) == 11 and url.replace('-', '').replace('_', '').isalnum():
            return cls(video_id=url, url=f"https://youtube.com/watch?v={url}")
            
        parsed = urlparse(url)
        video_id = None
        
        if 'youtube.com' in parsed.netloc:
            # Handle various YouTube URL formats
            if parsed.path == "/watch":
                video_id = parse_qs(parsed.query).get('v', [None])[0]
            elif parsed.path.startswith("/embed/"):
                video_id = parsed.path.split("/embed/")[1].split("?")[0]
        elif 'youtu.be' in parsed.netloc:
            video_id = parsed.path.lstrip('/')
            if '?' in video_id:
                video_id = video_id.split('?')[0]
        else:
            raise InvalidUrlError(f"Invalid YouTube URL format: {url}")
            
        if not video_id or len(video_id) != 11:
            raise InvalidUrlError(f"Could not extract valid video ID from: {url}")
            
        return cls(video_id=video_id, url=url)
    
    def __str__(self) -> str:
        return f"Video({self.video_id})"


@dataclass
class TranscriptSegment:
    """Single segment of transcript content."""
    
    text: str
    start: Optional[float] = None  # seconds from video start
    duration: Optional[float] = None  # segment duration in seconds
    
    @property
    def end(self) -> Optional[float]:
        """Calculate end time if start and duration available."""
        if self.start is not None and self.duration is not None:
            return self.start + self.duration
        return None
    
    def format_timestamp(self) -> str:
        """Format start time as [HH:MM:SS]."""
        if self.start is None:
            return ""
        
        hours = int(self.start // 3600)
        minutes = int((self.start % 3600) // 60)
        seconds = int(self.start % 60)
        
        return f"[{hours:02d}:{minutes:02d}:{seconds:02d}]"


@dataclass
class Transcript:
    """Complete transcript for a video."""
    
    video_id: str
    language_code: str
    segments: List[TranscriptSegment]
    is_generated: bool = False  # auto-generated vs manual
    is_translatable: bool = False
    
    @property
    def total_duration(self) -> Optional[float]:
        """Calculate total transcript duration."""
        if not self.segments or not self.segments[-1].end:
            return None
        return self.segments[-1].end
    
    @property
    def full_text(self) -> str:
        """Get complete transcript text without timestamps."""
        return " ".join(segment.text for segment in self.segments)
    
    def __len__(self) -> int:
        return len(self.segments)