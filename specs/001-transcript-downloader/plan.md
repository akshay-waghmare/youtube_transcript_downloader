# Implementation Plan: yttranscript CLI Tool

**Branch**: `001-transcript-downloader` | **Date**: 2025-01-23 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-transcript-downloader/spec.md`

## Summary

Build a minimal Python CLI tool that extracts YouTube video transcripts using the youtube-transcript-api library. The tool will support plain text and Markdown output formats, optional timestamps, multi-language support, and file output capabilities. Focus on cross-platform compatibility, robust error handling, and PyPI distribution with uvx support.

## Technical Context

**Language/Version**: Python 3.8+ (broad compatibility requirement)  
**Primary Dependencies**: youtube-transcript-api (transcript extraction), click (CLI framework), setuptools (packaging)  
**Storage**: File system for output files, no persistent storage required  
**Testing**: pytest (unit/integration tests), pytest-cov (code coverage tracking), requests-mock (API mocking)  
**Target Platform**: Cross-platform (Windows, macOS, Linux) CLI application
**Project Type**: Single-module CLI tool with minimal dependencies  
**Performance Goals**: <10 seconds transcript extraction, <100MB memory usage  
**Constraints**: No API keys required, minimal dependencies, cross-platform compatibility  
**Scale/Scope**: Single-user CLI tool, typical video transcripts (up to 10+ hours)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ Minimalism First
- Single purpose: extract YouTube transcripts ✓
- Minimal dependencies: youtube-transcript-api, click, setuptools ✓
- No feature creep: core functionality only ✓

### ✅ CLI-Centric Design  
- Command-line interface with clear inputs/outputs ✓
- Unix philosophy: args → stdout, errors → stderr ✓
- Human-readable (plain text) and structured (Markdown) formats ✓

### ✅ Test-Driven Development
- TDD approach: tests → implement → verify ✓
- Unit tests for all functions planned ✓
- Integration tests for YouTube API interactions planned ✓

### ✅ Robust Error Handling
- Network timeout handling ✓
- Invalid URL validation ✓
- Private/unavailable video error messages ✓
- Graceful failure scenarios covered ✓

### ✅ Cross-Platform Compatibility
- Python standard library usage ✓
- Cross-platform dependencies (click) ✓
- Consistent file path handling planned ✓
- No platform-specific code ✓

## Project Structure

### Documentation (this feature)

```
specs/001-transcript-downloader/
├── spec.md           # Feature specification
├── plan.md           # This implementation plan
├── tasks.md          # Task breakdown (to be generated)
├── data-model.md     # Data structures and entities
├── research.md       # Technical research and decisions
└── contracts/        # API contracts and interfaces
```

### Source Code Structure

```
yttranscript/
├── pyproject.toml         # Modern Python packaging
├── README.md              # Installation and usage
├── LICENSE                # MIT license
├── src/
│   └── yttranscript/
│       ├── __init__.py    # Package initialization
│       ├── __main__.py    # Entry point for python -m yttranscript
│       ├── cli.py         # Click-based command interface
│       ├── core.py        # Core transcript extraction logic
│       ├── formatters.py  # Output formatting (plain/markdown)
│       ├── models.py      # Data models and types
│       └── exceptions.py  # Custom exception classes
├── tests/
│   ├── __init__.py
│   ├── test_cli.py        # CLI interface tests
│   ├── test_core.py       # Core functionality tests
│   ├── test_formatters.py # Output formatting tests
│   └── fixtures/          # Test data and mock responses
└── docs/                  # User documentation
    ├── installation.md
    ├── usage.md
    └── troubleshooting.md
```

## Phase 0: Research & Technology Validation

### Research Topics

1. **youtube-transcript-api Library Analysis**
   - API stability and maintenance status
   - Language support capabilities
   - Error handling patterns
   - Rate limiting behavior

2. **Click Framework Integration**
   - Command structure design
   - Parameter validation
   - Progress indicators implementation
   - Error handling integration

3. **Cross-Platform Testing Strategy**
   - GitHub Actions CI/CD setup
   - Windows/macOS/Linux compatibility validation
   - Python version matrix testing

4. **PyPI Packaging Requirements**  
   - pyproject.toml configuration
   - Console scripts entry points
   - uvx compatibility requirements
   - Dependency management

## Phase 1: Core Architecture Design

### Data Model Design
- Video entity with URL, title, available languages
- Transcript entity with content, timestamps, language
- Output configuration with format, file options
- CLI options parsing and validation

### API Contracts
- Core transcript extraction interface
- Formatter interface for different output types
- Error handling contracts
- CLI command structure

### Integration Points
- youtube-transcript-api integration wrapper
- File system operations abstraction
- Progress reporting interface
- Language detection and selection logic

## Phase 2: Implementation Strategy

### Development Phases

1. **MVP Implementation** (P1 features)
   - Basic URL parsing and validation (including bare video IDs)
   - Core transcript extraction using youtube-transcript-api
   - Plain text output to stdout
   - Basic error handling with retry logic and exponential backoff

2. **Format & Output Extension** (P2 features)
   - Markdown formatting with bullet points
   - File output with --output flag and --force option
   - Optional timestamp inclusion
   - Status indicators (spinner/message, not progress bar)

3. **Language & Polish** (P2-P3 features)
   - Multi-language support with --language flag
   - --list-languages functionality
   - Comprehensive error messages with templates
   - Package distribution setup
   - JSON output format (deferred P3 for machine-readable requirement)

### Testing Strategy

1. **Unit Tests**
   - URL validation logic
   - Transcript formatting functions  
   - CLI parameter parsing
   - Error handling scenarios

2. **Integration Tests**
   - End-to-end transcript extraction
   - File output operations
   - Multi-language functionality
   - Cross-platform behavior

3. **Mock Testing**
   - Mock YouTube API responses
   - Network failure simulation
   - Invalid video scenarios

### Quality Gates

- ≥90% code coverage requirement
- All tests pass on Python 3.8, 3.9, 3.10, 3.11+
- Cross-platform validation (Windows, macOS, Linux)
- Performance validation (<10s extraction, <100MB memory)
- Security scan for dependency vulnerabilities

## Risk Mitigation

### Technical Risks
- **youtube-transcript-api reliability**: Plan fallback error messages, monitor library maintenance
- **Cross-platform file handling**: Use pathlib, test extensively across platforms
- **YouTube API changes**: Implement robust error handling, graceful degradation

### Operational Risks  
- **PyPI packaging complexity**: Start with simple setup, iterate based on feedback
- **User experience**: Extensive CLI testing, clear error messages, comprehensive documentation

## Success Metrics

- Tool successfully extracts transcripts from 95% of public videos with transcripts
- Installation works via both `pip install yttranscript` and `uvx yttranscript`
- Processing time <10 seconds for typical videos
- Memory usage <100MB during operation
- Zero crashes on valid inputs across all supported platforms

## Next Steps

1. Generate detailed task breakdown with `/speckit.tasks`
2. Create research.md with technical investigation results
3. Design data-model.md with entity definitions
4. Implement MVP following TDD approach
5. Iterate through P2/P3 features based on user feedback
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```
# [REMOVE IF UNUSED] Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure: feature modules, UI flows, platform tests]
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

## Complexity Tracking

*Fill ONLY if Constitution Check has violations that must be justified*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
