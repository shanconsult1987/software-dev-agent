---
applyTo: "**/*.py"
---

# Python Instructions

When modifying Python:

- Follow existing patterns.
- Keep functions small.
- Prefer standard library functionality.
- Avoid unnecessary dependencies.
- Preserve existing API behavior.
- Add unittest coverage for behavior changes.
- Validate error conditions.
- Do not modify unrelated functionality.

Before completing a task, run:

python -m unittest discover -v

Then run:

python eval/evaluate.py