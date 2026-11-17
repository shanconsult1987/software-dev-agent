
# Software Development Agent Instructions

## Repository purpose

This repository demonstrates a controlled
agentic software development lifecycle.

## Development rules

- Use Python.
- Keep the application minimal.
- Follow existing coding patterns.
- Use pytest for unit tests.
- Validate user inputs.
- Do not introduce unnecessary dependencies.

## Agent rules

- Planner must plan, not execute.
- Developer must follow an approved plan.
- Reviewer must independently evaluate changes.
- Summary Agent must record outcomes.

## Security

- Never expose API keys.
- Never commit .env.
- Never modify workflow permissions without approval.
- Never merge automatically.
- Preserve audit records.

## Quality

- All tests must pass.
- Every feature needs acceptance criteria.
- Every pull request must include test evidence.
- Code reviews are mandatory for all changes.
