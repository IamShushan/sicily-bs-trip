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

## Privacy scanning

- 2026-08-28: `python3 scripts/privacy_scan.py --all-files` reads every path from
  `git ls-files` directly from the working tree. During a tracked-file rename it
  fails closed on the missing old path until the rename is staged. Stage the
  rename first, then run the full scan; the commit hook still scans the staged
  content.

## Git and pull requests

- 2026-08-28: A follow-up branch created from an unmerged feature branch
  produces a stacked PR. PR #9 therefore targets `feat/collapsible-days`, and
  merging it does not publish to `main`. Before branching, check whether the
  parent is merged; if stacking is intentional, state the base clearly and plan
  the final PR from the parent branch to `main`.
