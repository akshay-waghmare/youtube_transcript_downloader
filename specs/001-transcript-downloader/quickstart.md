# Quickstart Guide: yttranscript Development

**Date**: 2025-01-23  
**Audience**: Developers implementing the yttranscript CLI tool

## Development Setup

### Prerequisites

- Python 3.8+ installed
- Git for version control
- Code editor with Python support

### Environment Setup

```bash
# Clone the repository
git clone https://github.com/username/yttranscript.git
cd yttranscript

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install development dependencies
pip install -e .[dev]
```

### Project Structure Creation

```bash
# Create source structure
mkdir -p src/yttranscript
mkdir -p tests
mkdir -p docs

# Create essential files
touch src/yttranscript/__init__.py
touch src/yttranscript/__main__.py
touch src/yttranscript/cli.py
touch src/yttranscript/core.py
touch src/yttranscript/formatters.py
touch src/yttranscript/models.py
touch src/yttranscript/exceptions.py

# Create test files
touch tests/__init__.py
touch tests/test_cli.py
touch tests/test_core.py
touch tests/test_formatters.py
```

## TDD Implementation Order

Following constitutional TDD requirements:

### Phase 1: Core Data Models (test_models.py)

```python
# Test first
def test_video_from_url_valid():
    video = Video.from_url('https://youtube.com/watch?v=dQw4w9WgXcQ')
    assert video.video_id == 'dQw4w9WgXcQ'

def test_video_from_url_invalid():
    with pytest.raises(InvalidUrlError):
        Video.from_url('https://not-youtube.com')

# Then implement Video class in models.py
```

### Phase 2: Core Extraction Logic (test_core.py)

```python
# Test first
def test_extract_transcript_success(mock_api):
    extractor = TranscriptExtractor()
    transcript = extractor.extract('dQw4w9WgXcQ')
    assert isinstance(transcript, Transcript)
    assert len(transcript.segments) > 0

# Then implement TranscriptExtractor in core.py
```

### Phase 3: Output Formatting (test_formatters.py)

```python
# Test first
def test_plain_formatter():
    formatter = PlainFormatter()
    result = formatter.format(mock_transcript)
    assert "Hello world" in result

def test_markdown_formatter():
    formatter = MarkdownFormatter()
    result = formatter.format(mock_transcript)
    assert "- Hello world" in result

# Then implement formatters in formatters.py
```

### Phase 4: CLI Interface (test_cli.py)

```python
# Test first
def test_cli_basic_usage(runner):
    result = runner.invoke(main, ['https://youtube.com/watch?v=test'])
    assert result.exit_code == 0

# Then implement CLI in cli.py
```

## Key Dependencies

### pyproject.toml

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "yttranscript"
version = "0.1.0"
description = "Extract YouTube video transcripts from command line"
requires-python = ">=3.8"
dependencies = [
    "youtube-transcript-api>=0.6.0",
    "click>=8.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "black>=23.0.0",
    "isort>=5.12.0",
    "mypy>=1.0.0",
    "pre-commit>=3.0.0",
]

[project.scripts]
yttranscript = "yttranscript.cli:main"

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=yttranscript --cov-report=term-missing"

[tool.black]
line-length = 88
target-version = ["py38"]

[tool.isort]
profile = "black"
```

## Testing Strategy

### Unit Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=yttranscript --cov-report=html

# Run specific test file
pytest tests/test_core.py -v
```

### Mock Testing Setup

```python
# tests/conftest.py
import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_youtube_api():
    mock = MagicMock()
    mock.get_transcript.return_value = [
        {'text': 'Hello world', 'start': 0.0, 'duration': 2.5},
        {'text': 'This is a test', 'start': 2.5, 'duration': 3.0},
    ]
    return mock
```

### Integration Tests

```python
# Use real video IDs for integration tests
INTEGRATION_VIDEO_ID = 'dQw4w9WgXcQ'  # Public video with transcript

def test_end_to_end_extraction():
    """Test against real YouTube video."""
    result = extract_transcript(f'https://youtube.com/watch?v={INTEGRATION_VIDEO_ID}')
    assert result is not None
    assert len(result) > 0
```

## Code Quality Tools

### Pre-commit Setup

```bash
# Install pre-commit hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

### .pre-commit-config.yaml

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.9.1
    hooks:
      - id: black
  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.1
    hooks:
      - id: mypy
```

## Development Workflow

### 1. Feature Development

```bash
# Create feature branch
git checkout -b feature/basic-extraction

# Write tests first (TDD)
# Implement feature
# Run tests
pytest

# Format code
black src/ tests/
isort src/ tests/

# Type check
mypy src/

# Commit changes
git add .
git commit -m "feat: implement basic transcript extraction"
```

### 2. Testing Checklist

- [ ] Unit tests pass with ≥90% coverage
- [ ] Integration tests pass with real YouTube videos
- [ ] Cross-platform testing (Windows, macOS, Linux)
- [ ] Python version matrix (3.8, 3.9, 3.10, 3.11+)
- [ ] Code formatting (black, isort)
- [ ] Type checking (mypy)
- [ ] Error handling scenarios tested

### 3. Release Process

```bash
# Update version in pyproject.toml
# Run full test suite
pytest

# Build package
python -m build

# Test installation
pip install dist/yttranscript-*.whl
yttranscript --version

# Upload to PyPI (test first)
twine upload --repository testpypi dist/*
twine upload dist/*
```

## Performance Testing

### Memory Profiling

```python
import tracemalloc

tracemalloc.start()
# Run transcript extraction
current, peak = tracemalloc.get_traced_memory()
print(f"Current memory usage: {current / 1024 / 1024:.1f} MB")
print(f"Peak memory usage: {peak / 1024 / 1024:.1f} MB")
tracemalloc.stop()
```

### Timing Tests

```python
import time

start_time = time.time()
result = extract_transcript(video_url)
duration = time.time() - start_time
print(f"Extraction took {duration:.2f} seconds")
```

## Troubleshooting Common Issues

### Import Errors
- Ensure virtual environment is activated
- Check PYTHONPATH includes src directory
- Verify package installed with `pip install -e .`

### Test Failures  
- Check internet connection for integration tests
- Verify mock setup for unit tests
- Ensure test video IDs are still valid

### CLI Not Working
- Check console script entry point in pyproject.toml
- Reinstall package: `pip install -e .`
- Verify PATH includes Python scripts directory

This quickstart guide provides a structured approach to implementing the yttranscript tool following TDD principles and constitutional requirements.