# Tasks: yttranscript CLI Tool

**Input**: Design documents from `/specs/001-transcript-downloader/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each user story.

## Format: `[ID] [P?] [Story] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4, US5)
- Include exact file paths in descriptions

## User Story Mapping
- **US1**: Basic Transcript Extraction (Priority P1)
- **US2**: Output Format Selection (Priority P2) 
- **US3**: File Output (Priority P2)
- **US4**: Multi-language Support (Priority P3)
- **US5**: Robust Error Handling (Priority P1)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure that all user stories depend on

- [ ] **T001** Create project directory structure: `src/yttranscript/`, `tests/`, `docs/`
- [ ] **T002** Initialize Python package with `pyproject.toml` using setuptools build system
- [ ] **T003** [P] Configure development dependencies: pytest, black, isort, mypy, pre-commit
- [ ] **T004** [P] Create package files: `src/yttranscript/__init__.py`, `src/yttranscript/__main__.py`
- [ ] **T005** [P] Setup CI/CD pipeline with GitHub Actions for Python 3.8-3.11 matrix
- [ ] **T006** [P] Configure pre-commit hooks for code quality (black, isort, mypy)
- [ ] **T007** Create basic README.md with installation and usage placeholders

## Phase 2: Foundational Components (Required by all user stories)

**Purpose**: Core building blocks that enable all user stories

### Data Models & Exceptions (US1, US2, US3, US4, US5)

- [ ] **T008** [US1] Create `src/yttranscript/exceptions.py` with custom exception hierarchy
  - YttranscriptError, InvalidUrlError, TranscriptNotAvailableError, LanguageNotFoundError, NetworkError, FileOutputError
- [ ] **T009** [US1] Create `src/yttranscript/models.py` with Video class and URL parsing
  - Video.from_url() method supporting youtube.com and youtu.be formats
- [ ] **T010** [US1] Add TranscriptSegment and Transcript classes to `models.py`
  - TranscriptSegment with text, start, duration, format_timestamp()
  - Transcript with segments, language_code, full_text property

### Core Extraction Logic (US1, US4, US5)

- [ ] **T011** [US1] Create `src/yttranscript/core.py` with TranscriptExtractor class
  - Integration with youtube-transcript-api library
  - Basic extract_transcript(video_id) method
- [ ] **T012** [US5] Add comprehensive error handling to core.py
  - Handle TranscriptsDisabled, NoTranscriptFound, VideoUnavailable, TooManyRequests
  - Convert library exceptions to custom exceptions with helpful messages

### Output Formatting (US1, US2)

- [ ] **T013** [US2] Create `src/yttranscript/formatters.py` with formatter interface
  - Formatter protocol definition
  - PlainFormatter class with format() method
- [ ] **T014** [US2] Add MarkdownFormatter class to formatters.py
  - Bullet-point formatting for transcript segments
  - Optional timestamp integration

---

## Phase 3: User Story Implementation

### US1: Basic Transcript Extraction (Priority P1) - MVP

**Goal**: Extract and display YouTube transcripts in plain text

- [ ] **T015** [US1] Create basic CLI interface in `src/yttranscript/cli.py`
  - Click command with URL argument
  - Basic transcript extraction and plain text output to stdout
- [ ] **T016** [US1] Add progress indicators using click.progressbar
  - Show extraction progress during API calls
- [ ] **T017** [US1] Implement console script entry point in pyproject.toml
  - Configure `yttranscript = "yttranscript.cli:main"`
- [ ] **T018** [US1] Create `tests/test_models.py` with Video URL parsing tests
  - Test valid YouTube URLs (youtube.com, youtu.be variants)
  - Test invalid URL handling and error messages
- [ ] **T019** [US1] Create `tests/test_core.py` with transcript extraction tests
  - Mock youtube-transcript-api responses
  - Test successful extraction scenarios
- [ ] **T020** [US1] Create `tests/test_cli.py` with basic CLI tests
  - Test command execution with valid URLs
  - Test error handling for invalid URLs

### US2: Output Format Selection (Priority P2)

**Goal**: Support plain text and Markdown output formats

- [ ] **T021** [US2] Add --format option to CLI with choices ['plain', 'markdown']
  - Default to plain format for backward compatibility
- [ ] **T022** [US2] Integrate formatters into CLI command flow
  - Route format selection to appropriate formatter
- [ ] **T023** [US2] Create `tests/test_formatters.py` with formatting tests
  - Test PlainFormatter output matches expected format
  - Test MarkdownFormatter bullet-point output
  - Test formatting with and without timestamps

### US3: File Output (Priority P2)

**Goal**: Save transcripts to files instead of stdout

- [ ] **T024** [US3] Add --output option to CLI accepting file path
  - Use click.Path() for path validation
- [ ] **T025** [US3] Implement file writing logic with error handling
  - Handle file permissions, disk space, invalid paths
  - Preserve UTF-8 encoding for special characters
- [ ] **T026** [US3] Add file overwrite protection and --force flag
  - Prompt user for confirmation on existing files
  - Allow bypass with --force flag
- [ ] **T027** [US3] Add file output tests to `tests/test_cli.py`
  - Test successful file creation
  - Test file overwrite scenarios
  - Test file permission error handling

### US4: Multi-language Support (Priority P3)

**Goal**: Extract transcripts in different languages

- [ ] **T028** [US4] Add language detection to core.py
  - Implement list_available_languages() method
  - Default to English with fallback to first available
- [ ] **T029** [US4] Add --language option to CLI
  - Accept language codes (en, es, fr, etc.)
- [ ] **T030** [US4] Add --list-languages flag to CLI
  - Display available languages for a video
  - Format as user-friendly list with language names
- [ ] **T031** [US4] Update core extraction logic for language selection
  - Pass language preference to youtube-transcript-api
  - Implement fallback logic for unavailable languages
- [ ] **T032** [US4] Add language support tests to `tests/test_core.py`
  - Test language listing functionality
  - Test language selection and fallback behavior
  - Mock multilingual video responses

### US5: Robust Error Handling (Priority P1) - Critical

**Goal**: Graceful failure handling with helpful error messages

- [ ] **T033** [US5] Implement URL validation in cli.py
  - Validate YouTube URL format before processing
  - Display clear error messages for invalid URLs
- [ ] **T034** [US5] Add network error handling to core.py
  - Handle connection timeouts and network failures
  - Implement retry logic with exponential backoff
- [ ] **T035** [US5] Create comprehensive error message templates
  - Context-specific error messages for each failure type
  - Include troubleshooting suggestions where appropriate
- [ ] **T036** [US5] Add error handling tests to `tests/test_cli.py`
  - Test invalid URL error messages
  - Test network failure scenarios
  - Test private/unavailable video handling

---

## Phase 4: Timestamps & Polish

### Timestamp Support (US1, US2)

- [ ] **T037** [US1,US2] Add --timestamps/--no-timestamps flag to CLI
  - Default to no timestamps for clean output
- [ ] **T038** [US1,US2] Update formatters to support timestamp inclusion
  - Modify PlainFormatter and MarkdownFormatter
  - Format timestamps as [HH:MM:SS]
- [ ] **T039** [US1,US2] Add timestamp tests to `tests/test_formatters.py`
  - Test timestamp formatting in both output formats
  - Test timestamp parsing and display accuracy

---

## Phase 5: Integration & End-to-End Testing

### Integration Tests

- [ ] **T040** [US1] Create `tests/test_integration.py` with real YouTube video tests
  - Use known public video IDs with available transcripts
  - Test end-to-end extraction workflow
- [ ] **T041** [US2,US3] Add file output integration tests
  - Test complete workflow: URL → extraction → file output
  - Verify file contents match expected format
- [ ] **T042** [US4] Add multilingual integration tests
  - Test with videos having multiple language options
  - Verify language selection and fallback behavior

### Performance & Quality

- [ ] **T043** [P] Add performance tests for large transcripts
  - Test memory usage stays under 100MB constitutional requirement
  - Test extraction completes within 10-second target
- [ ] **T044** [P] Add cross-platform testing to CI/CD
  - Test on Windows, macOS, Linux runners
  - Verify identical behavior across platforms
- [ ] **T045** [P] Achieve ≥90% code coverage requirement
  - Add missing test coverage for edge cases
  - Configure pytest-cov reporting

---

## Phase 6: Packaging & Distribution

### PyPI Packaging

- [ ] **T046** [P] Finalize pyproject.toml with complete metadata
  - Add description, license, author, homepage URLs
  - Specify minimum dependency versions
- [ ] **T047** [P] Create comprehensive README.md
  - Installation instructions (pip and uvx)
  - Usage examples for all CLI options
  - Troubleshooting section
- [ ] **T048** [P] Add LICENSE file (MIT license)
- [ ] **T049** [P] Create CHANGELOG.md with release notes
- [ ] **T050** [P] Test package installation and console script
  - Build wheel and sdist packages
  - Test installation from built packages
  - Verify uvx compatibility

### Documentation

- [ ] **T051** [P] Create `docs/installation.md` with detailed setup instructions
- [ ] **T052** [P] Create `docs/usage.md` with comprehensive examples
- [ ] **T053** [P] Create `docs/troubleshooting.md` with common issues and solutions

---

## Dependencies & Parallel Execution

### Critical Path (Must complete in order)
1. **Phase 1 Setup** (T001-T007) → **Phase 2 Foundational** (T008-T014) → **US1 MVP** (T015-T020)
2. **US1 Complete** → **US2, US3, US4, US5** can proceed in parallel
3. **All User Stories Complete** → **Phase 5 Integration** → **Phase 6 Packaging**

### Parallel Execution Opportunities
- **T003, T004, T005, T006, T007** can run in parallel after T002
- **T008, T009, T010** can be developed in parallel (different classes)
- **T018, T019, T020, T023** (all test files) can be developed in parallel
- **T021-T027** (US2), **T024-T027** (US3), **T028-T032** (US4) can proceed in parallel after US1
- **T046-T053** (documentation and packaging) can be developed in parallel

### Estimated Timeline
- **Phase 1-2**: 3-4 days (setup and foundations)
- **Phase 3**: 5-7 days (user story implementation)
- **Phase 4-5**: 3-4 days (polish and testing)
- **Phase 6**: 2-3 days (packaging and documentation)
- **Total**: 13-18 days for complete implementation

This task breakdown follows TDD principles with tests accompanying each implementation task, enables independent user story development, and maintains constitutional compliance throughout the development process.