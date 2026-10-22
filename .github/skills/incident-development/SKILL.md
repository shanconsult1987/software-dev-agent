---
name: incident-development
description: Rules for implementing CityOps incident functionality.
---

# Incident Development Skill

Use this skill whenever working on
CityOps incident functionality.

## Incident Model

An incident has:

- id
- title
- severity
- status

## Supported Severity

- high
- medium

## Supported Status

- open
- closed

## API Rules

Incident endpoints:

- return JSON
- return 404 for missing incidents
- preserve existing endpoints
- follow existing Flask patterns

## Testing

Every behavior change must include tests.

Minimum coverage:

1. successful behavior
2. missing resource
3. existing behavior remains unchanged

## Implementation

Prefer existing structures.

Do not introduce:

- databases
- new frameworks
- unnecessary packages

## Completion

Run:

python -m unittest discover -v

Then:

python eval/evaluate.py

Review the final diff before completion.