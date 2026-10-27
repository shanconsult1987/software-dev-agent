# Software Development Agent

## Purpose

This repository is a minimal software development agent demonstration.

## Development rules

- Keep the application simple.
- Use Python.
- Use Flask for the API.
- Use pytest for tests.
- Do not introduce unnecessary frameworks.
- Every code change must have tests.
- Do not modify unrelated files.
- Explain the implementation before making significant changes.

## Quality rules

Before completing a task:

1. Run all unit tests.
2. Check for regressions.
3. Review changed files.
4. Update documentation when behavior changes.

## Security rules

- Never hard-code secrets.
- Never commit API keys.
- Validate external input.
- Keep permissions least-privileged.