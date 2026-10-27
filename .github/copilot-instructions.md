# Software Development Agent

## Purpose

This repository demonstrates a simple software development agent.

The agent implements software changes from GitHub Issues.

## Technology

- Python
- Flask
- pytest

## Development Principles

1. Keep the application simple.
2. Make the smallest change required.
3. Every feature requires tests.
4. Do not modify unrelated files.
5. Do not add unnecessary dependencies.
6. Never add secrets.
7. Run all tests before completing a task.
8. Preserve existing API behavior.

## SDLC

Issue
→ Plan
→ Implement
→ Test
→ Pull Request
→ CI
→ Security
→ Review
→ Merge
→ Deploy

## Testing

Run:

python -m pytest -v