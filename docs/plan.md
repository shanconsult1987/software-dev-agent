# Feature Plan

## Feature

Add deployment risk analysis.

## Goal

Allow the development agent to evaluate a proposed software change.

## Input

A textual description of a software change.

## Output

A risk classification:

- LOW
- MEDIUM
- HIGH

## Success Criteria

1. The feature accepts a change description.
2. The feature returns a risk level.
3. Invalid input is rejected.
4. Unit tests cover the behavior.
5. CI passes before merge.

## Human Approval

HIGH-risk changes require human approval.