"""CONTRIBUTING.md - Guidelines for contributing to the project."""

# Contributing to Medical Review Sentiment Analysis

Thank you for your interest in contributing!

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/medical-review-sentiment-mlops.git`
3. Create a virtual environment: `uv venv` and activate it
4. Install dev dependencies: `uv sync --extra dev --extra lint`

## Development Workflow

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Make your changes
3. Run tests: `make test`
4. Run linting: `make lint`
5. Commit with clear message: `git commit -m "feat: add new feature"`
6. Push and create a Pull Request

## Code Style

- Follow PEP 8
- Use type hints for all functions
- Run `make format` to auto-format code
- Maximum line length: 100 characters

## Testing

- Write tests for new features
- Ensure all tests pass: `make test`
- Aim for > 80% coverage: `make test-cov`

## Documentation

- Update README.md if needed
- Add docstrings to all functions
- Update CHANGELOG.md

## Questions?

Open an issue or start a discussion!
