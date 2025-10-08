# Data Model: yttranscript CLI Tool

**Date**: 2025-01-23  
**Context**: Data structures and entity definitions

## Core Entities

### Video

Represents a YouTube video with transcript capabilities.

```python
from dataclasses import dataclass
from typing import List, Optional
from urllib.parse import urlparse, parse_qs

@dataclass
class Video:
    """YouTube video with transcript metadata."""
    
    video_id: str
    url: str
    title: Optional[str] = None
    duration: Optional[int] = None  # seconds
    available_languages: List[str] = None
    
    @classmethod
    def from_url(cls, url: str) -> 'Video':
        """Extract video ID from YouTube URL."""
        parsed = urlparse(url)
        
        if 'youtube.com' in parsed.netloc:
            video_id = parse_qs(parsed.query).get('v', [None])[0]
        elif 'youtu.be' in parsed.netloc:
            video_id = parsed.path.lstrip('/')
        else:
            raise ValueError(f"Invalid YouTube URL: {url}")
            
        if not video_id:
            raise ValueError(f"Could not extract video ID from: {url}")
            
        return cls(video_id=video_id, url=url)
    
    def __str__(self) -> str:
        return f"Video({self.video_id})"
```

### TranscriptSegment

Individual segment of transcript with optional timestamp.

```python
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
```

### Transcript

Complete transcript with metadata and segments.

```python
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
```

### OutputFormat

Configuration for different output formats.

```python
from enum import Enum
from typing import Protocol

class FormatType(Enum):
    """Supported output formats."""
    PLAIN = "plain"
    MARKDOWN = "markdown"

class Formatter(Protocol):
    """Interface for transcript formatters."""
    
    def format(self, transcript: Transcript, include_timestamps: bool = False) -> str:
        """Format transcript according to this formatter's rules."""
        ...

class PlainFormatter:
    """Plain text formatter."""
    
    def format(self, transcript: Transcript, include_timestamps: bool = False) -> str:
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
        lines = []
        for segment in transcript.segments:
            line = "- "
            if include_timestamps and segment.start is not None:
                line += f"**{segment.format_timestamp()}** "
            line += segment.text
            lines.append(line)
        return "\n".join(lines)
```

### CliOptions

Command-line interface configuration.

```python
@dataclass
class CliOptions:
    """Configuration from command-line arguments."""
    
    url: str
    format: FormatType = FormatType.PLAIN
    output_file: Optional[str] = None
    language: Optional[str] = None
    include_timestamps: bool = False
    list_languages: bool = False
    
    def validate(self) -> None:
        """Validate option combinations."""
        if self.list_languages and any([
            self.output_file,
            self.include_timestamps,
            self.format != FormatType.PLAIN
        ]):
            raise ValueError("--list-languages cannot be used with other output options")
```

## Error Handling

### Custom Exceptions

```python
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
```

## Data Flow

### Extraction Pipeline

```
URL Input → Video.from_url() → YouTubeTranscriptApi.get_transcript() 
→ [TranscriptSegment] → Transcript → Formatter.format() → Output
```

### Language Discovery Pipeline

```
URL Input → Video.from_url() → YouTubeTranscriptApi.list_transcripts()
→ [Language Info] → Display Available Languages
```

## Memory Considerations

### Streaming Design

For large transcripts (10+ hour videos):
- Process segments incrementally
- Write output as segments are formatted
- Avoid loading entire transcript into memory

```python
def stream_format(transcript_segments: Iterator[TranscriptSegment], 
                 formatter: Formatter, 
                 output_file: TextIO) -> None:
    """Stream format large transcripts to avoid memory issues."""
    for segment in transcript_segments:
        formatted_line = formatter.format_segment(segment)
        output_file.write(formatted_line + "\n")
```

## Validation Rules

### URL Validation
- Must be valid YouTube URL (youtube.com/watch?v= or youtu.be/)
- Video ID must be 11 characters alphanumeric
- Handle URL variants (with/without www, with additional parameters)

### Language Code Validation  
- Must match available languages from YouTube
- Use ISO 639-1 language codes where possible
- Provide helpful error messages for invalid codes

### File Output Validation
- Check write permissions before processing
- Handle existing file conflicts
- Validate file path format across platforms

## Testing Data Structures

### Mock Responses

```python
# Test transcript data
MOCK_TRANSCRIPT_SEGMENTS = [
    {'text': 'Hello world', 'start': 0.0, 'duration': 2.5},
    {'text': 'This is a test', 'start': 2.5, 'duration': 3.0},
    {'text': 'Goodbye', 'start': 5.5, 'duration': 1.5}
]

# Test video IDs (public videos for integration tests)
TEST_VIDEO_IDS = {
    'english_only': 'dQw4w9WgXcQ',  # Never Gonna Give You Up
    'multilingual': 'ABC123DEF456',  # Video with multiple languages
    'no_transcript': 'XYZ789ABC123'  # Video without transcripts
}
```

This data model provides a clean separation of concerns, strong typing, and extensible design for future enhancements while maintaining simplicity aligned with the constitutional minimalism principle.