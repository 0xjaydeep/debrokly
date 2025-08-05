# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

"Debrokly" is a Python library and CLI tool for analyzing password-protected credit card statement PDFs. The project extracts transaction data from various bank statement formats and exports to CSV/Excel.

**Key Features:**
- Generic format detection for any credit card statement
- Password-protected PDF handling
- OCR/LLM-based parsing for diverse PDF formats
- Python library with CLI interface
- Export to CSV and Excel formats

**Current Status:** Requirements defined, ready for development setup and implementation.

## Requirements Documentation

See `REQUIREMENTS.md` for complete project specifications, including:
- Detailed feature requirements
- Technical architecture decisions
- Development phases and success criteria
- Target user scenarios and use cases

## Development Setup

Since this is a new project with no established tooling:

1. The project will likely need a Python package manager (pip, poetry, uv, etc.)
2. No build, test, or lint commands are available yet
3. No project dependencies or virtual environment configuration exists
4. No source code structure has been established

## Next Steps for Development

When beginning development on this project, you'll need to:

1. Choose and set up a Python package manager and virtual environment
2. Create the basic project structure (src/, tests/, etc.)
3. Add a pyproject.toml, setup.py, or requirements.txt for dependencies
4. Establish development commands for testing, linting, and building

## Repository Information

- License: MIT
- Current branch: dev
- Main branch: main
- Owner: Jaydeep Chauhan