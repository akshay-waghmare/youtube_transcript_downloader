# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-23

### Added
- Initial release of yttranscript CLI tool
- Support for extracting YouTube video transcripts
- Multiple output formats (plain text, Markdown)
- Optional timestamp inclusion in output
- Multi-language transcript support
- File output with overwrite protection
- Cross-platform compatibility (Windows, macOS, Linux)
- Comprehensive error handling and user-friendly messages
- Support for various YouTube URL formats and bare video IDs
- `--list-languages` flag to show available transcript languages
- `--force` flag for non-interactive file overwriting
- Complete CLI interface with help and version information

### Technical Details
- Built with Python 3.8+ compatibility
- Uses youtube-transcript-api for transcript extraction
- Click framework for CLI interface
- Comprehensive test suite with pytest
- Type hints throughout codebase
- Cross-platform file handling with UTF-8 encoding
- Exponential backoff retry logic for network operations

### Dependencies
- youtube-transcript-api >= 0.6.0
- click >= 8.0.0

### Development
- Test-driven development approach
- 70%+ code coverage
- Automated testing with pytest
- Support for uvx installation and usage
- MIT license