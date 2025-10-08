# CLI Interface Contract

**Version**: 1.0.0  
**Date**: 2025-01-23

## Command Structure

### Basic Usage

```bash
yttranscript <youtube_url> [OPTIONS]
```

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--format` | choice(plain, markdown) | plain | Output format |
| `--output` | path | stdout | Output file path |
| `--language` | string | en | Transcript language code |
| `--timestamps/--no-timestamps` | flag | false | Include timestamps |
| `--list-languages` | flag | false | List available languages |
| `--help` | flag | - | Show help message |
| `--version` | flag | - | Show version |

### Examples

```bash
# Basic extraction to stdout
yttranscript https://youtube.com/watch?v=dQw4w9WgXcQ

# Markdown format with timestamps
yttranscript https://youtube.com/watch?v=dQw4w9WgXcQ --format markdown --timestamps

# Save to file
yttranscript https://youtube.com/watch?v=dQw4w9WgXcQ --output transcript.txt

# Spanish transcript
yttranscript https://youtube.com/watch?v=dQw4w9WgXcQ --language es

# List available languages
yttranscript https://youtube.com/watch?v=dQw4w9WgXcQ --list-languages
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Invalid URL |
| 2 | Transcript not available |
| 3 | Language not found |
| 4 | Network error |
| 5 | File output error |
| 99 | Unknown error |

## Output Formats

### Plain Text

```
Hello world
This is a test
Goodbye
```

### Plain Text with Timestamps

```
[00:00:00] Hello world
[00:00:02] This is a test
[00:00:05] Goodbye
```

### Markdown

```markdown
- Hello world
- This is a test
- Goodbye
```

### Markdown with Timestamps

```markdown
- **[00:00:00]** Hello world
- **[00:00:02]** This is a test
- **[00:00:05]** Goodbye
```

## Error Messages

### Invalid URL
```
Error: Invalid YouTube URL provided
Expected format: https://youtube.com/watch?v=VIDEO_ID or https://youtu.be/VIDEO_ID
```

### No Transcript Available
```
Error: No transcript available for this video
The video may be private, deleted, or have transcripts disabled
```

### Language Not Found
```
Error: Transcript not available in language 'es'
Available languages: en, fr, de
Use --list-languages to see all available options
```

### Network Error
```
Error: Network connection failed
Check your internet connection and try again
```

### File Permission Error
```
Error: Cannot write to file 'transcript.txt'
Check file permissions and disk space
```

## Progress Indicators

### Normal Operation
```
Extracting transcript... ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
```

### Language Listing
```
Fetching available languages... ✓
Available languages:
- en (English)
- es (Spanish) 
- fr (French)
```

## Version Information

```bash
yttranscript --version
# Output: yttranscript version 0.1.0
```

## Help Output

```bash
yttranscript --help
# Usage: yttranscript [OPTIONS] URL
# 
#   Extract transcript from YouTube video.
# 
# Arguments:
#   URL  YouTube video URL
# 
# Options:
#   --format [plain|markdown]   Output format  [default: plain]
#   --output PATH              Output file path
#   --language TEXT            Transcript language code  [default: en]
#   --timestamps / --no-timestamps
#                              Include timestamps  [default: no-timestamps]
#   --list-languages           List available languages
#   --version                  Show version and exit
#   --help                     Show this message and exit
```