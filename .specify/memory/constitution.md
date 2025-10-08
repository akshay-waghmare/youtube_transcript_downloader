<!--
Sync Impact Report:
Version change: Template → 1.0.0
Added sections: All core principles and governance
Templates requiring updates: ✅ All templates aligned
First constitutional establishment for yttranscript project
-->

# yttranscript Constitution

## Core Principles

### I. Minimalism First
Every feature must justify its existence. The CLI tool should do one thing well: extract YouTube video transcripts and format them for output. No feature creep. No unnecessary dependencies. Start with the simplest implementation that works, then enhance based on actual user needs.

### II. CLI-Centric Design
The primary interface is a command-line tool with clear, predictable behavior. Follow Unix philosophy: read from stdin/args, write to stdout, errors to stderr. Support both interactive use and scripting. Provide both human-readable and machine-readable output formats (plain text, Markdown).

### III. Test-Driven Development (NON-NEGOTIABLE)
TDD mandatory for all functionality: Write tests → Verify user approval → Tests fail → Implement → Tests pass. Red-Green-Refactor cycle strictly enforced. Every function must have corresponding unit tests. Integration tests required for YouTube API interactions and file I/O operations.

### IV. Robust Error Handling
Network operations and external API calls MUST handle failures gracefully. Provide meaningful error messages that help users understand what went wrong and how to fix it. Handle common scenarios: network timeouts, unavailable videos, private videos, age-restricted content, API rate limits.

### V. Cross-Platform Compatibility
The tool must work identically on Windows, macOS, and Linux. Use Python's standard library and cross-platform packages. File paths, text encoding, and output formatting must be consistent across platforms. No platform-specific dependencies unless absolutely necessary.

## Technical Standards

Python 3.8+ required for broad compatibility. Use type hints for all function signatures. Follow PEP 8 style guidelines with black formatting. Dependencies must be minimal and well-maintained. Package installation should be simple: `pip install yttranscript` or `uv tool install yttranscript`.

## Quality Assurance

Code coverage must be ≥90%. All public functions require docstrings with examples. Performance tests for large transcript processing. Security review for any user input handling. Documentation must include installation, usage examples, and troubleshooting guide.

## Governance

This constitution supersedes all other development practices. All features, changes, and decisions must align with these principles. Amendments require justification, community input (if applicable), and migration plan. Complexity must be justified against the Minimalism First principle.

All pull requests must verify compliance with these principles. Code reviews must check adherence to TDD, error handling, and cross-platform compatibility requirements.

**Version**: 1.0.0 | **Ratified**: 2025-01-23 | **Last Amended**: 2025-01-23