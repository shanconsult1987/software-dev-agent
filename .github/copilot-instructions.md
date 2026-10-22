# CityOps Copilot Instructions

## Purpose

CityOps is a minimal Flask application demonstrating
agentic software development with GitHub.

## Technology

- Python
- Flask
- unittest
- GitHub Actions

## Core Principle

Keep the repository small.

Prefer:

- minimal changes
- existing patterns
- readable code
- automated tests
- explicit validation

Avoid:

- unnecessary frameworks
- unnecessary dependencies
- unrelated refactoring
- large architectural changes

## Development Workflow

For every software task:

1. Understand the issue.
2. Inspect the repository.
3. Read applicable instructions.
4. Identify relevant files.
5. Create a structured plan.
6. Validate the plan.
7. Implement the smallest safe change.
8. Add or update tests.
9. Run the test suite.
10. Run evaluation.
11. Review the diff.
12. Perform security checks.
13. Record important decisions.
14. Produce a reviewable PR.

## State

Agent progress is represented by:

.agent/state.json

## Audit

Agent/application activity is recorded in:

.agent/audit.jsonl

Do not delete or rewrite audit history
to hide previous actions.

## Security

Never:

- commit credentials
- expose API keys
- hard-code passwords
- disable security controls
- remove tests to make CI pass
- force-push shared branches

## Definition of Done

A task is complete only when:

- requirements are satisfied
- tests pass
- evaluation passes
- CI passes
- security review passes
- state is updated
- audit trail exists
- diff is minimal
- human review is available