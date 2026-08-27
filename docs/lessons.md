# lessons.md — what it is and how to use it

`lessons.md` is a running log of things learned while working in this repo.
It exists because context resets between sessions; anything not written down
is lost.

## When to write an entry

Write when you hit something non-obvious that would cost time to rediscover:

- A failure and its actual root cause.
- An API or tool that behaves differently than documented.
- A decision made, and the reason, so it is not relitigated.
- An approach that was tried and rejected, and why.

## When NOT to write

- Task status or progress narration.
- Generic best practices.
- Anything already covered in `AGENTS.md` or `docs/DECISIONS.md`.

## Format

Use one line or a short block per lesson, newest last, grouped by area.

## Maintenance

- Read this file at the start of every session.
- If a lesson is stable and always applies, promote it to `AGENTS.md` or
  `docs/DECISIONS.md` and delete it here.
- Prune entries that are no longer true. A stale lesson is worse than no lesson.
