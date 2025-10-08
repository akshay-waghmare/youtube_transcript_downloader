
# yttranscript

A minimal Python CLI tool for extracting YouTube video transcripts.

## Features

- Extract transcripts from YouTube videos using video URLs or video IDs
- Support for multiple output formats (plain text, Markdown)
- Optional timestamp inclusion
- Multi-language transcript support
- File output with overwrite protection
- Cross-platform compatibility (Windows, macOS, Linux)
- No API key required

## Installation

### From PyPI (when published)

```bash
pip install yttranscript
```

### Using uvx (recommended for one-time usage)

```bash
uvx yttranscript https://youtube.com/watch?v=VIDEO_ID
```

### From Source

```bash
git clone https://github.com/akshay-waghmare/youtube_transcript_downloader.git
cd youtube_transcript_downloader
pip install -e .
```

## Usage

### Basic Usage

```bash
# Extract transcript from YouTube URL
yttranscript https://youtube.com/watch?v=dQw4w9WgXcQ

# Use just the video ID
yttranscript dQw4w9WgXcQ

# Output to file
yttranscript dQw4w9WgXcQ --output transcript.txt
```

### Output Formats

```bash
# Plain text (default)
yttranscript VIDEO_ID --format plain

# Markdown with bullet points
yttranscript VIDEO_ID --format markdown

# Include timestamps
yttranscript VIDEO_ID --timestamps
```

### Language Options

```bash
# List available languages
yttranscript VIDEO_ID --list-languages

# Extract specific language
yttranscript VIDEO_ID --language es

# Extract with Spanish transcript and timestamps in Markdown
yttranscript VIDEO_ID --language es --format markdown --timestamps
```

### File Operations

```bash
# Save to file
yttranscript VIDEO_ID --output transcript.txt

# Overwrite existing file without confirmation
yttranscript VIDEO_ID --output transcript.txt --force
```

## Examples

### Extract transcript in Markdown format with timestamps

```bash
yttranscript dQw4w9WgXcQ --format markdown --timestamps
```

Output:
```markdown
- **[00:00:00]** We're no strangers to love
- **[00:00:03]** You know the rules and so do I
- **[00:00:07]** A full commitment's what I'm thinking of
```

### Save Spanish transcript to file

```bash
yttranscript dQw4w9WgXcQ --language es --output transcript_es.txt
```

### Check available languages

```bash
yttranscript dQw4w9WgXcQ --list-languages
```

Output:
```
Available languages:
- en (English)
- es (Spanish) (auto-generated)
- fr (French) (auto-generated)
```

## Supported URL Formats

- `https://youtube.com/watch?v=VIDEO_ID`
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://youtube.com/embed/VIDEO_ID`
- `VIDEO_ID` (11-character video ID)

## Error Handling

The tool provides clear error messages for common issues:

- Invalid YouTube URLs
- Videos without transcripts
- Private or unavailable videos
- Network connectivity issues
- File permission errors

## Requirements

- Python 3.8 or higher
- Internet connection
- YouTube videos with available transcripts

## Contributing

This project was built using **Spec-Driven Development** methodology. For development workflow documentation, see:

- [Development Workflow Guide](.github/copilot-instructions.md)
- [Project Constitution](.specify/memory/constitution.md)

### Development Setup

```bash
git clone https://github.com/akshay-waghmare/youtube_transcript_downloader.git
cd youtube_transcript_downloader
pip install -e .[dev]
```

### Running Tests

```bash
pytest                          # Run all tests
pytest --cov=yttranscript      # Run with coverage
pytest tests/test_models.py    # Run specific test file
```

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](LICENSE)