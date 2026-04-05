# CLAUDE.md

This repository uses Claude/Codex as an execution agent, not just a chat assistant.

## Project Identity

- Product:
- Users:
- Primary outcome:
- Current phase:

## Runbook

### Start

```bash
# fill in the real command
```

### Test

```bash
# fill in the real command
```

### Build / Package

```bash
# fill in the real command
```

## Architecture Boundaries

- Define the core modules and their ownership.
- State which runtime/database/message gateway choices are authoritative.
- State what is transitional compatibility only.
- State what must not be expanded further.

## Repository Workflow

Use issue-centered closed-loop delivery by default:

1. Read the issue and local repo rules first.
2. Create a dedicated branch.
3. Implement only the issue scope.
4. Run targeted verification before commit.
5. Push, open PR, merge, then sync local `master`.

## Definition Of Done

A task is not done when code is written. It is done only when:

- the change is implemented
- the relevant checks passed
- the affected runtime path was verified when applicable
- the branch/PR state is clean and understandable
- local `master` is synced after merge

## Rules

- Do not revert unrelated local changes.
- Do not widen scope silently.
- Findings come before summaries in review work.
- Treat regression risk as a first-class concern.
- Promote only stable, repeatable rules into this file.
- Keep temporary debugging notes out of this file.

## Local Runtime Notes

- Ports:
- Required env vars:
- External services:
- Data/runtime config paths:

## Dangerous Actions

Require extra caution before:

- deleting branches
- overwriting user config
- stopping unknown processes
- changing production credentials
- force pushing
- destructive database operations

## Promotion Rules

When a new preference or workflow is discovered, classify it before storing it:

- Project-wide stable rule -> this file
- Personal preference -> personal memory, not this repo
- Temporary session note -> do not persist here
